"""
This module contains classes for interacting with a vector database.

Classes:
    VectorDB: An abstract base class for a vector database.
    PineconeVDB: A concrete implementation of VectorDB using Pinecone as the vector database.

"""
from os import environ

from pinecone import Pinecone, ScoredVector


class VectorDB:
    """
    An abstract base class for a vector database.

    Methods:
       save: Save a list of vectors to the database. Not implemented in this base class.
    """

    def save(self, vectors: list[dict]):
        """
        Save a list of vectors to the database.

        Args:
            vectors (list[dict]): A list of vectors to save.

        Raises:
            NotImplemented: This method is not implemented in the base class.
        """
        raise NotImplemented


class PineconeVDB(VectorDB):
    """
    A concrete implementation of VectorDB using Pinecone as the vector database.

    Attributes:
        prefix (str): A prefix for print statements.
        namespace (str): The namespace for the Pinecone index.
        pinecone (Pinecone): The Pinecone client.
        index (Pinecone.Index): The Pinecone index.

    Methods:
        save: Save a list of vectors to the Pinecone index.
        query: Query the Pinecone index for the most similar vectors.
    """

    prefix = '[Pinecone]'

    def __init__(self, index: str, namespace="ns1"):
        """
        Initialize a PineconeVDB instance.

        Args:
            index (str): The name of the Pinecone index.
            namespace (str, optional): The namespace for the Pinecone index. Defaults to "ns1".
        """
        self.namespace = namespace
        self.pinecone = Pinecone(environ.get('PINECONE_API_KEY'))
        self.index = self.pinecone.Index(index)

    def save(self, vectors: list[dict]):
        """
        Save a list of vectors to the Pinecone index.

        Args:
            vectors (list[dict]): A list of vectors to save.

        Raises:
            Exception: If an error occurs during the upload.
        """
        try:
            print(self.prefix, 'Starting data upload...')
            self.index.upsert(vectors=vectors, namespace=self.namespace)
            print(self.prefix, 'Upload completed...')
        except Exception as ex:
            print(self.prefix, 'Failed with error:', ex)
            raise ex

    def query(self, vector: list[float], metadata: dict = None, top_k=2) -> list[ScoredVector]:
        """
        Query the Pinecone index for the most similar vectors.

        Args:
            vector (list[float]): The vector to compare.
            metadata (dict, optional): Additional metadata to filter the results. Defaults to None.
            top_k (int, optional): The number of most similar vectors to return. Defaults to 2.

        Returns:
            list[ScoredVector]: A list of the most similar vectors.
        """
        response = self.index.query(
            namespace=self.namespace,
            vector=vector,
            top_k=top_k,
            include_values=True,
            include_metdata=True if metadata else False,
            filter=metadata,
        )
        return response.matches
