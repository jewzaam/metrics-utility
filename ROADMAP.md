# Roadmap - Future Improvements

This document tracks potential improvements and breaking changes for future major versions of `metrics-utility`.

## Version 1.0.0 - API Modernization (Breaking Changes)

When ready to break backward compatibility, consider these improvements:

### API Naming Conventions

Rename functions to follow Python PEP 8 snake_case conventions:

| Current (v0.x)      | Proposed (v1.0)        | Notes                           |
|---------------------|------------------------|---------------------------------|
| `setDebug()`        | `set_debug()`          | Follow Python naming            |
| `enrichLabels()`    | `enrich_labels()`      | Follow Python naming            |
| `findNewestFile()`  | `find_newest_file()`   | Follow Python naming            |
| `watchFile()`       | `watch_file()`         | Follow Python naming            |
| `watchDirectory()`  | `watch_directory()`    | Follow Python naming            |
| `getGauge()`        | Internal only          | Not in public API               |
| `getCounter()`      | Internal only          | Not in public API               |

### Parameter Naming

Rename parameters to follow snake_case:

- `labelDict` → `labels` or `label_dict`
- `frequencySeconds` → `frequency_seconds`
- `newestLogFile` → `newest_log_file`
- `filesWatched` → `files_watched`

### Code Quality Improvements

1. **Logging Framework**
   - Replace `print()` statements with proper Python `logging` module
   - Allows users to configure log levels and handlers
   - More flexible than current debug flag

2. **Path Operations**
   - Migrate from `os.path` to `pathlib.Path`
   - More modern, cleaner API
   - Better cross-platform support

3. **Exception Handling**
   - Replace broad `except Exception` with specific exception types
   - Better error messages and handling
   - Allow users to handle specific errors

4. **Type Annotations**
   - Use `prometheus_client` types instead of `Any`
   - More precise type hints throughout
   - Better IDE support

### API Improvements

1. **Avoid Shadowing Builtins**
   - Rename `set()` function to `set_gauge()` or `gauge_set()`
   - Clearer and avoids shadowing Python's built-in `set`

2. **Context Managers**
   - Add context manager support for metrics lifecycle
   ```python
   with metrics_utility.gauge("my_metric", labels={"x": "y"}) as g:
       g.set(42)
   ```

3. **Decorator Support**
   - Add decorators for common patterns
   ```python
   @metrics_utility.time_execution("function_duration")
   def my_function():
       pass
   ```

4. **Configuration Object**
   - Replace global `DEBUG` flag with configuration object
   ```python
   config = metrics_utility.Config(debug=True, auto_enrich=True)
   metrics_utility.configure(config)
   ```

## Version 0.x.x - Non-Breaking Improvements

These can be done without breaking compatibility:

### Documentation

- [ ] Add more examples in `examples/` directory
- [ ] Add API documentation with Sphinx
- [ ] Create tutorial/guide for common use cases
- [ ] Add troubleshooting section to README

### Testing

- [ ] Increase test coverage to 90%+
- [ ] Add property-based testing with Hypothesis
- [ ] Add benchmarks for performance testing
- [ ] Add stress tests for file watching

### Features

- [ ] Add metric deletion/cleanup utilities
- [ ] Support for Prometheus histograms and summaries
- [ ] Add health check endpoint helper
- [ ] Support for metric metadata (HELP, TYPE)
- [ ] Add batch metric updates
- [ ] Support for custom label enrichment functions

### Infrastructure

- [ ] Publish to PyPI for `pip install metrics-utility`
- [ ] Set up automated releases
- [ ] Add security scanning (Dependabot, Snyk)
- [ ] Add performance benchmarks in CI
- [ ] Create Docker image with utility pre-installed

### Developer Experience

- [ ] Add pre-commit hooks
- [ ] Improve error messages
- [ ] Add debug mode that shows metric creation/updates
- [ ] Create development container config

## Migration Path to v1.0

When ready for v1.0 with breaking changes:

1. **v0.9.0 - Deprecation Warnings**
   - Add new snake_case functions alongside old ones
   - Mark old functions as deprecated with warnings
   - Update documentation to show new API

2. **v0.9.x - Migration Period**
   - Give users 6-12 months to migrate
   - Provide migration tool/script
   - Update all examples to use new API

3. **v1.0.0 - Breaking Release**
   - Remove deprecated functions
   - Clean, modern API following Python best practices
   - Comprehensive migration guide

## Contributing

Have suggestions for the roadmap? 

1. Open an issue with your proposal
2. Include use case and rationale
3. Consider backward compatibility impact
4. Propose migration path if breaking change

---

**Note:** This roadmap is not a commitment and priorities may change based on user feedback and project needs.

## Version History

- **v0.1.0** (Current) - Initial packaged release with restructured codebase
- **Pre-packaging** - Single file utility copied between projects

