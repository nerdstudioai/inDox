# # import warnings
# # from loguru import logger
# # import sys
# # import pickle
# # import os

# # warnings.filterwarnings("ignore")

# # # Set up logging
# # logger.remove()
# # logger.add(
# #     sys.stdout, format="<green>{level}</green>: <level>{message}</level>", level="INFO"
# # )
# # logger.add(
# #     sys.stdout, format="<red>{level}</red>: <level>{message}</level>", level="ERROR"
# # )


# # class KVCache:
# #     """
# #     Key-Value Cache for storing and managing preloaded knowledge.
# #     """

# #     def __init__(self, cache_dir="kv_cache"):
# #         """
# #         Initialize the cache with a directory for storing precomputed KV pairs.
# #         """
# #         self.cache_dir = cache_dir
# #         if not os.path.exists(self.cache_dir):
# #             os.makedirs(self.cache_dir)

# #     def save_cache(self, key, kv_data):
# #         """
# #         Save KV cache to disk.

# #         Args:
# #             key (str): The cache key.
# #             kv_data (object): The data to save.
# #         """
# #         filepath = os.path.join(self.cache_dir, f"{key}.pkl")
# #         with open(filepath, "wb") as f:
# #             pickle.dump(kv_data, f)
# #         logger.info(f"KV cache saved: {filepath}")

# #     def load_cache(self, key):
# #         """
# #         Load KV cache from disk.

# #         Args:
# #             key (str): The cache key.

# #         Returns:
# #             object: The loaded KV cache data.
# #         """
# #         filepath = os.path.join(self.cache_dir, f"{key}.pkl")
# #         if os.path.exists(filepath):
# #             with open(filepath, "rb") as f:
# #                 kv_data = pickle.load(f)
# #             logger.info(f"KV cache loaded: {filepath}")
# #             return kv_data
# #         else:
# #             logger.warning(f"KV cache not found for key: {key}")
# #             return None

# #     def reset_cache(self):
# #         """
# #         Clear the cache directory.
# #         """
# #         for filename in os.listdir(self.cache_dir):
# #             filepath = os.path.join(self.cache_dir, filename)
# #             os.remove(filepath)
# #         logger.info("KV cache reset successfully")


# # class CAG:
# #     """
# #     Cache-Augmented Generation Pipeline.
# #     """

# #     def __init__(self, llm, embedding_model, cache: KVCache, max_tokens=128000):
# #         """
# #         Initialize the CAG pipeline.

# #         Args:
# #             llm (object): The LLM instance.
# #             embedding_model (object): The embedding model instance.
# #             cache (KVCache): The KV cache instance.
# #             max_tokens (int): The maximum tokens for the LLM context.
# #         """
# #         self.llm = llm
# #         self.embedding_model = embedding_model
# #         self.cache = cache
# #         self.max_tokens = max_tokens
# #         self.loaded_kv_cache = None

# #     def preload_documents(self, documents, cache_key):
# #         """
# #         Precompute the KV cache from documents and save it.

# #         Args:
# #             documents (list of str): The documents to preload.
# #             cache_key (str): The key for the KV cache.
# #         """
# #         logger.info(f"Precomputing KV cache for {len(documents)} documents...")
# #         try:
# #             kv_cache = self.embedding_model.embed_documents(documents)
# #             self.cache.save_cache(cache_key, kv_cache)
# #             logger.info(f"Preloaded {len(documents)} documents into KV cache.")
# #         except Exception as e:
# #             logger.error(f"Error during KV cache preloading: {e}")
# #             raise

# #     def inference(self, query, cache_key):
# #         """
# #         Perform inference using the precomputed KV cache and a query.

# #         Args:
# #             query (str): The query to answer.
# #             cache_key (str): The key for the KV cache.

# #         Returns:
# #             str: The generated response.
# #         """
# #         if not self.loaded_kv_cache:
# #             logger.info(f"Loading KV cache for key: {cache_key}")
# #             self.loaded_kv_cache = self.cache.load_cache(cache_key)

