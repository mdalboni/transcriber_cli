"""
This module contains classes for encoding text.

Classes:
    TextEncoder: An abstract base class for a text encoder.
    BertTextEncoder: A concrete implementation of TextEncoder using the BERT model for encoding.

"""

from sentence_transformers import SentenceTransformer


class TextEncoder:
    """
    An abstract base class for a text encoder.

    Attributes:
        PREFIX (str): A prefix for print statements.

    Methods:
        encode: Encode a list of texts. Not implemented in this base class.
    """

    PREFIX = '[TEXT ENCODER]'

    def encode(self, texts: list[str]) -> list[dict]:
        """
        Encode a list of texts.

        Args:
            texts (list[str]): A list of texts to encode.

        Raises:
            NotImplemented: This method is not implemented in the base class.
        """
        raise NotImplemented


class BertTextEncoder(TextEncoder):
    """
    A concrete implementation of TextEncoder using the BERT model for encoding.

    Attributes:
        model (str): The name of the BERT model.
        transformer (SentenceTransformer): The SentenceTransformer instance.

    Methods:
        encode: Encode a list of texts using the BERT model.
    """

    model = 'multi-qa-distilbert-dot-v1'

    def __init__(self):
        """
        Initialize a BertTextEncoder instance.

        The BERT model is initialized in this method.
        """
        self.transformer = SentenceTransformer(self.model)

    def encode(self, texts: list[str]):
        """
        Encode a list of texts using the BERT model.

        Args:
            texts (list[str]): A list of texts to encode.

        Returns:
            list[dict]: A list of encoded texts.
        """
        print(self.PREFIX, self.__class__.__name__, 'Encoding inputs...')
        return [self.transformer.encode(text) for text in texts]
