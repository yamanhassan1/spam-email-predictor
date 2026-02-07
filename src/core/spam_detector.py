"""
Spam detection service with proper OOP design.
Encapsulates model loading, prediction, and analysis logic.
"""
import pickle
import time
from pathlib import Path
from typing import Optional, List, Tuple, Set
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pandas as pd

from .models import (
    PredictionResult, 
    MessageType, 
    ConfidenceLevel,
    MessageFeatures,
    BatchAnalysisResult
)
from .feature_extractor import FeatureExtractor


class ModelLoadError(Exception):
    """Exception raised when model loading fails."""
    pass


class SpamDetectorService:
    """
    Main service class for spam detection.
    Handles model loading, preprocessing, and prediction.
    """
    
    def __init__(self, model_dir: Optional[Path] = None, data_dir: Optional[Path] = None):
        """
        Initialize spam detector service.
        
        Args:
            model_dir: Directory containing model files
            data_dir: Directory containing preprocessed data
        """
        self.model_dir = model_dir or self._get_default_model_dir()
        self.data_dir = data_dir or self._get_default_data_dir()
        
        # Initialize components
        self.vectorizer = None
        self.model = None
        self.spam_words: Set[str] = set()
        self.ham_words: Set[str] = set()
        self.stop_words: Set[str] = set()
        self.stemmer = PorterStemmer()
        self.feature_extractor = FeatureExtractor()
        
        # Load models and data
        self._initialize()
    
    def _get_default_model_dir(self) -> Path:
        """Get default model directory."""
        return Path(__file__).resolve().parent.parent.parent / "Models"
    
    def _get_default_data_dir(self) -> Path:
        """Get default data directory."""
        return Path(__file__).resolve().parent.parent.parent / "Data" / "preprocessed"
    
    def _initialize(self) -> None:
        """Initialize NLTK resources and load models."""
        # Setup NLTK
        try:
            nltk.download('stopwords', quiet=True)
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
        except Exception:
            pass
        
        # Load stopwords
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
        
        # Load models and word lists
        self._load_models()
        self._load_word_lists()
    
    def _load_models(self) -> None:
        """Load TF-IDF vectorizer and classifier."""
        vec_path = self.model_dir / "vectorizer.pkl"
        model_path = self.model_dir / "model.pkl"
        
        if not vec_path.exists() or not model_path.exists():
            raise ModelLoadError(
                f"Model files not found at {self.model_dir}. "
                f"Expected: {vec_path} and {model_path}"
            )
        
        try:
            with open(vec_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
        
        except Exception as e:
            raise ModelLoadError(f"Failed to load models: {str(e)}")
    
    def _load_word_lists(self) -> None:
        """Load spam and ham word lists."""
        spam_path = self.data_dir / "top_30_most_used_spam_words.csv"
        ham_path = self.data_dir / "top_30_most_used_ham_words.csv"
        
        try:
            if spam_path.exists():
                spam_df = pd.read_csv(spam_path)
                self.spam_words = set(spam_df['word'].str.lower())
        except Exception:
            self.spam_words = set()
        
        try:
            if ham_path.exists():
                ham_df = pd.read_csv(ham_path)
                self.ham_words = set(ham_df['word'].str.lower())
        except Exception:
            self.ham_words = set()
    
    def preprocess_text(self, text: str) -> Tuple[str, List[str]]:
        """
        Preprocess text: tokenize, remove stopwords, and stem.
        
        Args:
            text: Raw text message
            
        Returns:
            Tuple of (processed_text, word_list)
        """
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = nltk.word_tokenize(text)
        
        # Keep only alphanumeric words
        words = [w for w in tokens if w.isalnum()]
        
        # Remove stopwords
        words = [w for w in words if w not in self.stop_words]
        
        # Stem words
        words = [self.stemmer.stem(w) for w in words]
        
        # Join back to string
        processed_text = ' '.join(words)
        
        return processed_text, words
    
    def _get_confidence_level(self, confidence: float) -> ConfidenceLevel:
        """Determine confidence level from confidence score."""
        if confidence >= 95:
            return ConfidenceLevel.VERY_HIGH
        elif confidence >= 80:
            return ConfidenceLevel.HIGH
        elif confidence >= 60:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def predict(self, raw_text: str) -> PredictionResult:
        """
        Predict if message is spam or ham.
        
        Args:
            raw_text: Raw message text
            
        Returns:
            PredictionResult with classification and analysis
        """
        # Preprocess text
        processed_text, words = self.preprocess_text(raw_text)
        
        # Vectorize
        vector = self.vectorizer.transform([processed_text])
        
        # Predict
        prediction = self.model.predict(vector)[0]
        probabilities = self.model.predict_proba(vector)[0]
        
        # Calculate metrics
        ham_prob = probabilities[0] * 100
        spam_prob = probabilities[1] * 100
        confidence = max(probabilities) * 100
        
        # Determine message type
        message_type = MessageType.SPAM if prediction == 1 else MessageType.HAM
        confidence_level = self._get_confidence_level(confidence)
        
        # Extract features
        features = self.feature_extractor.extract_features(
            raw_text=raw_text,
            processed_words=words,
            spam_words_set=self.spam_words,
            ham_words_set=self.ham_words
        )
        
        # Analyze patterns
        spam_patterns, found_spam, found_ham = self.feature_extractor.analyze_patterns(
            raw_text=raw_text,
            processed_words=words,
            spam_words_set=self.spam_words,
            ham_words_set=self.ham_words
        )
        
        return PredictionResult(
            message_type=message_type,
            confidence=confidence,
            confidence_level=confidence_level,
            spam_probability=spam_prob,
            ham_probability=ham_prob,
            features=features,
            processed_text=processed_text,
            spam_patterns=spam_patterns,
            found_spam_words=found_spam,
            found_ham_words=found_ham
        )
    
    def predict_batch(self, messages: List[str]) -> BatchAnalysisResult:
        """
        Predict multiple messages in batch.
        
        Args:
            messages: List of raw message texts
            
        Returns:
            BatchAnalysisResult with aggregate statistics
        """
        start_time = time.time()
        
        results = []
        spam_count = 0
        total_confidence = 0.0
        
        for message in messages:
            result = self.predict(message)
            results.append(result)
            
            if result.is_spam:
                spam_count += 1
            
            total_confidence += result.confidence
        
        processing_time = time.time() - start_time
        total_messages = len(messages)
        ham_count = total_messages - spam_count
        avg_confidence = total_confidence / total_messages if total_messages > 0 else 0.0
        
        return BatchAnalysisResult(
            total_messages=total_messages,
            spam_count=spam_count,
            ham_count=ham_count,
            average_confidence=avg_confidence,
            results=results,
            processing_time=processing_time
        )
    
    def get_statistics(self) -> dict:
        """Get service statistics and model information."""
        return {
            "model_loaded": self.model is not None,
            "vectorizer_loaded": self.vectorizer is not None,
            "spam_words_count": len(self.spam_words),
            "ham_words_count": len(self.ham_words),
            "stop_words_count": len(self.stop_words),
            "model_dir": str(self.model_dir),
            "data_dir": str(self.data_dir)
        }