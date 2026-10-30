"""
Text Preprocessing and NLP Cleaning Utilities
Supports both English and Hindi text normalization, tokenization, and language detection.
"""
import re
from typing import List, Set

# Comprehensive English stopwords list
STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", 
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", 
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", 
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", 
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", 
    "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", 
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", 
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", 
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", 
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", 
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", 
    "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", 
    "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", 
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", 
    "yours", "yourself", "yourselves"
}

# Common Hindi stopwords (connecting particles, pronouns, auxiliaries)
HINDI_STOPWORDS: Set[str] = {
    "का", "के", "की", "को", "में", "से", "पर", "और", "या", "यह", "वह", "है", "हैं", "था", "थी", "थे",
    "होना", "करना", "किया", "लिए", "ने", "तक", "साथ", "भी", "तो", "ही", "एक", "इस", "उस", "अपने", "अपनी",
    "द्वारा", "गया", "गई", "गए", "रहा", "रही", "रहे", "सकते", "सकता", "सकती", "वाले", "वाली", "वाला"
}

def detect_language(text: str) -> str:
    """
    Detects whether the text is predominantly Hindi or English.
    Returns: 'hi' for Hindi, 'en' for English.
    """
    if not text:
        return "en"
    
    # Count Devanagari characters (\u0900 - \u097F)
    devanagari_count = len(re.findall(r'[\u0900-\u097F]', text))
    if devanagari_count >= 12:
        return "hi"
    
    # Look for Hindi resume keywords
    hindi_keywords = ["अनुभव", "कौशल", "शिक्षा", "प्रोजेक्ट", "परियोजना", "स्नातक", "वर्ष का अनुभव", "वेतन"]
    if any(kw in text for kw in hindi_keywords):
        return "hi"
    
    return "en"

def clean_text(text: str) -> str:
    """
    Cleans raw resume or job description text:
    - Normalizes unicode characters
    - Replaces bullet points and separators with spaces
    - Preserves crucial tech symbols like C++, C#, .NET, CI/CD, Node.js
    - Preserves Devanagari (Hindi) characters
    - Strips excess whitespace
    """
    if not text:
        return ""
    
    # Replace non-breaking spaces and fancy quotes
    text = text.replace('\xa0', ' ').replace('’', "'").replace('“', '"').replace('”', '"')
    
    # Normalize bullet characters
    text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219\*\-\–\—]', ' ', text)
    
    # Replace newlines and tabs with spaces
    text = re.sub(r'[\r\n\t]+', ' ', text)
    
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text: str, remove_stopwords: bool = True, min_len: int = 2) -> List[str]:
    """
    Tokenizes text while maintaining tech terminology (e.g., node.js, c++, scikit-learn)
    and Devanagari words.
    """
    text = clean_text(text).lower()
    
    # Regex to find word tokens in English and Devanagari
    tokens = re.findall(r'[a-zA-Z0-9\u0900-\u097F\+#\.]+(?:-[a-zA-Z0-9\u0900-\u097F\+#\.]+)*', text)
    
    cleaned_tokens = []
    for token in tokens:
        # Strip trailing punctuation except ++ and #
        token = token.strip(',.;:')
        if not token:
            continue
        if len(token) < min_len and token not in {"c", "r", "go", "js"}:
            continue
        if remove_stopwords and (token in STOPWORDS or token in HINDI_STOPWORDS):
            continue
        cleaned_tokens.append(token)
        
    return cleaned_tokens

def extract_ngrams(tokens: List[str], n: int = 2) -> List[str]:
    """
    Extracts n-grams for multi-word skill matching (e.g. 'machine learning', 'spring boot').
    """
    if len(tokens) < n:
        return []
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
