import re
from typing import List, Set

STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me",
    "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only",
    "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't",
    "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
    "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
    "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've",
    "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while",
    "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd",
    "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

def stem(word: str) -> str:
    """Lightweight rule-based suffix stemming."""
    w = word.lower()
    if len(w) <= 3:
        return w

    if w.endswith("sses"):
        w = w[:-2]
    elif w.endswith("ies"):
        w = w[:-2]
    elif w.endswith("ss"):
        pass
    elif w.endswith("s") and len(w) > 3:
        w = w[:-1]

    if w.endswith("ational"):
        w = w[:-5] + "e"
    elif w.endswith("tional"):
        w = w[:-2]
    elif w.endswith("ing") and len(w) > 4:
        w = w[:-3]
        if w.endswith("nn") or w.endswith("mm") or w.endswith("tt") or w.endswith("pp"):
            w = w[:-1]
    elif w.endswith("ed") and len(w) > 4:
        w = w[:-2]
        if w.endswith("nn") or w.endswith("mm") or w.endswith("tt") or w.endswith("pp"):
            w = w[:-1]
    elif w.endswith("ly") and len(w) > 4:
        w = w[:-2]
    elif w.endswith("ment") and len(w) > 5:
        w = w[:-4]
    elif w.endswith("ness") and len(w) > 5:
        w = w[:-4]

    return w

def tokenize(text: str, remove_stopwords: bool = True, apply_stem: bool = True) -> List[str]:
    """Tokenizes text into cleaned, stemmed terms."""
    if not text:
        return []

    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    result = []
    for w in words:
        if remove_stopwords and w in STOPWORDS:
            continue
        if len(w) < 2:
            continue
        token = stem(w) if apply_stem else w
        result.append(token)

    return result
