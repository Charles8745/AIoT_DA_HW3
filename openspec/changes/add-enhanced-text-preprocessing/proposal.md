# Change Proposal: Enhanced Text Preprocessing Pipeline

## Summary
Expand and standardize the text preprocessing capabilities in `sources/defs.py` to provide a comprehensive, reusable preprocessing pipeline for spam detection and phishing classification tasks. Currently, preprocessing is minimal and scattered across notebooks; this change centralizes and enhances it.

## Motivation
Current state:
- Only `get_lemmas()` and `get_tokens()` exist in `defs.py`
- Each notebook implements preprocessing ad-hoc (case conversion, train-test split, feature extraction)
- No standardized handling of: punctuation, special characters, URLs, numbers, stopwords
- No validation or configuration for preprocessing parameters
- Difficult to reproduce preprocessing across models and datasets

This change enables:
- **Consistency**: All models use identical preprocessing logic
- **Modularity**: Reusable preprocessing steps with configuration options
- **Quality**: Better feature engineering through enhanced text cleaning
- **Reproducibility**: Documented preprocessing pipelines that can be versioned
- **Maintainability**: Centralized code reduces duplication (~40% reduction in notebook preprocessing code)

## Scope

### New Preprocessing Capabilities
1. **Text Cleaning**: Remove/normalize punctuation, special characters, URLs, email addresses
2. **Case Normalization**: Lowercase conversion with edge-case handling
3. **Stopword Removal**: Optional removal of common English stopwords
4. **Number Handling**: Replace numbers with tokens or remove entirely
5. **Whitespace Normalization**: Clean excess spaces and newlines
6. **Character Filtering**: Remove control characters and non-ASCII characters (configurable)

### Integration Points
- `sources/preprocessing.py` (new module with TextPreprocessor class)
- Update `sources/defs.py` to import from preprocessing module
- No breaking changes to existing notebook interfaces

### Out of Scope (Future Enhancements)
- Stemming (beyond current lemmatization)
- Language detection
- Semantic preprocessing (paraphrasing, synonym expansion)
- GPU-accelerated preprocessing

## Impact Assessment
- **Scope**: Moderate (new module, updates to defs.py)
- **Breaking Changes**: None (existing functions remain)
- **Code Duplication Reduction**: ~35-40% in preprocessing code
- **Performance**: Minimal impact; single-pass preprocessing
- **Testing**: Add unit tests for each preprocessing function

## Success Criteria
✅ All preprocessing functions tested with both SMS spam and phishing datasets
✅ Backward compatible with existing notebooks
✅ Improvement in model accuracy or consistency due to better feature engineering
✅ All code follows project conventions from `openspec/project.md`
✅ Comprehensive documentation with usage examples

## Timeline & Effort
- Estimated effort: 2-3 hours
- No blocking dependencies

## Approval Status
- [x] Ready for review
- [x] Approved for implementation (2025-10-22)
- [x] Implementation completed (2025-10-22)
- [x] Archived (2025-10-22) - v1.0
