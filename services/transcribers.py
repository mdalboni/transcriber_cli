"""
This module contains classes for transcribing audio files into text.

Classes:
    TranscriberService: An abstract base class for a transcriber service.
    AAITranscriber: A concrete implementation of TranscriberService using the AssemblyAI API for transcribing.

"""
from os import environ
import assemblyai as aai
from assemblyai import Transcript


class TranscriberService:
    """
    TranscriberService is an abstract base class that provides a blueprint for a service that transcribes audio files into text.

    Attributes:
        PREFIX (str): A prefix for print statements, used for logging purposes.
    """

    PREFIX = '[TRANSCRIBER SERVICE]'

    def transcribe(self, file_path: str) -> list[str]:
        """
        Abstract method to transcribe an audio file into text.

        Args:
            file_path (str): The path to the audio file to be transcribed.

        Raises:
            NotImplemented: This method needs to be implemented in a subclass.

        Returns:
            list[str]: This method should return a list of transcribed sentences when implemented.
        """
        raise NotImplemented

    def transcribe_many(self, file_paths: list[str]):
        """
        Abstract method to transcribe multiple audio files into text.

        Args:
            file_paths (list[str]): A list of paths to the audio files to be transcribed.

        Raises:
            NotImplemented: This method needs to be implemented in a subclass.

        Returns:
            list[str]: This method should return a list of transcribed sentences from all audio files when implemented.
        """
        raise NotImplemented


class AAITranscriber(TranscriberService):
    """
    AAITranscriber is a concrete implementation of TranscriberService that uses the AssemblyAI API to transcribe audio files into text.

    Attributes:
        aai (assemblyai): The AssemblyAI API client.
        transcriber (assemblyai.Transcriber): The AssemblyAI transcriber.
    """

    def __init__(self):
        """
        Initializes the AssemblyAI API client and transcriber with the API key from the environment variables.
        """
        self.aai = aai
        self.aai.settings.api_key = environ.get('ASSEMBLY_AI_API_KEY')
        self.transcriber = aai.Transcriber()

    def transcribe(self, file_path: str) -> list[str]:
        """
        Transcribes an audio file into text using the AssemblyAI API.

        Args:
            file_path (str): The path to the audio file to be transcribed.

        Returns:
            list[str]: A list of transcribed sentences.
        """
        transcript = self.transcriber.transcribe(file_path)
        return self._get_sentences_from_transcript(transcript)

    def transcribe_many(self, file_paths: list[str]):
        """
        Transcribes multiple audio files into text using the AssemblyAI API.

        Args:
            file_paths (list[str]): A list of paths to the audio files to be transcribed.

        Returns:
            list[str]: A list of transcribed sentences from all audio files.
        """
        transcripts = self.transcriber.transcribe_group(file_paths)
        transcriptions = []
        for transcript in transcripts.transcripts:
            transcriptions.extend(self._get_sentences_from_transcript(transcript))
        return transcriptions

    def _get_sentences_from_transcript(self, transcript: Transcript) -> list[str]:
        """
        Extracts sentences from a transcript.

        Args:
            transcript (Transcript): The transcript object from which to extract sentences.

        Returns:
            list[str]: A list of sentences extracted from the transcript.
        """
        print(self.PREFIX, self.__class__.__name__, 'File:', transcript.audio_url, 'Sentences found:')
        sentences = []
        sentences_obj = transcript.get_sentences()
        for sentence in sentences_obj:
            print('\t-', sentence.text)
            sentences.append(sentence.text)
        return sentences
