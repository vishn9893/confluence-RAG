#!/usr/bin/env python3
import logging
import os
from dotenv import load_dotenv
import truststore
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import ConfluenceLoader
from langchain.document_loaders.confluence import ContentFormat

from constants import *

load_dotenv()

truststore.inject_into_ssl()

# CONFLUENCE_TOKEN = os.getenv('CONFLUENCE_TOKEN')
# CONFLUENCE_USERNAME = os.getenv('CONFLUENCE_USERNAME')
# CONFLUENCE_BASE_URL = os.getenv('CONFLUENCE_BASE_URL')
# CONFLUENCE_SPACES_TO_LOAD = os.getenv('CONFLUENCE_SPACES_TO_LOAD')
# CONFLUENCE_MAX_PAGES_PER_SPACE = int(os.getenv('CONFLUENCE_MAX_PAGES_PER_SPACE', '10'))

# CONFLUENCE_CHUNK_SIZE = int(os.getenv('CONFLUENCE_CHUNK_SIZE', '1000'))
# CONFLUENCE_CHUNK_OVERLAP = int(os.getenv('CONFLUENCE_CHUNK_OVERLAP', '100'))

# CONFLUENCE_RETRIES = int(os.getenv('CONFLUENCE_RETRIES', '10'))
# CONFLUENCE_MIN_RETRY_S = int(os.getenv('CONFLUENCE_MIN_RETRY_S', '2'))
# CONFLUENCE_MAX_RETRY_S = int(os.getenv('CONFLUENCE_MAX_RETRY_S', '10'))
# SPACE_KEY = os.getenv('CONFLUENCE_SPACE_KEY')

def main():
    # embeddings
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CONFLUENCE_CHUNK_SIZE,
        chunk_overlap=CONFLUENCE_CHUNK_OVERLAP
    )

    # vectorstore
    db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)

    # logging.info(f"Reading spaces:{CONFLUENCE_SPACES_TO_LOAD} from {CONFLUENCE_BASE_URL}, limit {CONFLUENCE_MAX_PAGES_PER_SPACE} pages/space")
    loader = ConfluenceLoader(url=CONFLUENCE_BASE_URL, api_key=CONFLUENCE_TOKEN, username=CONFLUENCE_USERNAME, number_of_retries=CONFLUENCE_RETRIES, min_retry_seconds=CONFLUENCE_MIN_RETRY_S, max_retry_seconds=CONFLUENCE_MAX_RETRY_S)

    # for space in CONFLUENCE_SPACES_TO_LOAD:
    #     # Process one space at a time
    #     logging.info(f"Loading space {space}...")
    documents = loader.load(space_key=SPACE_KEY, content_format=ContentFormat.VIEW, max_pages=CONFLUENCE_MAX_PAGES_PER_SPACE)
    logging.info(f"Loaded {len(documents)} documents")
    texts = text_splitter.split_documents(documents)
    logging.info(f"Split into {len(texts)} chunks of text")

    # Save space embeddings
    db.add_documents(texts)
    db.persist()
    
    texts = None
    documents = None


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
    )
    main()