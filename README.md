# Email/SMS Spam Detector

A machine learning-based web application that classifies emails and SMS messages as spam or ham (not spam) using Natural Language Processing (NLP) and Naive Bayes classification.

## 🌐 Live Demo

**Try the app online**: [https://spam-email-predictor-app.streamlit.app/](https://spam-email-predictor-app.streamlit.app/)

## 🚀 Features

- **Real-time Spam Detection**: Classify messages instantly using a pre-trained machine learning model
- **User-friendly Interface**: Simple and intuitive Streamlit web application
- **NLP-based Preprocessing**: Advanced text processing including tokenization, stop word removal, and stemming
- **TF-IDF Vectorization**: Efficient text feature extraction using Term Frequency-Inverse Document Frequency
- **Naive Bayes Classifier**: Probabilistic machine learning model trained for spam detection

## 📁 Project Structure

```
Email Spam Detector/
│
your-project/
├── app.py
│
├── Models/
│   ├── model.pkl                  # Trained Naive Bayes model
│   └── vectorizer.pkl             # TF-IDF vectorizer
│
└── Notebooks/
│    ├── EDA_and_Experiments.ipynb  # Exploratory Data Analysis
│    ├── preprocessing.ipynb        # Data preprocessing pipeline
│    └── Model_Building.ipynb       # Model training and evaluation
├── Data/
│   └── preprocessed/
│       ├── top_30_most_used_spam_words.csv
│       └── top_30_most_used_ham_words.csv
└── src/
    ├── __init__.py
    ├── design.py
    ├── model.py
    ├── nlp.py
    ├── analysis.py
    ├── features.py
    ├── visualization.py          ✅ Uses: probability_bar, top_words_bar, characters_pie
    ├── components/
    │   ├── __init__.py
    │   ├── input_section.py      ✅ UPDATED - File upload + tabs
    │   ├── pattern_analysis.py   ✅ Required
    │   └── feature_analysis.py   ✅ Required
    └── pages/
        ├── __init__.py
        ├── home.py                ✅ UPDATED - Batch processing + correct imports
        ├── about.py
        ├── help.py
        ├── contact.py
        └── info_section.py
```

## 🛠️ Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd "Email Spam Detector"
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements
   ```

3. **Download NLTK data** (required for text processing):
   ```python
   import nltk
   nltk.download('stopwords')
   nltk.download('punkt')
   ```

## 📦 Dependencies

- `streamlit==1.30.0` - Web application framework
- `nltk==3.9.1` - Natural Language Processing library
- `pandas==2.1.0` - Data manipulation and analysis
- `scikit-learn==1.3.0` - Machine learning library

## 🚀 Usage

1. **Start the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

3. **Enter a message** in the text area and click "Predict" to classify it as spam or not spam

## 🔧 How It Works

### 1. Text Preprocessing
The application preprocesses input text through the following steps:
- **Lowercasing**: Converts all text to lowercase
- **Tokenization**: Splits text into individual words
- **Special Character Removal**: Removes non-alphanumeric characters
- **Stop Word Removal**: Eliminates common words (e.g., "the", "is", "and")
- **Stemming**: Reduces words to their root form using Porter Stemmer

### 2. Feature Extraction
- **TF-IDF Vectorization**: Converts preprocessed text into numerical features using Term Frequency-Inverse Document Frequency

### 3. Classification
- **Naive Bayes Model**: The trained model predicts whether the message is spam (1) or ham (0)

## 📊 Model Development

The project includes Jupyter notebooks for the complete machine learning pipeline:

- **`EDA_and_Experiments.ipynb`**: Exploratory data analysis and experiments
- **`preprocessing.ipynb`**: Data cleaning and text transformation pipeline
- **`Model_Building.ipynb`**: Model training, evaluation, and selection

### Model Training Process:
1. Load and clean the raw dataset
2. Preprocess text data (lowercase, tokenize, remove stop words, stem)
3. Split data into training and testing sets (80/20)
4. Vectorize text using TF-IDF
5. Train Naive Bayes classifier (MultinomialNB)
6. Evaluate model performance
7. Save trained model and vectorizer for deployment

## 📝 Notes

- The pre-trained models (`model.pkl` and `vectorizer.pkl`) must be present in the `Models/` directory for the application to work
- Ensure all dependencies are installed before running the application
- The model was trained on a specific dataset; performance may vary with different message styles or languages

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available for educational purposes.

---

**Built with ❤️ using Python, Streamlit, NLTK, and scikit-learn**