# #         if not self.loaded_kv_cache:
# #             logger.error("KV cache is not loaded. Please preload the documents first.")
# #             raise RuntimeError("KV cache missing or not loaded.")

# #         try:
# #             # Generate query embedding
# #             logger.info("Generating query embedding...")
# #             query_embedding = self.embedding_model.embed_query(query)

# #             # Perform inference with the LLM
# #             logger.info("Performing inference with preloaded KV cache...")
# #             response = self.llm.answer_question(
# #                 context=self.loaded_kv_cache, question=query
# #             )
# #             return response
# #         except Exception as e:
# #             logger.error(f"Error during inference: {e}")
# #             raise

# #     def reset_session(self):
# #         """
# #         Reset the session by clearing the loaded KV cache.
# #         """
# #         logger.info("Resetting session and clearing loaded KV cache...")
# #         self.loaded_kv_cache = None

# import warnings
# from loguru import logger
# import sys
# import pickle
# import os
# import numpy as np
# from typing import List, Dict, Any

# warnings.filterwarnings("ignore")

# # Set up logging
# logger.remove()
# logger.add(
#     sys.stdout, format="<green>{level}</green>: <level>{message}</level>", level="INFO"
# )
# logger.add(
#     sys.stdout, format="<red>{level}</red>: <level>{message}</level>", level="ERROR"
# )


# class KVCache:
#     """
#     Key-Value Cache for storing and managing preloaded knowledge.
#     """

#     def __init__(self, cache_dir="kv_cache"):
#         self.cache_dir = cache_dir
#         if not os.path.exists(self.cache_dir):
#             os.makedirs(self.cache_dir)

#     def save_cache(self, key, kv_data):
#         filepath = os.path.join(self.cache_dir, f"{key}.pkl")
#         with open(filepath, "wb") as f:
#             pickle.dump(kv_data, f)
#         logger.info(f"KV cache saved: {filepath}")

#     def load_cache(self, key):
#         filepath = os.path.join(self.cache_dir, f"{key}.pkl")
#         if os.path.exists(filepath):
#             with open(filepath, "rb") as f:
#                 kv_data = pickle.load(f)
#             logger.info(f"KV cache loaded: {filepath}")
#             return kv_data
#         else:
#             logger.warning(f"KV cache not found for key: {key}")
#             return None

#     def reset_cache(self):
#         for filename in os.listdir(self.cache_dir):
#             filepath = os.path.join(self.cache_dir, filename)
#             os.remove(filepath)
#         logger.info("KV cache reset successfully")


# class CacheEntry:
#     """
#     Structure to hold both text content and its embedding.
#     """

#     def __init__(self, text: str, embedding: np.ndarray):
#         self.text = text
#         self.embedding = embedding


# class CAG:
#     """
#     Cache-Augmented Generation Pipeline with semantic search.
#     """

#     def __init__(
#         self,
#         llm,
#         embedding_model,
#         cache: KVCache,
#         # top_k: int = 5,
#         # similarity_threshold: float = 0.5,
#     ):
#         """
#         Initialize the CAG pipeline.

#         Args:
#             llm: The LLM instance
#             embedding_model: The embedding model instance
#             cache (KVCache): The KV cache instance
#             top_k (int): Number of most similar chunks to retrieve
#             similarity_threshold (float): Minimum similarity score (0-1) for inclusion
#         """
#         self.llm = llm
#         self.embedding_model = embedding_model
#         self.cache = cache
#         self.loaded_kv_cache = None
#         # self.top_k = top_k
#         # self.similarity_threshold = similarity_threshold

#     def compute_similarity(
#         self, query_embedding: np.ndarray, doc_embedding: np.ndarray
#     ) -> float:
#         """
#         Compute cosine similarity between query and document embeddings.
#         """
#         return np.dot(query_embedding, doc_embedding) / (
#             np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
#         )

