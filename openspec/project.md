```markdown
# Project Context

## Purpose
AIoT Data Analysis and Machine Learning (HW3) - Building and comparing classification models to detect spam SMS and phishing emails. The project implements multiple ML algorithms and evaluates their effectiveness on real-world datasets.

## Tech Stack
- **Language**: Python 3.x
- **ML Frameworks**: scikit-learn, NLTK
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib
- **NLP**: TextBlob (lemmatization, tokenization)
- **Development Environment**: Jupyter Notebooks
- **Models Implemented**:
  - Bayesian Spam Detector (Naive Bayes)
  - Decision Tree Phishing Detector
  - Perceptron (binary classification)
  - Support Vector Machine (SVM)
  - Logistic Regression
  - Linear Regression

## Project Conventions

### Code Style
- Python 3 with PEP 8 conventions
- Jupyter Notebooks for exploratory and analytical work
- Shared utility functions in `sources/defs.py` (tokenization, visualization)
- Lemmatization via TextBlob for NLP preprocessing

### Architecture Patterns
- **Dataset-driven**: Multiple specialized datasets for different tasks (phishing, SMS spam)
- **Algorithm comparison**: Each notebook implements a distinct ML algorithm
- **Train-test split workflow**: Standard ML pipeline with data preprocessing, model training, and evaluation
- **Visualization**: Decision regions and model performance plots

### Testing Strategy
- Manual validation on test sets
- Model performance metrics (accuracy, precision, recall, F1)
- Decision boundary visualization for 2D feature spaces
- Cross-validation where applicable

### Git Workflow
- Feature-branch workflow per algorithm/model
- Commit messages: Descriptive with model/dataset context
- Dataset versioning: Separate CSV files for different preprocessing stages

## Domain Context
- **Spam Detection**: Binary classification of SMS messages (spam vs. ham)
- **Phishing Detection**: Binary classification of emails/messages (phishing vs. legitimate)
- **Text Preprocessing**: Lemmatization and tokenization using NLP techniques
- **Feature Engineering**: Converting text to numerical features for ML models
- **Model Selection**: Comparing multiple algorithms to find best fit for each domain

## Important Constraints
- Imbalanced datasets: Spam/phishing are minority class in real-world data
- Text preprocessing: Must handle lowercase, stopwords, and tokenization consistently
- Dataset size: Limited to CSV files in `datasets/` folder
- Jupyter environment: Models should be reproducible and runnable in notebook cells

## External Dependencies
- NLTK Corpus (for TextBlob)
- Scikit-learn pre-trained models
- Matplotlib/Seaborn for visualization

```
