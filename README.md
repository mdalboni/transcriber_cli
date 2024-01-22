# README.md

## Summary

This project is a Python-based application that provides a command-line interface (CLI) for transcribing video files
into text and saving the transcriptions in a vector database. It uses the AssemblyAI API for transcribing and provides
functionalities for saving and searching transcriptions.

## Required Resources
1. Create a pinecone account -> https://www.pinecone.io/
   1. Create an index:
   2. Index config: 
   ![readme_assets/img.png](readme_assets/img.png)
   3. Get your API_KEY by clicking on connect:
   ![readme_assets/img_1.png](readme_assets/img_1.png)
2. Create your AssemblyAi account -> https://www.assemblyai.com/
   1. Get your API_KEY on the home page.

## Installation

To install the project, follow these steps:  
Obs: The project was done with Python 3.9

1. Clone the repository:
    ```
    git clone https://github.com/mdalboni/transcriber_cli.git
    ```
2. Navigate to the project directory:
    ```
    cd transcriber_cli
    ```
3. Install the required Python packages using your virtual env:
    ```
    pip install -r requirements.txt
    ```
4. Set the required environment variables:
    ```
    export ASSEMBLY_AI_API_KEY=your_assembly_ai_api_key
    export PINECONE_API_KEY=your_pinecone_api_key
    ```

## Execution

To execute the project, you can use the following commands:

- To save transcriptions on the cloud:
    ```
    python main.py save -f <file_paths>
    example:
    python main.py save -f yt_short.mp4
    ```
- To search for a vector from a file:
    ```
    python main.py search -f <file_path> -m <metadata> -k <top_k> -o <output_file>
    example:
    python main.py search -f test.csv -m one two -k 2 -o output.json
    ```

Replace `<file_paths>`, `<file_path>`, `<metadata>`, `<top_k>`, and `<output_file>` with your actual values.


## Details and other information


### Topic Extractor
The topic extractor does everything in one batch, so if you upload multiple files, they will get into the same topic extraction.  
I could fix this by splitting the process for each file, but due to my lack of time and knowing this would increase the execution 
time by a ton for larger file groups, so in the end I did not implement this change.


### I am not a ML Engineer
Because of this I cannot confirm if the vectors and metadata search are the best. Also, I am not able to decide which vector 
size is more suitable for the experiment.
