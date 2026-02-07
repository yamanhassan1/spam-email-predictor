"""
Core models for spam detection with proper OOP design.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime


class MessageType(Enum):
    """Message classification types."""
    SPAM = "spam"
    HAM = "ham"
    UNKNOWN = "unknown"


class ConfidenceLevel(Enum):
    """Confidence level categorization."""
    VERY_HIGH = "very_high"  # >= 95%
    HIGH = "high"  # >= 80%
    MEDIUM = "medium"  # >= 60%
    LOW = "low"  # < 60%


@dataclass
class MessageFeatures:
    """Extracted features from a message."""
    # Text content features
    word_count: int = 0
    char_count: int = 0
    unique_word_count: int = 0
    spam_keyword_frequency: int = 0
    ham_keyword_frequency: int = 0
    avg_word_length: float = 0.0
    char_ngram_count: int = 0
    
    # Formatting features
    capital_letter_ratio: float = 0.0
    exclamation_count: int = 0
    question_mark_count: int = 0
    special_char_count: int = 0
    all_caps_word_count: int = 0
    
    # URL features
    url_count: int = 0
    url_shortener_count: int = 0
    suspicious_ip_url_count: int = 0
    https_link_count: int = 0
    http_link_count: int = 0
    
    # Structural features
    html_content_presence: bool = False
    hidden_or_colored_text: bool = False
    
    # Statistical features
    text_entropy: float = 0.0
    repeated_word_ratio: float = 0.0
    
    # Behavioral indicators
    imperative_verb_count: int = 0
    urgency_word_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class PredictionResult:
    """Spam detection prediction result."""
    message_type: MessageType
    confidence: float  # 0-100
    confidence_level: ConfidenceLevel
    spam_probability: float  # 0-100
    ham_probability: float  # 0-100
    features: MessageFeatures
    processed_text: str
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    
    # Pattern analysis
    spam_patterns: Dict[str, bool] = field(default_factory=dict)
    found_spam_words: List[str] = field(default_factory=list)
    found_ham_words: List[str] = field(default_factory=list)
    
    @property
    def is_spam(self) -> bool:
        """Check if message is classified as spam."""
        return self.message_type == MessageType.SPAM
    
    @property
    def confidence_percentage(self) -> str:
        """Get formatted confidence percentage."""
        return f"{self.confidence:.2f}%"
    
    def get_risk_level(self) -> str:
        """Get risk level description."""
        if not self.is_spam:
            return "Safe"
        
        if self.confidence >= 95:
            return "Critical Risk"
        elif self.confidence >= 80:
            return "High Risk"
        elif self.confidence >= 60:
            return "Medium Risk"
        else:
            return "Low Risk"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "message_type": self.message_type.value,
            "confidence": self.confidence,
            "confidence_level": self.confidence_level.value,
            "spam_probability": self.spam_probability,
            "ham_probability": self.ham_probability,
            "is_spam": self.is_spam,
            "risk_level": self.get_risk_level(),
            "features": self.features.to_dict(),
            "processed_text": self.processed_text,
            "timestamp": self.analysis_timestamp.isoformat(),
            "spam_patterns": self.spam_patterns,
            "found_spam_words": self.found_spam_words,
            "found_ham_words": self.found_ham_words
        }


@dataclass
class BatchAnalysisResult:
    """Result from batch message analysis."""
    total_messages: int
    spam_count: int
    ham_count: int
    average_confidence: float
    results: List[PredictionResult] = field(default_factory=list)
    processing_time: float = 0.0
    
    @property
    def spam_percentage(self) -> float:
        """Get percentage of spam messages."""
        if self.total_messages == 0:
            return 0.0
        return (self.spam_count / self.total_messages) * 100
    
    @property
    def ham_percentage(self) -> float:
        """Get percentage of ham messages."""
        if self.total_messages == 0:
            return 0.0
        return (self.ham_count / self.total_messages) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_messages": self.total_messages,
            "spam_count": self.spam_count,
            "ham_count": self.ham_count,
            "spam_percentage": self.spam_percentage,
            "ham_percentage": self.ham_percentage,
            "average_confidence": self.average_confidence,
            "processing_time": self.processing_time,
            "results": [r.to_dict() for r in self.results]
        }


@dataclass
class FileUploadResult:
    """Result from file upload processing."""
    filename: str
    file_type: str
    messages_extracted: int
    success: bool
    error_message: Optional[str] = None
    extracted_messages: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "filename": self.filename,
            "file_type": self.file_type,
            "messages_extracted": self.messages_extracted,
            "success": self.success,
            "error_message": self.error_message,
            "extracted_messages": self.extracted_messages
        }