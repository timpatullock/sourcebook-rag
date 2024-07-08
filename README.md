# sourcebook-rag

A small RAG which embeds pdfs into a Chroma DB and is then accessed via a light Streamlit UI.

### Installation

Ensure you have Python installed as well as any required buildchain tools.

Install the python dependencies under `requirements.txt`

`pip install -r requirements.txt`

Set up your environment the way you prefer, the repo assumes you're using dotenv so you can copy the `.env.example`

### Execution

If you're running a Chroma server, set it up how you wish, eg. [Docker](https://cookbook.chromadb.dev/running/running-chroma/).

If you choose not to run the Chroma server, it will create a local chroma cache in a `chroma` directory.

Insert any documents you wish under a `data` directory.

Create your database by populating it with `python ./create_collection.py`

Run your application with Streamlit using `streamlit run run.py`

You may add further documents to the database via the file picker and "Update"
