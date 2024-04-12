import weaviate
import weaviate.classes as wvc
import os
from dotenv import load_dotenv, find_dotenv
import requests

class WeaviateConnection:
    """
    A class representing a connection to the Weaviate database.

    This class provides methods to store embeddings, chunks, and titles in a Weaviate database.
    """

    def __init__(self):
        """
        Initializes the WeaviateConnection object.

        Retrieves the Weaviate URL and token from environment variables.
        """
        # get from env
        load_dotenv(find_dotenv())
        self.weaviate_url = os.environ.get("WEAVIATE_URL")
        self.weaviate_token = os.environ.get("WEAVIATE_TOKEN")

    def store_embeddings(self, embeddings:list, chunks:list, title:str):
        """
        Store the embeddings, chunks, and title in a Weaviate database.

        Args:
            embeddings (list): A list of embeddings.
            chunks (list): A list of chunks.
            title (str): The title of the document.

        Returns:
            None
        """
        try:
            objects = []
            for i, chunk in enumerate(chunks):
                object_props = {
                    "class": "Policy",
                    "properties": {
                        "chunk": chunk,
                        "title": title,
                        "vector": embeddings[i]
                    }
                }
                objects.append(object_props)

            payload = {"objects": objects}
            with requests.Session() as session:
                response = session.post(f"{self.weaviate_url}/v1/batch/objects?consistency_level=QUORUM", 
                                        json=payload, headers={"Authorization": f"Bearer {self.weaviate_token}"})
                response.raise_for_status()
                print(response.json)
        except Exception as e:
            print(f"Error storing embeddings: {e}")
