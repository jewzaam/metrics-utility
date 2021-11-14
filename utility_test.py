import utility
import time
import prometheus_client

if __name__ == '__main__':
    # simple test, toggle a metric on and off...
    # start metrics on port 7777

    # Start up the server to expose the metrics.
    prometheus_client.start_http_server(7777)
    
    """
    Note this is successful only if the metric has labels.
    If it doesn't have labels I didn't find an easy way to remove the value.
    The best option is to set value back to the defaul, which is 0.0 in __init__.
    If you set None for the value and the metric has no labels it will fail.
    """

    labels={"foo":"bar"}
    while True:
        utility.set("utility_test_labels", 200, labels)
        time.sleep(5)
        utility.set("utility_test_labels", None, labels)
        time.sleep(5)

