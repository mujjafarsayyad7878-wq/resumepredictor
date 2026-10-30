"""
TF-IDF Vectorizer and Cosine Similarity Scoring Engine
Dual-Engine: Uses Scikit-learn if available, with a built-in mathematical vectorizer fallback.
"""
import math
from collections import Counter
from typing import List, Tuple, Dict, Any

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from app.nlp.preprocessor import clean_text, tokenize, extract_ngrams

class CustomTfidfEngine:
    """
    Mathematical TF-IDF implementation using sublinear term frequencies
    and smoothed inverse document frequencies.
    """
    def __init__(self, ngram_range: Tuple[int, int] = (1, 2)):
        self.ngram_range = ngram_range
        self.vocabulary_: Dict[str, int] = {}
        self.idf_: Dict[str, float] = {}

    def _get_doc_tokens(self, text: str) -> List[str]:
        tokens = tokenize(text, remove_stopwords=True)
        all_features = list(tokens)
        if self.ngram_range[1] >= 2:
            all_features.extend(extract_ngrams(tokens, 2))
        if self.ngram_range[1] >= 3:
            all_features.extend(extract_ngrams(tokens, 3))
        return all_features

    def fit_transform(self, raw_documents: List[str]) -> List[Dict[int, float]]:
        """
        Fits vocabulary and IDF weights on corpus, returns sparse TF-IDF vectors.
        """
        doc_token_lists = [self._get_doc_tokens(doc) for doc in raw_documents]
        n_docs = len(doc_token_lists)

        # Build vocabulary & document frequency
        df: Dict[str, int] = Counter()
        for doc_tokens in doc_token_lists:
            unique_terms = set(doc_tokens)
            for term in unique_terms:
                df[term] += 1

        # Build index mapping
        self.vocabulary_ = {term: idx for idx, term in enumerate(df.keys())}
        
        # Calculate smoothed IDF: log((1 + n) / (1 + df)) + 1
        self.idf_ = {}
        for term, freq in df.items():
            self.idf_[term] = math.log((1 + n_docs) / (1 + freq)) + 1.0

        # Transform documents
        vectors = []
        for doc_tokens in doc_token_lists:
            tf = Counter(doc_tokens)
            vec: Dict[int, float] = {}
            norm_sq = 0.0

            for term, count in tf.items():
                if term in self.vocabulary_:
                    idx = self.vocabulary_[term]
                    # Sublinear tf: 1 + log(tf)
                    val = (1.0 + math.log(count)) * self.idf_[term]
                    vec[idx] = val
                    norm_sq += val * val

            # L2 Normalization
            norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
            for idx in vec:
                vec[idx] /= norm

            vectors.append(vec)

        return vectors

    def transform(self, raw_documents: List[str]) -> List[Dict[int, float]]:
        """
        Transforms unseen documents using pre-fitted vocabulary and IDF.
        """
        vectors = []
        for doc in raw_documents:
            doc_tokens = self._get_doc_tokens(doc)
            tf = Counter(doc_tokens)
            vec: Dict[int, float] = {}
            norm_sq = 0.0

            for term, count in tf.items():
                if term in self.vocabulary_:
                    idx = self.vocabulary_[term]
                    val = (1.0 + math.log(count)) * self.idf_[term]
                    vec[idx] = val
                    norm_sq += val * val

            norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
            for idx in vec:
                vec[idx] /= norm

            vectors.append(vec)
        return vectors

    @staticmethod
    def cosine_similarity(vec1: Dict[int, float], vec2: Dict[int, float]) -> float:
        """
        Computes dot product between two L2-normalized sparse vectors.
        """
        common_indices = set(vec1.keys()) & set(vec2.keys())
        sim = sum(vec1[idx] * vec2[idx] for idx in common_indices)
        return max(0.0, min(1.0, float(sim)))

def compute_similarity(text1: str, text2: str) -> Dict[str, Any]:
    """
    Computes TF-IDF Cosine Similarity between Resume text and Job Description.
    Returns:
        - similarity_score: float in [0.0, 1.0]
        - percentage: float in [0.0, 100.0]
        - engine_used: 'scikit-learn' or 'custom-nlp'
    """
    clean_t1 = clean_text(text1)
    clean_t2 = clean_text(text2)

    if not clean_t1 or not clean_t2:
        return {"similarity_score": 0.0, "percentage": 0.0, "engine_used": "none"}

    if SKLEARN_AVAILABLE:
        try:
            vectorizer = TfidfVectorizer(
                ngram_range=(1, 2),
                stop_words='english',
                sublinear_tf=True
            )
            tfidf_matrix = vectorizer.fit_transform([clean_t1, clean_t2])
            score = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
            score = max(0.0, min(1.0, score))
            return {
                "similarity_score": round(score, 4),
                "percentage": round(score * 100, 2),
                "engine_used": "scikit-learn"
            }
        except Exception:
            pass

    # Mathematical Vectorizer
    engine = CustomTfidfEngine(ngram_range=(1, 2))
    vectors = engine.fit_transform([clean_t1, clean_t2])
    score = CustomTfidfEngine.cosine_similarity(vectors[0], vectors[1])
    
    return {
        "similarity_score": round(score, 4),
        "percentage": round(score * 100, 2),
        "engine_used": "custom-nlp-tfidf"
    }
