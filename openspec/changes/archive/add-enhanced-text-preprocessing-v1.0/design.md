# Design: Enhanced Text Preprocessing Pipeline

## Architecture Overview

```
sources/preprocessing.py (NEW)
├── TextPreprocessor (class)
│   ├── __init__(config: PreprocessingConfig)
│   ├── clean_text() → str
│   ├── normalize_case() → str
│   ├── remove_stopwords() → str
│   ├── process() → str (full pipeline)
│   └── batch_process() → List[str]
├── PreprocessingConfig (dataclass)
│   ├── lowercase: bool = True
│   ├── remove_punctuation: bool = True
│   ├── remove_urls: bool = True
│   ├── remove_emails: bool = True
│   ├── remove_numbers: bool = False
│   ├── remove_stopwords: bool = False
│   ├── normalize_whitespace: bool = True
│   └── remove_non_ascii: bool = True
├── Preprocessing Functions
│   ├── remove_urls()
│   ├── remove_emails()
│   ├── remove_punctuation()
│   ├── remove_numbers()
│   └── normalize_whitespace()
│
sources/defs.py (MODIFIED)
├── Import TextPreprocessor, PreprocessingConfig
├── keep get_tokens() (use preprocessed input)
├── keep get_lemmas() (use preprocessed input)
└── Add preprocess_text() wrapper for backward compatibility
```

## Key Design Decisions

### 1. Configuration-Driven Approach
- `PreprocessingConfig` dataclass allows flexible preprocessing pipelines
- Different tasks (spam vs. phishing) might need different preprocessing
- Enables A/B testing preprocessing variations

### 2. Processing Pipeline Order
```
Input Text
  ↓
1. URL/Email Removal
  ↓
2. Lowercase Normalization
  ↓
3. Punctuation/Special Character Removal
  ↓
4. Number Handling (remove or keep)
  ↓
5. Whitespace Normalization
  ↓
6. Stopword Removal (optional, after tokenization)
  ↓
Output Clean Text
```

**Rationale**: URL and email removal first (before case conversion to preserve patterns); stopwords last (requires tokenization).

### 3. Class-Based Design
- Encapsulate state (config, stopword lists) in TextPreprocessor
- Reusable across multiple documents in a batch
- Lazy-load NLTK stopwords to reduce startup time

### 4. Backward Compatibility
- Existing `get_lemmas()` and `get_tokens()` remain unchanged
- New `preprocess_text()` function acts as bridge
- Notebooks can incrementally adopt enhanced preprocessing

## Integration with Existing Code

### Before (Current)
```python
from defs import get_lemmas
bow = CountVectorizer(analyzer=get_lemmas).fit(text_train)
```

### After (Enhanced, Optional)
```python
from defs import preprocess_text, get_lemmas
from preprocessing import TextPreprocessor, PreprocessingConfig

# Option 1: Simple usage (backward compatible)
bow = CountVectorizer(analyzer=get_lemmas).fit(text_train)

# Option 2: Enhanced preprocessing
config = PreprocessingConfig(remove_urls=True, remove_stopwords=True)
preprocessor = TextPreprocessor(config)
preprocessed_text = [preprocessor.process(msg) for msg in text_train]
bow = CountVectorizer(analyzer=get_lemmas).fit(preprocessed_text)
```

## Testing Strategy

- Unit tests for each preprocessing function
- Integration tests with real SMS and phishing datasets
- Validation: ensure no data loss, consistent output format
- Performance benchmarks: measure preprocessing time per message

## Future Extensions

1. **Stemming Support**: Add Porter Stemmer or Snowball Stemmer
2. **Language Detection**: Handle multilingual text
3. **Custom Dictionaries**: Domain-specific stopword lists
4. **Caching**: Precompute frequent preprocessing operations
5. **Parallel Processing**: Batch-process large datasets with multiprocessing