#     def get_relevant_context(
#         self, query_embedding: np.ndarray, cache_entries: List[CacheEntry]
#     ) -> List[str]:
#         """
#         Retrieve most relevant context chunks based on semantic similarity.
#         """
#         similarities = [
#             (entry, self.compute_similarity(query_embedding, entry.embedding))
#             for entry in cache_entries
#         ]

#         # Sort by similarity score
#         similarities.sort(key=lambda x: x[1], reverse=True)

#         # Filter by threshold and take top k
#         relevant_chunks = [
#             entry.text
#             for entry, score in similarities[: self.top_k]
#             if score >= self.similarity_threshold
#         ]

#         logger.info(f"Selected {len(relevant_chunks)} relevant chunks from cache")

#         # Log similarity scores for debugging
#         for i, (entry, score) in enumerate(similarities[: self.top_k]):
#             logger.debug(f"Chunk {i+1} similarity score: {score:.3f}")

#         return relevant_chunks

#     def preload_documents(self, documents: List[str], cache_key: str):
#         """
#         Precompute the KV cache from pre-chunked documents and save it.

#         Args:
#             documents (List[str]): Pre-chunked documents
#             cache_key (str): The key for the KV cache
#         """
#         logger.info(f"Precomputing KV cache for {len(documents)} document chunks...")
#         try:
#             # Create cache entries with both text and embeddings
#             cache_entries = []
#             for chunk in documents:
#                 embedding = self.embedding_model.embed_query(chunk)
#                 cache_entries.append(CacheEntry(chunk, embedding))

#             self.cache.save_cache(cache_key, cache_entries)
#             logger.info(f"Preloaded {len(cache_entries)} document chunks into KV cache")
#         except Exception as e:
#             logger.error(f"Error during KV cache preloading: {e}")
#             raise

#     def infer(
#         self,
#         query: str,
#         cache_key: str,
#         top_k: int = 5,
#         similarity_threshold: float = 0.5,
#     ) -> str:
#         """
#         Perform inference using the precomputed KV cache and a query.
#         """
#         self.top_k = top_k
#         self.similarity_threshold = similarity_threshold
#         if not self.loaded_kv_cache:
#             logger.info(f"Loading KV cache for key: {cache_key}")
#             self.loaded_kv_cache = self.cache.load_cache(cache_key)

#         if not self.loaded_kv_cache:
#             logger.error("KV cache is not loaded. Please preload the documents first.")
#             raise RuntimeError("KV cache missing or not loaded.")

#         try:
#             # Generate query embedding
#             logger.info("Generating query embedding...")
#             query_embedding = self.embedding_model.embed_query(query)

#             # Get relevant context using semantic search
#             logger.info("Retrieving relevant context...")
#             relevant_context = self.get_relevant_context(
#                 query_embedding, self.loaded_kv_cache
#             )

#             # Perform inference with filtered context
#             logger.info("Performing inference with filtered context...")
#             response = self.llm.answer_question(
#                 context=relevant_context, question=query
#             )
#             return response
#         except Exception as e:
#             logger.error(f"Error during inference: {e}")
#             raise

#     def reset_session(self):
#         """
#         Reset the session by clearing the loaded KV cache.
#         """
#         logger.info("Resetting session and clearing loaded KV cache...")
#         self.loaded_kv_cache = None

# import warnings
# from loguru import logger
# import sys
# import pickle
# import os
# import numpy as np
# from typing import List, Dict, Any, Optional
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# warnings.filterwarnings("ignore")

# # Set up logging
# logger.remove()
# logger.add(
#     sys.stdout, format="<green>{level}</green>: <level>{message}</level>", level="INFO"
# )
# logger.add(
#     sys.stdout, format="<red>{level}</red>: <level>{message}</level>", level="ERROR"
# )


# class KVCache:
#     """
#     Key-Value Cache for storing and managing preloaded knowledge.
#     """

#     def __init__(self, cache_dir="kv_cache"):
#         self.cache_dir = cache_dir
#         if not os.path.exists(self.cache_dir):
#             os.makedirs(self.cache_dir)

