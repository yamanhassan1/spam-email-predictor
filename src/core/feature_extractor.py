"""
Feature extraction service for spam detection.
Extracts text, formatting, URL, and behavioral features.
"""
import re
import math
from collections import Counter
from typing import Dict, List, Set, Tuple

from .models import MessageFeatures


class FeatureExtractor:
    """Extract features from message text for spam detection."""
    
    # Common URL shorteners
    URL_SHORTENERS = {
        "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd",
        "buff.ly", "adf.ly", "bit.do", "lnkd.in", "db.tt", "qr.ae",
        "cur.lv", "ity.im", "q.gs", "po.st", "bc.vc", "twitthis.com",
        "u.to", "j.mp", "buzurl.com", "cutt.ly", "short.io", "rebrand.ly",
        "bl.ink", "short.link"
    }
    
    # Imperative verbs commonly used in spam
    IMPERATIVE_VERBS = {
        "click", "buy", "claim", "order", "register", "subscribe",
        "act", "call", "reply", "send", "verify", "confirm", "update",
        "unsubscribe", "open", "download", "install", "visit", "join"
    }
    
    # Urgency words
    URGENCY_WORDS = {
        "urgent", "immediately", "asap", "now", "limited", "hurry",
        "expire", "expires", "deadline", "last chance", "act now",
        "don't wait", "limited time", "only today", "final notice",
        "instant", "quick", "rush", "emergency", "today only", "ending soon"
    }
    
    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text."""
        pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.findall(pattern, text, re.IGNORECASE)
    
    def char_ngrams(self, text: str, n: int = 3) -> Counter:
        """Generate character n-grams."""
        text = text.lower().replace(" ", "")
        if len(text) < n:
            return Counter()
        return Counter(text[i:i + n] for i in range(len(text) - n + 1))
    
    def text_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text."""
        if not text:
            return 0.0
        
        counter = Counter(text.lower())
        total = len(text)
        
        entropy = -sum(
            (count / total) * math.log2(count / total)
            for count in counter.values()
        )
        
        return entropy
    
    def extract_features(
        self,
        raw_text: str,
        processed_words: List[str],
        spam_words_set: Set[str],
        ham_words_set: Set[str]
    ) -> MessageFeatures:
        """
        Extract all features from message text.
        
        Args:
            raw_text: Original message text
            processed_words: Preprocessed words
            spam_words_set: Set of known spam words
            ham_words_set: Set of known ham words
            
        Returns:
            MessageFeatures object
        """
        # Word tokenization for raw text
        words = re.findall(r"\b\w+\b", raw_text)
        word_count = len(words)
        char_count = len(raw_text)
        unique_words = set(w.lower() for w in words)
        
        # Text content features
        spam_keyword_count = sum(1 for w in unique_words if w in spam_words_set)
        ham_keyword_count = sum(1 for w in unique_words if w in ham_words_set)
        
        word_lengths = [len(w) for w in words if w]
        avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
        
        # Character n-grams
        char_trigrams = self.char_ngrams(raw_text, 3)
        char_ngram_count = len(char_trigrams)
        
        # Formatting features
        letters = [c for c in raw_text if c.isalpha()]
        alpha_count = len(letters)
        upper_count = sum(1 for c in raw_text if c.isupper())
        capital_ratio = upper_count / alpha_count if alpha_count else 0
        
        exclamation_count = raw_text.count("!")
        question_count = raw_text.count("?")
        special_chars = sum(1 for c in raw_text if c in "$@#%&*")
        all_caps_words = sum(1 for w in re.findall(r"\b[A-Z]+\b", raw_text) if len(w) > 1)
        
        # URL features
        urls = self.extract_urls(raw_text)
        url_count = len(urls)
        url_shortener_count = 0
        suspicious_ip_url_count = 0
        https_count = 0
        http_count = 0
        
        for url in urls:
            lower_url = url.lower()
            
            if any(short in lower_url for short in self.URL_SHORTENERS):
                url_shortener_count += 1
            
            if re.search(r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url):
                suspicious_ip_url_count += 1
            
            if lower_url.startswith("https://"):
                https_count += 1
            elif lower_url.startswith("http://"):
                http_count += 1
        
        # Structural features
        html_tags = bool(re.search(r"<[a-zA-Z][^>]*>", raw_text))
        hidden_or_colored = bool(
            re.search(r"style\s*=\s*[^>]*(display:\s*none|color:\s*#?[fF]{6})", raw_text, re.I)
            or re.search(r"color\s*:\s*#?[fF]{6}", raw_text, re.I)
        )
        
        # Statistical features
        entropy = self.text_entropy(raw_text)
        total_word_occurrences = len(processed_words)
        repeated_word_ratio = (
            1 - len(unique_words) / total_word_occurrences
            if total_word_occurrences else 0
        )
        
        # Behavioral indicators
        text_lower = raw_text.lower()
        imperative_count = sum(
            1 for verb in self.IMPERATIVE_VERBS
            if re.search(r"\b" + re.escape(verb) + r"\b", text_lower)
        )
        urgency_count = sum(
            1 for word in self.URGENCY_WORDS
            if re.search(r"\b" + re.escape(word) + r"\b", text_lower)
        )
        
        return MessageFeatures(
            word_count=word_count,
            char_count=char_count,
            unique_word_count=len(unique_words),
            spam_keyword_frequency=spam_keyword_count,
            ham_keyword_frequency=ham_keyword_count,
            avg_word_length=round(avg_word_length, 2),
            char_ngram_count=char_ngram_count,
            capital_letter_ratio=round(capital_ratio, 4),
            exclamation_count=exclamation_count,
            question_mark_count=question_count,
            special_char_count=special_chars,
            all_caps_word_count=all_caps_words,
            url_count=url_count,
            url_shortener_count=url_shortener_count,
            suspicious_ip_url_count=suspicious_ip_url_count,
            https_link_count=https_count,
            http_link_count=http_count,
            html_content_presence=html_tags,
            hidden_or_colored_text=hidden_or_colored,
            text_entropy=round(entropy, 4),
            repeated_word_ratio=round(repeated_word_ratio, 4),
            imperative_verb_count=imperative_count,
            urgency_word_count=urgency_count
        )
    
    def analyze_patterns(
        self,
        raw_text: str,
        processed_words: List[str],
        spam_words_set: Set[str],
        ham_words_set: Set[str]
    ) -> Tuple[Dict[str, bool], List[str], List[str]]:
        """
        Analyze spam patterns in message.
        
        Returns:
            Tuple of (spam_patterns, found_spam_words, found_ham_words)
        """
        # Detect spam patterns
        spam_patterns = {
            'Free/Freebie': bool(re.search(r'\bfree\b', raw_text, re.I)),
            'Win/Prize': bool(re.search(r'\b(win|won|prize|winner)\b', raw_text, re.I)),
            'Urgent': bool(re.search(r'\burgent\b', raw_text, re.I)),
            'Click Here': bool(re.search(r'\bclick\s+(here|now|link)\b', raw_text, re.I)),
            'Money/Cash': bool(re.search(r'\b(money|cash|\$\d+|dollar)\b', raw_text, re.I)),
            'Limited Time': bool(re.search(r'\b(limited|expires?|deadline)\b', raw_text, re.I)),
        }
        
        # Find spam and ham words
        found_spam = [w for w in processed_words if w in spam_words_set]
        found_ham = [w for w in processed_words if w in ham_words_set]
        
        return spam_patterns, found_spam, found_ham