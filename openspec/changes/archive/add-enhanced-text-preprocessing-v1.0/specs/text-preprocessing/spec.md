# Specification: Text Preprocessing Capability

## Overview
This specification defines the text preprocessing capability for spam detection and phishing classification. The preprocessing module provides configurable, reusable functions for cleaning and normalizing text data before feature extraction.

## ADDED Requirements

### Requirement: Configurable Text Preprocessing
Provide a flexible, configuration-driven preprocessing system for text data.

#### Scenario: Create preprocessor with default configuration
```python
from sources.preprocessing import TextPreprocessor, PreprocessingConfig

# Default config: lowercase, remove punctuation, normalize whitespace
preprocessor = TextPreprocessor()
cleaned_text = preprocessor.process("Hello!!!  Visit https://example.com for more.")
# Output: "hello visit example com for more"
```

#### Scenario: Customize preprocessing steps
```python
config = PreprocessingConfig(
    lowercase=True,
    remove_urls=True,
    remove_emails=True,
    remove_punctuation=True,
    remove_numbers=False,
    remove_stopwords=True,
    normalize_whitespace=True
)
preprocessor = TextPreprocessor(config)
cleaned = preprocessor.process("Check email test@example.com or visit www.test.com 123-456")
# Removes URLs/emails and stopwords, keeps numbers
```

### Requirement: URL and Email Removal
Remove URLs and email addresses from text while preserving message content.

#### Scenario: Remove URLs from spam message
```python
preprocessor = TextPreprocessor()
text_with_urls = "Win free money! Click here: http://malicious.com/win NOW!!"
cleaned = preprocessor.remove_urls(text_with_urls)
# Output: "Win free money! Click here: NOW!!"
```

#### Scenario: Remove email addresses from phishing messages
```python
text_with_email = "Verify your account at support@bank.fake - contact us@fraud.net"
cleaned = preprocessor.remove_emails(text_with_email)
# Output: "Verify your account at - contact us"
```

### Requirement: Case Normalization
Convert text to lowercase with proper handling of special cases.

#### Scenario: Normalize mixed-case spam messages
```python
preprocessor = TextPreprocessor()
text = "URGENT: VERIFY Your PayPal Account!!!"
normalized = preprocessor.normalize_case(text)
# Output: "urgent: verify your paypal account!!!"
```

### Requirement: Punctuation and Special Character Handling
Remove or normalize punctuation and special characters.

#### Scenario: Remove punctuation from message
```python
preprocessor = TextPreprocessor()
text = "Hello!!! How are you??? (Very well, thank you.) @#$%"
cleaned = preprocessor.remove_punctuation(text)
# Output: "Hello How are you Very well thank you"
```

### Requirement: Stopword Removal
Optionally remove common English stopwords for improved feature extraction.

#### Scenario: Remove stopwords from SMS
```python
config = PreprocessingConfig(remove_stopwords=True)
preprocessor = TextPreprocessor(config)
text = "Click the link to win a free prize today"
cleaned = preprocessor.process(text)
# Output: "click link win free prize" (removed: the, to, a, today)
```

### Requirement: Whitespace Normalization
Clean excess whitespace and newlines from text.

#### Scenario: Normalize whitespace in multiline text
```python
preprocessor = TextPreprocessor()
text = "Hello    world\n\n\nTest   message"
normalized = preprocessor.normalize_whitespace(text)
# Output: "Hello world Test message"
```

### Requirement: Number Handling
Configurable handling of numbers (keep, remove, or replace with token).

#### Scenario: Remove numbers for text-only analysis
```python
config = PreprocessingConfig(remove_numbers=True)
preprocessor = TextPreprocessor(config)
text = "Call 555-1234 or order 100 items"
cleaned = preprocessor.process(text)
# Output: "call or order items"
```

#### Scenario: Keep numbers for analysis that includes quantity features
```python
config = PreprocessingConfig(remove_numbers=False)
preprocessor = TextPreprocessor(config)
text = "Order 100 items for $49.99"
cleaned = preprocessor.process(text)
# Output: "order 100 items for 4999"  # periods removed, numbers kept
```

### Requirement: Batch Processing
Efficiently preprocess multiple messages at once.

#### Scenario: Preprocess entire SMS dataset
```python
import pandas as pd
from sources.preprocessing import TextPreprocessor

df = pd.read_csv('../datasets/sms_spam_no_header.csv')
preprocessor = TextPreprocessor()
df['cleaned_text'] = df['text'].apply(preprocessor.process)
```

### Requirement: Backward Compatibility
Preserve existing preprocessing functions while enhancing capabilities.

#### Scenario: Existing code continues to work unchanged
```python
from sources.defs import get_lemmas, get_tokens

# Existing notebooks can use original functions
lemmas = get_lemmas("Hello world")  # Still works
tokens = get_tokens("Hello world")   # Still works
```

#### Scenario: Bridge function for gradual migration
```python
from sources.defs import preprocess_text

# New wrapper function
text = "Visit http://example.com NOW!!!"
cleaned = preprocess_text(text)  # Uses enhanced preprocessing
```

## MODIFIED Requirements

### Requirement: Enhanced Tokenization
Tokenization should work with cleaned text for better accuracy.

#### Current Behavior
```python
def get_lemmas(msg):
    # Works on raw text with punctuation, URLs, etc.
    return [word.lemma for word in TextBlob(str(msg)).words]
```

#### Improved Behavior
```python
def get_lemmas(msg):
    # Input is now expected to be preprocessed (lowercase, no URLs)
    # Produces better lemmas with fewer noise features
    return [word.lemma for word in TextBlob(str(msg)).words]
```

**Note**: Function signature unchanged, but behavior improves with preprocessed input.

## REMOVED Requirements
None (purely additive change)

## Acceptance Criteria
✅ All preprocessing functions tested with SMS spam and phishing datasets
✅ Output text is consistent (no spurious whitespace, predictable format)
✅ Backward compatibility maintained (existing `get_lemmas()`, `get_tokens()` work)
✅ Configuration system allows flexible preprocessing variations
✅ No performance degradation (< 5ms per message on modern hardware)
✅ Comprehensive docstrings with usage examples
✅ Unit test coverage > 85% for preprocessing module