#     def save_cache(self, key, kv_data):
#         filepath = os.path.join(self.cache_dir, f"{key}.pkl")
#         with open(filepath, "wb") as f:
#             pickle.dump(kv_data, f)
#         logger.info(f"KV cache saved: {filepath}")

#     def load_cache(self, key):
#         filepath = os.path.join(self.cache_dir, f"{key}.pkl")
#         if os.path.exists(filepath):
#             with open(filepath, "rb") as f:
#                 kv_data = pickle.load(f)
#             logger.info(f"KV cache loaded: {filepath}")
#             return kv_data
#         else:
#             logger.warning(f"KV cache not found for key: {key}")
#             return None

#     def reset_cache(self):
#         for filename in os.listdir(self.cache_dir):
#             filepath = os.path.join(self.cache_dir, filename)
#             os.remove(filepath)
#         logger.info("KV cache reset successfully")


# class CacheEntry:
#     """
#     Structure to hold text content and optionally its embedding.
#     """

#     def __init__(self, text: str, embedding: Optional[np.ndarray] = None):
#         self.text = text
#         self.embedding = embedding


# class CAG:
#     """
#     Cache-Augmented Generation Pipeline with optional embedding-based similarity search.
#     """

#     def __init__(
#         self,
#         llm,
#         embedding_model: Optional[Any] = None,  # Make embedding_model optional
#         cache: Optional[KVCache] = None,
#     ):
#         """
#         Initialize the CAG pipeline.

#         Args:
#             llm: The LLM instance
#             embedding_model: The embedding model instance (optional)
#             cache (KVCache): The KV cache instance (optional)
#         """
#         self.llm = llm
#         self.embedding_model = embedding_model
#         self.cache = cache if cache else KVCache()  # Default cache if not provided
#         self.use_embedding = embedding_model is not None  # Auto-set use_embedding
#         self.loaded_kv_cache = None

#     def compute_similarity(
#         self, query_embedding: np.ndarray, doc_embedding: np.ndarray
#     ) -> float:
#         """
#         Compute cosine similarity between query and document embeddings.
#         """
#         return np.dot(query_embedding, doc_embedding) / (
#             np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
#         )

#     def text_based_similarity(self, query: str, documents: List[str]) -> List[float]:
#         """
#         Compute similarity between query and documents using TF-IDF.
#         """
#         vectorizer = TfidfVectorizer()
#         tfidf_matrix = vectorizer.fit_transform([query] + documents)
#         similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
#         return similarities

#     def get_relevant_context(
#         self,
#         query: str,
#         cache_entries: List[CacheEntry],
#         top_k: int = 5,
#         similarity_threshold: float = 0.5,
#     ) -> List[str]:
#         """
#         Retrieve most relevant context chunks based on similarity.
#         """
#         if self.use_embedding:
#             # Embedding-based similarity search
#             query_embedding = self.embedding_model.embed_query(query)
#             similarities = [
#                 (entry, self.compute_similarity(query_embedding, entry.embedding))
#                 for entry in cache_entries
#                 if entry.embedding is not None
#             ]
#         else:
#             # Text-based similarity search
#             document_texts = [entry.text for entry in cache_entries]
#             similarities = [
#                 (entry, score)
#                 for entry, score in zip(
#                     cache_entries, self.text_based_similarity(query, document_texts)
#                 )
#             ]

#         # Sort by similarity score
#         similarities.sort(key=lambda x: x[1], reverse=True)

#         # Filter by threshold and take top k
#         relevant_chunks = [
#             entry.text
#             for entry, score in similarities[:top_k]
#             if score >= similarity_threshold
#         ]

#         logger.info(f"Selected {len(relevant_chunks)} relevant chunks from cache")
#         return relevant_chunks

