"""
Secure file handler for processing uploaded email files.
Supports .txt, .eml, .msg, .csv with proper validation and sanitization.
"""
import re
import io
import csv
import email
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass
from email import policy
from email.parser import BytesParser

from .models import FileUploadResult


class FileValidationError(Exception):
    """Custom exception for file validation errors."""
    pass


@dataclass
class FileConfig:
    """File upload configuration and limits."""
    MAX_FILE_SIZE_MB: int = 10
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
    MAX_MESSAGES_PER_FILE: int = 1000
    ALLOWED_EXTENSIONS: Tuple[str, ...] = ('.txt', '.eml', '.csv', '.msg')
    
    # Security patterns to detect malicious content
    SUSPICIOUS_PATTERNS: Tuple[str, ...] = (
        r'<script[\s\S]*?>',  # JavaScript
        r'javascript:',  # JavaScript URLs
        r'data:text/html',  # Data URIs
        r'on\w+\s*=',  # Event handlers
    )


class SecureFileHandler:
    """
    Secure handler for processing uploaded message files.
    Implements validation, sanitization, and extraction.
    """
    
    def __init__(self, config: Optional[FileConfig] = None):
        """Initialize with optional custom configuration."""
        self.config = config or FileConfig()
    
    def validate_file(self, uploaded_file) -> None:
        """
        Validate uploaded file for security and compliance.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Raises:
            FileValidationError: If validation fails
        """
        # Check file exists
        if uploaded_file is None:
            raise FileValidationError("No file provided")
        
        # Check file size
        file_size = uploaded_file.size
        if file_size == 0:
            raise FileValidationError("File is empty")
        
        if file_size > self.config.MAX_FILE_SIZE_BYTES:
            raise FileValidationError(
                f"File too large. Maximum size: {self.config.MAX_FILE_SIZE_MB}MB"
            )
        
        # Check file extension
        filename = uploaded_file.name.lower()
        if not any(filename.endswith(ext) for ext in self.config.ALLOWED_EXTENSIONS):
            allowed = ', '.join(self.config.ALLOWED_EXTENSIONS)
            raise FileValidationError(
                f"Invalid file type. Allowed: {allowed}"
            )
    
    def sanitize_text(self, text: str) -> str:
        """
        Sanitize text content by removing potentially malicious code.
        
        Args:
            text: Raw text content
            
        Returns:
            Sanitized text
        """
        # Remove suspicious patterns
        for pattern in self.config.SUSPICIOUS_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Remove null bytes and control characters (except newlines/tabs)
        text = ''.join(char for char in text if char.isprintable() or char in '\n\t\r')
        
        # Limit text length per message
        max_length = 50000
        if len(text) > max_length:
            text = text[:max_length]
        
        return text.strip()
    
    def extract_from_txt(self, content: bytes) -> List[str]:
        """
        Extract messages from plain text file.
        Each line or paragraph is treated as a separate message.
        
        Args:
            content: File content bytes
            
        Returns:
            List of extracted messages
        """
        try:
            text = content.decode('utf-8', errors='ignore')
        except Exception:
            text = content.decode('latin-1', errors='ignore')
        
        # Split by double newlines (paragraphs) or single newlines
        messages = []
        
        # Try paragraph splitting first
        paragraphs = text.split('\n\n')
        if len(paragraphs) > 1:
            messages = [self.sanitize_text(p) for p in paragraphs if p.strip()]
        else:
            # Fall back to line splitting
            lines = text.split('\n')
            messages = [self.sanitize_text(line) for line in lines if line.strip()]
        
        return [msg for msg in messages if len(msg) > 10][:self.config.MAX_MESSAGES_PER_FILE]
    
    def extract_from_eml(self, content: bytes) -> List[str]:
        """
        Extract message content from .eml email file.
        
        Args:
            content: File content bytes
            
        Returns:
            List containing the email body
        """
        try:
            msg = BytesParser(policy=policy.default).parsebytes(content)
            
            # Extract text content
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        try:
                            body = part.get_content()
                            break
                        except Exception:
                            continue
            else:
                try:
                    body = msg.get_content()
                except Exception:
                    body = str(msg.get_payload(decode=True), errors='ignore')
            
            sanitized = self.sanitize_text(body)
            return [sanitized] if sanitized and len(sanitized) > 10 else []
        
        except Exception as e:
            raise FileValidationError(f"Failed to parse .eml file: {str(e)}")
    
    def extract_from_csv(self, content: bytes) -> List[str]:
        """
        Extract messages from CSV file.
        Assumes messages are in a column named 'message', 'text', 'content', or 'body'.
        
        Args:
            content: File content bytes
            
        Returns:
            List of extracted messages
        """
        try:
            text = content.decode('utf-8', errors='ignore')
            reader = csv.DictReader(io.StringIO(text))
            
            # Find the message column
            fieldnames = reader.fieldnames or []
            message_column = None
            
            for col in ['message', 'text', 'content', 'body', 'email']:
                if col in [f.lower() for f in fieldnames]:
                    message_column = next(
                        f for f in fieldnames if f.lower() == col
                    )
                    break
            
            if not message_column:
                raise FileValidationError(
                    "CSV must have a column named 'message', 'text', 'content', or 'body'"
                )
            
            messages = []
            for row in reader:
                msg = row.get(message_column, '').strip()
                if msg and len(msg) > 10:
                    messages.append(self.sanitize_text(msg))
                
                if len(messages) >= self.config.MAX_MESSAGES_PER_FILE:
                    break
            
            return messages
        
        except UnicodeDecodeError:
            raise FileValidationError("Invalid CSV encoding. Please use UTF-8.")
        except Exception as e:
            raise FileValidationError(f"Failed to parse CSV: {str(e)}")
    
    def process_file(self, uploaded_file) -> FileUploadResult:
        """
        Process uploaded file and extract messages.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            FileUploadResult with extraction details
        """
        try:
            # Validate file
            self.validate_file(uploaded_file)
            
            # Read file content
            content = uploaded_file.read()
            filename = uploaded_file.name
            file_ext = Path(filename).suffix.lower()
            
            # Extract messages based on file type
            messages = []
            
            if file_ext == '.txt':
                messages = self.extract_from_txt(content)
            elif file_ext == '.eml':
                messages = self.extract_from_eml(content)
            elif file_ext == '.csv':
                messages = self.extract_from_csv(content)
            elif file_ext == '.msg':
                # .msg files require special handling (Outlook format)
                # For now, treat as text
                messages = self.extract_from_txt(content)
            else:
                raise FileValidationError(f"Unsupported file type: {file_ext}")
            
            return FileUploadResult(
                filename=filename,
                file_type=file_ext,
                messages_extracted=len(messages),
                success=True,
                extracted_messages=messages
            )
        
        except FileValidationError as e:
            return FileUploadResult(
                filename=uploaded_file.name if uploaded_file else "unknown",
                file_type="unknown",
                messages_extracted=0,
                success=False,
                error_message=str(e)
            )
        except Exception as e:
            return FileUploadResult(
                filename=uploaded_file.name if uploaded_file else "unknown",
                file_type="unknown",
                messages_extracted=0,
                success=False,
                error_message=f"Unexpected error: {str(e)}"
            )
    
    def process_multiple_files(self, uploaded_files: List) -> List[FileUploadResult]:
        """
        Process multiple uploaded files.
        
        Args:
            uploaded_files: List of Streamlit UploadedFile objects
            
        Returns:
            List of FileUploadResult objects
        """
        results = []
        
        for uploaded_file in uploaded_files:
            result = self.process_file(uploaded_file)
            results.append(result)
        
        return results