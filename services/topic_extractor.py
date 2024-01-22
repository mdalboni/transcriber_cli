"""
This module contains classes for extracting topics from text.

Classes:
    TopicExtractor: An abstract base class for a topic extractor.
    LDATopicExtractor: A concrete implementation of TopicExtractor using the Latent Dirichlet Allocation (LDA) model for topic extraction.

"""

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

custom_stop_words = ["is", "of", "for", "the", "a", "an", "are", "in", "on", "at", "and", "to"]


class TopicExtractor:
    """
    An abstract base class for a topic extractor.

    Attributes:
        PREFIX (str): A prefix for print statements.

    Methods:
        get_topics: Extract topics from a list of texts. Not implemented in this base class.
    """

    PREFIX = '[TOPIC EXTRACTOR]'

    def get_topics(self, texts: list[str]) -> list[list[str]]:
        """
        Extract topics from a list of texts.

        Args:
            texts (list[str]): A list of texts to extract topics from.

        Raises:
            NotImplemented: This method is not implemented in the base class.
        """
        raise NotImplemented


class LDATopicExtractor(TopicExtractor):
    """
    A concrete implementation of TopicExtractor using the Latent Dirichlet Allocation (LDA) model for topic extraction.

    Methods:
        get_topics: Extract topics from a list of texts using the LDA model.
    """

    def get_topics(self, texts: list[str], top_k=5) -> list[list[str]]:
        """
        Extract topics from a list of texts using the LDA model.

        Args:
            texts (list[str]): A list of texts to extract topics from.
            top_k (int, optional): The number of top topics to return. Defaults to 5.

        Returns:
            list[list[str]]: A list of top topics for each text.
        """
        vectorizer = CountVectorizer(stop_words=custom_stop_words)
        lda = LatentDirichletAllocation(n_components=len(texts), random_state=42)  # 42 picked just for fun
        lda.fit(vectorizer.fit_transform(texts))

        feature_names = vectorizer.get_feature_names_out()
        topics = []
        for topic_idx, topic in enumerate(lda.components_):
            print(self.PREFIX, self.__class__.__name__, 'Topics found for:', texts[topic_idx])
            top_words_idx = topic.argsort()[:-top_k - 1:-1]
            top_words = [feature_names[i] for i in top_words_idx]
            print('\t', top_words)
            topics.append(top_words)

        return topics
