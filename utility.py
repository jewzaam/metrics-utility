import time
import re
import os
import socket
from threading import Thread

import prometheus_client

gauges = {}
counters = {}
filesWatched = []

DEBUG = False

def setDebug(value):
    global DEBUG
    DEBUG = value

def debug(message):
    if DEBUG == True:
        print(message)

def enrichLabels(labelDict):
    if labelDict is None:
        return labelDict
    if "host" in labelDict:
        return labelDict
    host=socket.gethostname().lower()
    labelDict.update(
        {
            "host": host,
        }
    )

def findNewestFile(directory, logfileregex):
    now=time.time()
    filemtimes = {}
    for root, _, files in os.walk(directory, topdown=False):
        for name in files:
            m = re.match(logfileregex, name)
            if m is not None:
                filename = os.path.join(root, name)
                mtime = os.path.getmtime(filename)
                if mtime >= now - 30*60:
                    # file was modified in the last 30 minutes.  consider it. else ignore it.
                    filemtimes[mtime] = filename
    s = sorted(filemtimes.items())
    if len(s) == 0:
        return None
    return s[-1][1]

def watchFile(filename, frequencySeconds, callback):
    try:
        if filename in filesWatched:
            print("Attempted create duplicate watchFile on: {}".format(filename))
            pass

        print("Creating watchFile on: {}".format(filename))

        filesWatched.append(filename)
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(frequencySeconds)
                else:
                    callback(filename, line)
    except Exception as e:
        # print the error in case it helps debug and remove the file from being tracked
        print(e)
        if filename in filesWatched:
            filesWatched.remove(filename)
        pass

def watchDirectory(logdir, logfileregex, frequencySeconds, callback):
    while True:
        newestLogFile = findNewestFile(logdir, logfileregex)
        while newestLogFile is None or newestLogFile in filesWatched:
            time.sleep(frequencySeconds)
            newestLogFile = findNewestFile(logdir, logfileregex)

        # got a new log file, attempt to start watching it
        t = Thread(target=watchFile, args=(newestLogFile,frequencySeconds,callback), daemon=True)
        t.start()

def getGauge(name, description, labelDict):
    if name in gauges:
        gauge = gauges[name]
    else:
        print("Creating Gauge: {}({})".format(name,labelDict))
        gauge = prometheus_client.Gauge(name, description, labelDict)
        gauges[name] = gauge
    return gauge

def getCounter(name, description, labelDict):
    if name in counters:
        counter = counters[name]
    else:
        print("Creating Counter: {}".format(name))
        counter = prometheus_client.Counter(name, description, labelDict)
        counters[name] = counter
    return counter

def set(name, value, labelDict):
    enrichLabels(labelDict)
    gauge = getGauge(name, "", labelDict.keys())
    debug("utility.set({}, {}, {})".format(name, value, labelDict))
    if len(labelDict.keys()) > 0:
        if value is not None:
            gauge.labels(*labelDict.values()).set(value)
        else:
            gauge.remove(*labelDict.values())
    else:
        # cannot clear value if there is no label, just let the error propogate up
        gauge.set(value)

def add(name, value, labelDict):
    enrichLabels(labelDict)
    gauge = getGauge(name, "", labelDict.keys())
    debug("utility.add({}, {}, {})".format(name, value, labelDict))
    if len(labelDict.keys()) > 0:
        if value is not None:
            gauge.labels(*labelDict.values()).inc(value)
        else:
            gauge.remove(*labelDict.values())
    else:
        gauge.inc(value)

def inc(name, labelDict):
    enrichLabels(labelDict)
    counter = getCounter(name, "", labelDict.keys())
    debug("utility.inc({}, {})".format(name, labelDict))
    if len(labelDict.keys()) > 0:
        counter.labels(*labelDict.values()).inc()
    else:
        counter.inc()

def dec(name, labelDict):
    enrichLabels(labelDict)
    counter = getCounter(name, "", labelDict.keys())
    debug("utility.dec({}, {})".format(name, labelDict))
    if len(labelDict.keys()) > 0:
        counter.labels(*labelDict.values()).dec()
    else:
        counter.dec()

def metrics(port):
    prometheus_client.start_http_server(port)