#     def preload_documents(self, documents: List[str], cache_key: str):
#         """
#         Precompute the KV cache from pre-chunked documents and save it.
#         """
#         logger.info(f"Precomputing KV cache for {len(documents)} document chunks...")
#         try:
#             # Create cache entries with text and optionally embeddings
#             cache_entries = []
#             for chunk in documents:
#                 if self.use_embedding:
#                     embedding = self.embedding_model.embed_query(chunk)
#                     cache_entries.append(CacheEntry(chunk, embedding))
#                 else:
#                     cache_entries.append(CacheEntry(chunk))

#             self.cache.save_cache(cache_key, cache_entries)
#             logger.info(f"Preloaded {len(cache_entries)} document chunks into KV cache")
#         except Exception as e:
#             logger.error(f"Error during KV cache preloading: {e}")
#             raise

#     def infer(
#         self,
#         query: str,
#         cache_key: str,
#         top_k: int = 5,
#         similarity_threshold: float = 0.5,
#     ) -> str:
#         """
#         Perform inference using the precomputed KV cache and a query.
#         """
#         if not self.loaded_kv_cache:
#             logger.info(f"Loading KV cache for key: {cache_key}")
#             self.loaded_kv_cache = self.cache.load_cache(cache_key)

#         if not self.loaded_kv_cache:
#             logger.error("KV cache is not loaded. Please preload the documents first.")
#             raise RuntimeError("KV cache missing or not loaded.")

#         try:
#             # Retrieve relevant context
#             logger.info("Retrieving relevant context...")
#             relevant_context = self.get_relevant_context(
#                 query, self.loaded_kv_cache, top_k, similarity_threshold
#             )

#             # Perform inference with filtered context
#             logger.info("Performing inference with filtered context...")
#             response = self.llm.answer_question(
#                 context=relevant_context, question=query
#             )
#             return response
#         except Exception as e:
#             logger.error(f"Error during inference: {e}")
#             raise

#     def reset_session(self):
#         """
#         Reset the session by clearing the loaded KV cache.
#         """
#         logger.info("Resetting session and clearing loaded KV cache...")
#         self.loaded_kv_cache = None


import warnings
from loguru import logger
import sys
import pickle
import os
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download("punkt")
nltk.download("stopwords")

warnings.filterwarnings("ignore")

# Set up logging
logger.remove()
logger.add(
    sys.stdout, format="<green>{level}</green>: <level>{message}</level>", level="INFO"
)
logger.add(
    sys.stdout, format="<red>{level}</red>: <level>{message}</level>", level="ERROR"
)


class AnswerValidator:
    """Validates generated answers for quality and hallucination"""

    def __init__(self, llm):
        self.llm = llm

    def check_hallucination(self, answer: str, context: List[str]) -> bool:
        result = self.llm.check_hallucination(context=context, answer=answer)
        return result.lower() == "yes"

    def grade_relevance(self, context: List[str], query: str) -> List[str]:
        return self.llm.grade_docs(context=context, question=query)


class WebSearchFallback:
    """Handles web search when local context is insufficient"""

    def search(self, query: str) -> List[str]:
        from ...utils import search_duckduckgo

        logger.info("Performing web search for additional context")
        return search_duckduckgo(query)


class KVCache:
    """
    Key-Value Cache for storing and managing preloaded knowledge.
    """

    def __init__(self, cache_dir="kv_cache"):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def save_cache(self, key, kv_data):
        filepath = os.path.join(self.cache_dir, f"{key}.pkl")
        with open(filepath, "wb") as f:
            pickle.dump(kv_data, f)
        logger.info(f"KV cache saved: {filepath}")

    def load_cache(self, key):
        filepath = os.path.join(self.cache_dir, f"{key}.pkl")
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                kv_data = pickle.load(f)
            logger.info(f"KV cache loaded: {filepath}")
            return kv_data
        else:
            logger.warning(f"KV cache not found for key: {key}")
            return None

    def reset_cache(self):
        for filename in os.listdir(self.cache_dir):
            filepath = os.path.join(self.cache_dir, filename)
            os.remove(filepath)
        logger.info("KV cache reset successfully")


