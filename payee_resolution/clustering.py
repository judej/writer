from typing import List, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter
import numpy as np

class PayeeClusterer:
    """
    Uses TF-IDF and KMeans to cluster payee strings and identify common names.
    """
    def __init__(self, n_clusters: int = 5):
        self.vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.cluster_labels: Dict[int, str] = {}
        self.is_fitted = False
        self.max_distance_threshold = 0.8 # Tunable threshold for "belonging" to a cluster

    def fit(self, payees: List[str]):
        """
        Fits the clustering model on a list of raw payee strings.
        Determines a label for each cluster based on common substrings.
        """
        if not payees:
            return

        # Vectorize
        tfidf_matrix = self.vectorizer.fit_transform(payees)
        
        # Cluster
        # Adjust n_clusters if we have fewer samples than clusters
        n_samples = len(payees)
        if n_samples < self.kmeans.n_clusters:
            self.kmeans.n_clusters = max(1, n_samples // 2)
            
        self.kmeans.fit(tfidf_matrix)
        
        # Determine labels for each cluster
        labels = self.kmeans.labels_
        
        # Group payees by cluster
        cluster_groups = {i: [] for i in range(self.kmeans.n_clusters)}
        for payee, label in zip(payees, labels):
            cluster_groups[label].append(payee)
            
        # Assign a "real name" to each cluster
        for label_id, group in cluster_groups.items():
            self.cluster_labels[label_id] = self._derive_label(group)
            
        self.is_fitted = True

    def _derive_label(self, group: List[str]) -> str:
        """
        Derives a representative label for a cluster of strings.
        """
        if not group:
            return "Unknown"
        
        cleaned_group = []
        for p in group:
            # simple strip of digits and special chars to find core brand
            c = "".join([x for x in p if x.isalpha() or x.isspace()]).strip()
            cleaned_group.append(c)
            
        if not cleaned_group:
            return group[0]
            
        # Count occurrences
        counts = Counter(cleaned_group)
        most_common = counts.most_common(1)[0][0]
        
        return most_common.title()

    def predict(self, payee: str) -> Optional[str]:
        """
        Predicts the real name for a new payee string.
        Returns None if the input is too far from any cluster center.
        """
        if not self.is_fitted:
            return None
            
        if not payee or len(payee.strip()) < 2:
            return None
            
        # Transform input
        vec = self.vectorizer.transform([payee])
        
        # If the input contains no features (e.g. no matching n-grams), return None
        if vec.nnz == 0:
            return None
        
        # Get distances to all cluster centers
        distances = self.kmeans.transform(vec)
        
        # Find closest cluster
        nearest_cluster_idx = np.argmin(distances)
        min_dist = distances[0][nearest_cluster_idx]
        
        # Check threshold
        # In cosine distance (if normalized), distances are small. 
        # But sklearn KMeans uses Euclidean distance on TFIDF vectors.
        # Since TFIDF vectors are normalized, max euclidean distance between two is sqrt(2) ~ 1.414.
        # A distance of 0.8 is quite far.
        if min_dist > self.max_distance_threshold:
            return None
        
        return self.cluster_labels.get(nearest_cluster_idx)