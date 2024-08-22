from __future__ import annotations

import os
from typing import TYPE_CHECKING, List, Optional
from indox.core import Embeddings

def get_from_env(key: str, env_key: str, default: Optional[str] = None) -> str:
    """Get a value from an environment variable or return a default value.

    Args:
        key: The key to look up.
        env_key: The environment variable to look up if the key is not found.
        default: The default value to return if the key is not found.

    Returns:
        str: The value of the key or default value.

    Raises:
        ValueError: If the key is not found and no default value is provided.
    """
    value = os.environ.get(env_key)
    if value:
        return value
    if default is not None:
        return default
    raise ValueError(
        f"Did not find {key}, please add an environment variable `{env_key}` "
        f"which contains it, or pass `{key}` as a named parameter."
    )


class ElasticsearchEmbeddings(Embeddings):
    """Elasticsearch embedding models.

    This class provides an interface to generate embeddings using a model deployed
    in an Elasticsearch cluster. It requires an Elasticsearch connection object
    and the model_id of the model deployed in the cluster.

    In Elasticsearch, you need to have an embedding model loaded and deployed.
    - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-trained-model.html
    - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-deploy-models.html
    """
    if TYPE_CHECKING:
        from elasticsearch import Elasticsearch
        from elasticsearch.client import MlClient

    def __init__(
        self,
        client: MlClient,
        model_id: str,
        *,
        input_field: str = "text_field",
    ):
        """
        Initialize the ElasticsearchEmbeddings instance.

        Args:
            client (MlClient): An Elasticsearch ML client object.
            model_id (str): The model_id of the model deployed in the Elasticsearch
                cluster.
            input_field (str): The name of the key for the input text field in the
                document. Defaults to 'text_field'.
        """
        self.client = client
        self.model_id = model_id
        self.input_field = input_field

    @classmethod
    def from_credentials(
        cls,
        model_id: str,
        *,
        es_cloud_id: Optional[str] = None,
        es_user: Optional[str] = None,
        es_password: Optional[str] = None,
        input_field: str = "text_field",
    ) -> ElasticsearchEmbeddings:
        """Instantiate embeddings from Elasticsearch credentials.

        Args:
            model_id (str): The model_id of the model deployed in the Elasticsearch
                cluster.
            input_field (str): The name of the key for the input text field in the
                document. Defaults to 'text_field'.
            es_cloud_id: (str, optional): The Elasticsearch cloud ID to connect to.
            es_user: (str, optional): Elasticsearch username.
            es_password: (str, optional): Elasticsearch password.

        Returns:
            ElasticsearchEmbeddings: An instance of ElasticsearchEmbeddings initialized with the provided credentials.
        """
        try:
            from elasticsearch import Elasticsearch
            from elasticsearch.client import MlClient
        except ImportError:
            raise ImportError(
                "elasticsearch package not found, please install with 'pip install "
                "elasticsearch'"
            )

        es_cloud_id = es_cloud_id or get_from_env("es_cloud_id", "ES_CLOUD_ID")
        es_user = es_user or get_from_env("es_user", "ES_USER")
        es_password = es_password or get_from_env("es_password", "ES_PASSWORD")

        # Connect to Elasticsearch
        es_connection = Elasticsearch(
            cloud_id=es_cloud_id, basic_auth=(es_user, es_password)
        )
        client = MlClient(es_connection)
        return cls(client, model_id, input_field=input_field)

    @classmethod
    def from_es_connection(
        cls,
        model_id: str,
        es_connection: Elasticsearch,
        input_field: str = "text_field",
    ) -> ElasticsearchEmbeddings:
        """
        Instantiate embeddings from an existing Elasticsearch connection.

        This method provides a way to create an instance of the ElasticsearchEmbeddings
        class using an existing Elasticsearch connection. The connection object is used
        to create an MlClient, which is then used to initialize the
        ElasticsearchEmbeddings instance.

        Args:
        model_id (str): The model_id of the model deployed in the Elasticsearch cluster.
        es_connection (elasticsearch.Elasticsearch): An existing Elasticsearch
        connection object.
        input_field (str, optional): The name of the key for the input text field in the document. Defaults to 'text_field'.

        Returns:
        ElasticsearchEmbeddings: An instance of ElasticsearchEmbeddings initialized with the provided connection.
        """
        # Importing MlClient from elasticsearch.client within the method to
        # avoid unnecessary import if the method is not used
        from elasticsearch.client import MlClient

        # Create an MlClient from the given Elasticsearch connection
        client = MlClient(es_connection)

        # Return a new instance of the ElasticsearchEmbeddings class
        return cls(client, model_id, input_field=input_field)

    def _embedding_func(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for the given texts using the Elasticsearch model.

        Args:
            texts (List[str]): A list of text strings to generate embeddings for.

        Returns:
            List[List[float]]: A list of embeddings, one for each text in the input list.
        """
        response = self.client.infer_trained_model(
            model_id=self.model_id, docs=[{self.input_field: text} for text in texts]
        )

        embeddings = [doc["predicted_value"] for doc in response["inference_results"]]
        return embeddings

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents.

        Args:
            texts (List[str]): A list of document text strings to generate embeddings for.

        Returns:
            List[List[float]]: A list of embeddings, one for each document in the input list.
        """
        return self._embedding_func(texts)

    def embed_query(self, text: str) -> List[float]:
        """
        Generate an embedding for a single query text.

        Args:
            text (str): The query text to generate an embedding for.

        Returns:
            List[float]: The embedding for the input query text.
        """
        return self._embedding_func([text])[0]