class CacheEntry:
    """
    Structure to hold text content and optionally its embedding.
    """

    def __init__(self, text: str, embedding: Optional[np.ndarray] = None):
        self.text = text
        self.embedding = embedding


class CAG:
    """
    Cache-Augmented Generation Pipeline with multi-query and smart retrieval.
    """

    def __init__(
        self,
        llm,
        embedding_model: Optional[Any] = None,
        cache: Optional[KVCache] = None,
        default_similarity_search_type: str = "tfidf",  # Default similarity search type
    ):
        """
        Initialize the CAG pipeline.

        Args:
            llm: The LLM instance
            embedding_model: The embedding model instance (optional)
            cache (KVCache): The KV cache instance (optional)
            default_similarity_search_type (str): Default similarity search type. Options: "tfidf", "bm25", "jaccard"
        """
        self.llm = llm
        self.embedding_model = embedding_model
        self.cache = cache if cache else KVCache()  # Default cache if not provided
        self.use_embedding = embedding_model is not None  # Auto-set use_embedding
        self.loaded_kv_cache = None
        self.default_similarity_search_type = default_similarity_search_type.lower()

        # Validate default_similarity_search_type
        if self.default_similarity_search_type not in ["tfidf", "bm25", "jaccard"]:
            raise ValueError(
                "Invalid default_similarity_search_type. Choose from 'tfidf', 'bm25', or 'jaccard'."
            )

    def _text_based_similarity(
        self, query: str, documents: List[str], similarity_search_type: str
    ) -> List[float]:
        """
        Compute similarity between query and documents based on the selected similarity search type.
        """
        if similarity_search_type == "tfidf":
            return self._tfidf_similarity(query, documents)
        elif similarity_search_type == "bm25":
            return self._bm25_similarity(query, documents)
        elif similarity_search_type == "jaccard":
            return self._jaccard_similarity(query, documents)
        else:
            raise ValueError(
                f"Unsupported similarity search type: {similarity_search_type}"
            )

    def _tfidf_similarity(self, query: str, documents: List[str]) -> List[float]:
        """
        Compute similarity between query and documents using TF-IDF.
        """
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([query] + documents)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        return similarities

    def _bm25_similarity(self, query: str, documents: List[str]) -> List[float]:
        """
        Compute similarity between query and documents using BM25.
        """
        from rank_bm25 import BM25Okapi

        tokenized_docs = [doc.split() for doc in documents]
        bm25 = BM25Okapi(tokenized_docs)
        tokenized_query = query.split()
        scores = bm25.get_scores(tokenized_query)
        return scores

    def _jaccard_similarity(self, query: str, documents: List[str]) -> List[float]:
        """
        Compute similarity between query and documents using Jaccard similarity.
        """
        query_tokens = set(query.split())
        similarities = []
        for doc in documents:
            doc_tokens = set(doc.split())
            intersection = query_tokens.intersection(doc_tokens)
            union = query_tokens.union(doc_tokens)
            jaccard_score = len(intersection) / len(union) if union else 0
            similarities.append(jaccard_score)
        return similarities

    def _get_relevant_context(
        self,
        query: str,
        cache_entries: List[CacheEntry],
        top_k: int = 5,
        similarity_threshold: float = 0.1,
        similarity_search_type: str = "tfidf",  # Default to TF-IDF
    ) -> List[str]:
        """
        Retrieve most relevant context chunks based on similarity.
        """
        if self.use_embedding:
            # Embedding-based similarity search
            query_embedding = self.embedding_model.embed_query(query)
            similarities = [
                (entry, self._compute_similarity(query_embedding, entry.embedding))
                for entry in cache_entries
                if entry.embedding is not None
            ]
        else:
            # Text-based similarity search
            document_texts = [entry.text for entry in cache_entries]
            similarities = [
                (entry, score)
                for entry, score in zip(
                    cache_entries,
                    self._text_based_similarity(
                        query, document_texts, similarity_search_type
                    ),
                )
            ]

        # Sort by similarity score
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Filter by threshold and take top k
        relevant_chunks = [
            entry.text
            for entry, score in similarities[:top_k]
            if score >= similarity_threshold
        ]

        logger.info(f"Selected {len(relevant_chunks)} relevant chunks from cache")
        return relevant_chunks

    def preload_documents(self, documents: List[str], cache_key: str):
        """
        Precompute the KV cache from pre-chunked documents and save it.
        """
        logger.info(f"Precomputing KV cache for {len(documents)} document chunks...")
        try:
            # Create cache entries with text and optionally embeddings
            cache_entries = []
            for chunk in documents:
                if self.use_embedding:
                    embedding = self.embedding_model.embed_query(chunk)
                    cache_entries.append(CacheEntry(chunk, embedding))
                else:
                    cache_entries.append(CacheEntry(chunk))

            self.cache.save_cache(cache_key, cache_entries)
            logger.info(f"Preloaded {len(cache_entries)} document chunks into KV cache")
        except Exception as e:
            logger.error(f"Error during KV cache preloading: {e}")
            raise

    def _compute_similarity(
        self, query_embedding: np.ndarray, doc_embedding: np.ndarray
    ) -> float:
        """
        Compute cosine similarity between query and document embeddings.
        """
        return np.dot(query_embedding, doc_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
        )

    # def _text_based_similarity(self, query: str, documents: List[str]) -> List[float]:
    #     """
    #     Compute similarity between query and documents using TF-IDF.
    #     """
    #     vectorizer = TfidfVectorizer()
    #     tfidf_matrix = vectorizer.fit_transform([query] + documents)
    #     similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    #     return similarities

    # def _get_relevant_context(
    #     self,
    #     query: str,
    #     cache_entries: List[CacheEntry],
    #     top_k: int = 5,
    #     similarity_threshold: float = 0.5,
    # ) -> List[str]:
    #     """
    #     Retrieve most relevant context chunks based on similarity.
    #     """
    #     if self.use_embedding:
    #         # Embedding-based similarity search
    #         query_embedding = self.embedding_model.embed_query(query)
    #         similarities = [
    #             (entry, self._compute_similarity(query_embedding, entry.embedding))
    #             for entry in cache_entries
    #             if entry.embedding is not None
    #         ]
    #     else:
    #         # Text-based similarity search
    #         document_texts = [entry.text for entry in cache_entries]
    #         print(document_texts)
    #         similarities = [
    #             (entry, score)
    #             for entry, score in zip(
    #                 cache_entries, self._text_based_similarity(query, document_texts)
    #             )
    #         ]
    #         print(similarities)
    #     # Sort by similarity score
    #     similarities.sort(key=lambda x: x[1], reverse=True)

    #     # Filter by threshold and take top k
    #     relevant_chunks = [
    #         entry.text
    #         for entry, score in similarities[:top_k]
    #         if score >= similarity_threshold
    #     ]

    #     logger.info(f"Selected {len(relevant_chunks)} relevant chunks from cache")
    #     return relevant_chunks

    def multi_query_retrieval(self, query: str, top_k: int = 5) -> List[str]:
        """
        Generate multiple queries and retrieve context for each.
        """
        from ...tools import MultiQueryRetrieval  # Import your multi-query tool

        logger.info("Performing multi-query retrieval")
        multi_query = MultiQueryRetrieval(self.llm, self.cache, top_k)
        return multi_query.run(query)

    def smart_retrieve(
        self,
        query: str,
        cache_entries: List[CacheEntry],
        top_k: int = 5,
        similarity_threshold: float = 0.5,
        similarity_search_type: Optional[str] = None,  # New parameter
    ) -> List[str]:
        """
        Smart retrieval with validation and fallback mechanisms.
        """
        logger.info("Using smart retrieval")

        # Initial retrieval
        relevant_context = self._get_relevant_context(
            query, cache_entries, top_k, similarity_threshold, similarity_search_type
        )

        if not relevant_context:
            logger.warning("No relevant context found in cache")
            return self._handle_web_fallback(query, top_k)

        # Grade documents using LLM's relevance check
        try:
            validator = AnswerValidator(self.llm)
            graded_context = validator.grade_relevance(relevant_context, query)
            if not graded_context:
                logger.info("No relevant documents found after grading")
                return self._handle_web_fallback(query, top_k)
        except Exception as e:
            logger.error(f"Error in document grading: {str(e)}")
            graded_context = relevant_context

        # Ensure we don't exceed top_k
        graded_context = graded_context[:top_k]

        # Check for hallucination if we have context
        if graded_context:
            try:
                answer = self.llm.answer_question(
                    context=graded_context, question=query
                )
                hallucination_result = validator.check_hallucination(
                    context=graded_context, answer=answer
                )
                if hallucination_result.lower() == "yes":
                    logger.info("Hallucination detected, regenerating answer")
                    answer = self.llm.answer_question(
                        context=graded_context, question=query
                    )
            except Exception as e:
                logger.error(
                    f"Error in answer generation or hallucination check: {str(e)}"
                )

        return graded_context

    def _handle_web_fallback(self, query: str, top_k: int) -> List[str]:
        """
        Handle web search fallback when cache retrieval is insufficient.
        """
        try:
            web_fallback = WebSearchFallback()
            web_results = web_fallback.search(query)

            if not web_results:
                logger.warning("No results from web fallback")
                return []

            # Grade web results using LLM's relevance check
            validator = AnswerValidator(self.llm)
            try:
                graded_web_context = validator.grade_relevance(web_results, query)
            except Exception as e:
                logger.error(f"Error grading web results: {str(e)}")
                graded_web_context = web_results

            return graded_web_context[:top_k]

        except Exception as e:
            logger.error(f"Web fallback failed: {str(e)}")
            return []

    def infer(
        self,
        query: str,
        cache_key: str,
        top_k: int = 5,
        similarity_threshold: float = 0.1,
        use_multi_query: bool = False,
        smart_retrieval: bool = False,
        similarity_search_type: Optional[
            str
        ] = None,  # Optional parameter for dynamic selection
    ) -> str:
        """
        Perform inference using the precomputed KV cache and a query.

        Args:
            query: The query string.
            cache_key: The key for the preloaded KV cache.
            top_k: Number of top results to retrieve.
            similarity_threshold: Minimum similarity score for filtering results.
            use_multi_query: Whether to use multi-query retrieval.
            smart_retrieval: Whether to use smart retrieval with validation.
            similarity_search_type: Similarity search type to use. If None, defaults to the class default. Options: "tfidf", "bm25", "jaccard"
        """
        if not self.loaded_kv_cache:
            logger.info(f"Loading KV cache for key: {cache_key}")
            self.loaded_kv_cache = self.cache.load_cache(cache_key)

        if not self.loaded_kv_cache:
            logger.error("KV cache is not loaded. Please preload the documents first.")
            raise RuntimeError("KV cache missing or not loaded.")

        # Use the provided similarity_search_type or fall back to the default
        similarity_search_type = (
            similarity_search_type or self.default_similarity_search_type
        )

        try:
            # Retrieve relevant context
            logger.info("Retrieving relevant context...")
            if smart_retrieval:
                relevant_context = self.smart_retrieve(
                    query,
                    self.loaded_kv_cache,
                    top_k,
                    similarity_threshold,
                    similarity_search_type,
                )
            elif use_multi_query:
                relevant_context = self.multi_query_retrieval(query, top_k)
            else:
                relevant_context = self._get_relevant_context(
                    query,
                    self.loaded_kv_cache,
                    top_k,
                    similarity_threshold,
                    similarity_search_type,
                )

            # Perform inference with filtered context
            logger.info("Performing inference with filtered context...")
            response = self.llm.answer_question(
                context=relevant_context, question=query
            )
            return response
        except Exception as e:
            logger.error(f"Error during inference: {e}")
            raise
