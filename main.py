#!/usr/bin/env python
"""
main.py
-------

This module contains the main entry point for the application. It provides a command-line interface (CLI) for saving and searching transcriptions of audio files.

Functions:
    verify_files: Checks if the provided files exist and match the expected extension.
    save_command: Transcribes audio files, extracts topics, encodes the transcriptions, and saves them in a vector database.
    search_file_command: Searches for a vector in a file and prints the results.
    warm_up: Checks if the required environment variables are set.
    main: The main entry point for the application. Parses command-line arguments and calls the appropriate function.

Usage:
    python main.py save --file <file_paths>
    python main.py search --file <file_path> [--metadata <metadata>] [--top_k <top_k>] [--output <output_file>]
"""
import argparse
import json
import warnings
from os import environ
from os.path import exists, isfile
from uuid import uuid4

from services.encoder import BertTextEncoder
from services.topic_extractor import LDATopicExtractor
from services.transcribers import AAITranscriber
from services.vector_database import PineconeVDB

warnings.filterwarnings("ignore")


def verify_files(files: list[str], check_extension: str = None):
    for file in files:
        if check_extension and not file.endswith(check_extension):
            raise Exception(f'File: {file} does not match the {check_extension} pattern')
        if not exists(file) and not isfile(file):
            raise Exception(f'File: {file} is not valid or not exists')


def save_command(args):
    verify_files(args.file)
    transcriber = AAITranscriber()
    transcriptions = transcriber.transcribe_many(args.file)
    topics = LDATopicExtractor()
    transcriptions_topics = topics.get_topics(transcriptions)
    encoder = BertTextEncoder()
    vectorized_data = encoder.encode(transcriptions)
    vectors_input = [
        {
            "id": str(uuid4()),
            "metadata": {"text": transcriptions_topics[idx]},
            "values": vectorized_data[idx]
        }
        for idx in range(len(vectorized_data))
    ]
    vdb = PineconeVDB('test')
    vdb.save(vectors_input)
    print("Completed!")


def search_file_command(args):
    PREFIX = '[SEARCH RESULT]'
    metadata = None
    verify_files([args.file], '.csv')
    if args.metadata:
        metadata = {"text": {"$in": args.metadata}}
    with open(args.file, 'r') as file:
        data = file.readline(5_000_000)
        vector = [float(item) for item in data.split(',')]
        if len(vector) != 768:
            raise Exception('Your vector does not have a dimension of 768. Please fix this and try again.')
    vdb = PineconeVDB('test')
    responses = vdb.query(vector, metadata, top_k=int(args.top_k))
    print(PREFIX, f'Number os results: {len(responses)}')
    output = [response.to_dict() for response in responses]
    if args.output:
        with open(args.output, 'w') as file:
            file.write(json.dumps(output))
        print(PREFIX, f'File {args.output} generated with success!')


def warm_up():
    prefix = '[WARM UP]'
    required_environ_vars = ['PINECONE_API_KEY', 'ASSEMBLY_AI_API_KEY']
    errors = []
    for var in required_environ_vars:
        if not environ.get(var):
            errors.append(f'{var} is not set in the environment')
    if errors:
        print(prefix, 'Errors were found, aborting process.')
        for err in errors:
            print(prefix, err)
        raise Exception('Environment is not ready')


def main():
    warm_up()

    parser = argparse.ArgumentParser(description="CLI Tool")
    subparsers = parser.add_subparsers(dest='command')

    save_parser = subparsers.add_parser('save', help='Save array to file')
    save_parser.add_argument('-f', '--file', required=True, nargs='+', help='List of files path to transcribe')

    search_file_parser = subparsers.add_parser('search', help='Search array in file')
    search_file_parser.add_argument('-f', '--file', required=True,
                                    help='File path with vector (Using CSV to save time)')
    search_file_parser.add_argument('-m', '--metadata', nargs='+', help='Array of metadata strings')
    search_file_parser.add_argument('-k', '--top_k', default=2, help='Top K results')
    search_file_parser.add_argument('-o', '--output', default='output.json',
                                    help='Search output file (as a JSON)')

    args = parser.parse_args()

    if args.command == 'save':
        save_command(args)
    elif args.command == 'search':
        search_file_command(args)


if __name__ == "__main__":
    main()
