# Tasks: Enhanced Text Preprocessing Pipeline

Implementation checklist for the preprocessing enhancement project.

## Phase 1: Core Module Setup

- [ ] Create `sources/preprocessing.py` module
- [ ] Define `PreprocessingConfig` dataclass with all configuration options
- [ ] Create `TextPreprocessor` class with `__init__` method
- [ ] Write module docstring with architecture overview
- [ ] Set up imports (re, NLTK, TextBlob)

## Phase 2: Basic Preprocessing Functions

- [ ] Implement `remove_urls()` - use regex to match http/https URLs
- [ ] Implement `remove_emails()` - use regex for email addresses
- [ ] Implement `normalize_case()` - convert to lowercase
- [ ] Implement `remove_punctuation()` - remove or normalize punctuation marks
- [ ] Implement `normalize_whitespace()` - clean excess spaces/newlines
- [ ] Implement `remove_non_ascii()` - optional filter for non-ASCII characters
- [ ] Implement `remove_numbers()` - remove or keep digits based on config

## Phase 3: Stopword Handling

- [ ] Lazy-load NLTK English stopwords in TextPreprocessor
- [ ] Implement `remove_stopwords()` method
- [ ] Handle edge case: stopword removal after tokenization
- [ ] Add configuration option to enable/disable stopword removal

## Phase 4: Pipeline and Batch Processing

- [ ] Implement `process()` method - orchestrate full preprocessing pipeline
- [ ] Document processing order in docstring
- [ ] Implement `batch_process()` method for list of texts
- [ ] Add validation for input types (string handling)
- [ ] Test pipeline order on sample texts from both datasets

## Phase 5: Backward Compatibility and Integration

- [ ] Update `sources/defs.py` imports to include preprocessing module
- [ ] Create `preprocess_text()` wrapper function in `defs.py`
- [ ] Verify existing `get_lemmas()` and `get_tokens()` still work
- [ ] Test with original notebook code to ensure no breakage
- [ ] Add docstring examples to `defs.py` showing new preprocessing

## Phase 6: Testing

- [ ] Write unit tests for each preprocessing function in `tests/test_preprocessing.py`
- [ ] Test with SMS spam dataset samples (various message types)
- [ ] Test with phishing email dataset samples
- [ ] Test edge cases: empty strings, special characters, multilingual text
- [ ] Validate output format consistency (no spurious whitespace)
- [ ] Benchmark preprocessing speed (should be < 5ms per message)
- [ ] Achieve > 85% code coverage for preprocessing module

## Phase 7: Notebook Integration (Optional - Phase 1 only)

- [ ] Update "Bayesian Spam Detector with Nltk.ipynb" to demonstrate new preprocessing
- [ ] Add example cell showing PreprocessingConfig usage
- [ ] Document which preprocessing settings work best for SMS spam
- [ ] Verify model performance with enhanced preprocessing
- [ ] Add markdown cell explaining preprocessing enhancements

## Phase 8: Documentation and Examples

- [ ] Create usage examples in docstrings (at least 3 per function)
- [ ] Add README section explaining TextPreprocessor
- [ ] Create quick-start guide: "How to use enhanced preprocessing"
- [ ] Document configuration options and their effects
- [ ] Add performance characteristics (timing, memory usage)

## Phase 9: Validation and Finalization

- [ ] Run full test suite: `pytest tests/test_preprocessing.py -v`
- [ ] Validate no regression in existing notebook execution
- [ ] Verify backward compatibility with original `get_lemmas()` calls
- [ ] Document any breaking changes (if any)
- [ ] Create final integration test combining preprocessing + model training
- [ ] Mark all tasks complete once validated

---

## Implementation Notes

### Dependencies to Install
- Already available: pandas, numpy, matplotlib, sklearn, textblob
- Need to verify: NLTK stopwords corpus (`nltk.download('stopwords')`)
- No new external packages required

### Key Testing Scenarios
1. **SMS Spam**: "Win FREE money NOW!!! Visit http://spam.com (555) 123-4567"
2. **Phishing Email**: "Urgent: Verify your account at http://fake-bank.com - contact@phishing.net"
3. **Normal Messages**: "Hi, how are you today? Let's meet at 3:30 PM"
4. **Edge Cases**: Empty string, only numbers, only punctuation, URLs without protocol

### Performance Target
- Single message: < 5ms (lemmatization not included, only preprocessing)
- Batch of 1000: < 5 seconds
- Scalability: Linear with message count

### Quality Metrics
- Unit test coverage: > 85%
- All docstrings complete with parameter descriptions
- Example code in all major functions
- No warnings from linting tools

---

## Definition of Done (DoD)

✅ All tasks completed and marked with `[x]`
✅ All unit tests passing with > 85% coverage
✅ No regression in existing notebook functionality
✅ Backward compatibility verified
✅ Code follows project conventions (openspec/project.md)
✅ Comprehensive documentation and examples
✅ Ready for integration into main notebooks
