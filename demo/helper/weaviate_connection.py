import os
from dotenv import load_dotenv, find_dotenv
import requests

class WeaviateConnection:
    """
    A class representing a connection to the Weaviate database.

    This class provides methods to store embeddings, chunks, and titles in a Weaviate database.
    """

    def __init__(self, schema_name: str = "Policy"):
        """
        Initializes a WeaviateConnection object.

        Args:
            schema_name (str, optional): The name of the schema to be used in Weaviate. Defaults to "Policy".

        Raises:
            ValueError: If the Weaviate URL or token is missing.
            ValueError: If the Weaviate database does not exist.
        """
        # get from env
        load_dotenv(find_dotenv())
        self.weaviate_url = os.environ.get("WEAVIATE_URL")
        self.weaviate_token = os.environ.get("WEAVIATE_TOKEN")
        self.schema_name = schema_name
        if not self.weaviate_url or not self.weaviate_token:
            raise ValueError("Weaviate URL or token is missing, please specify in .env file.")
        # check for database and schema
        if not self.__is_existing():
            raise ValueError("Weaviate database does not exist")
        if not self.__is_schema_existing():
            print("Schema does not exist, creating schema...")
            self.__create_schema()
        

    def store_embeddings(self, embeddings:list, chunks:list, title:str, vectorizer:str):
        """
        Stores the embeddings of chunks in the Weaviate database.

        Args:
            embeddings (list): A list of embeddings corresponding to each chunk.
            chunks (list): A list of chunks to be stored.
            title (str): The title associated with the chunks.
            vectorizer (str): The name of the vectorizer used to generate the embeddings.

        Raises:
            Exception: If there is an error storing the embeddings.

        Returns:
            None
        """
        try:
            objects = []
            for i, chunk in enumerate(chunks):
                object_props = {
                    "class": self.schema_name,
                    "properties": {
                        "chunk": chunk,
                        "title": title,
                        "vectorizer": vectorizer,
                    },
                    "vector": embeddings[i],
                }
                objects.append(object_props)

            payload = {"objects": objects}
            with requests.Session() as session:
                response = session.post(f"{self.weaviate_url}/v1/batch/objects?consistency_level=ALL", 
                                        json=payload, headers={"Authorization": f"Bearer {self.weaviate_token}"})
                response.raise_for_status()
        except Exception as e:
            print(f"Error storing embeddings: {e}")

    def __is_existing(self):
        """
        Check if the Weaviate database is existing.

        Returns:
            bool: True if the database exists, False otherwise.
        """
        try:
            with requests.Session() as session:
                response = session.get(f"{self.weaviate_url}/v1/meta", headers={"Authorization": f"Bearer {self.weaviate_token}"})
                response.raise_for_status()
                return True
        except Exception as e:
            return False
        
    def __is_schema_existing(self):
        """
        Check if the Weaviate database collection is existing.

        Returns:
            bool: True if the schema exists, False otherwise.
        """
        try:    
            with requests.Session() as session:
                response = session.get(f"{self.weaviate_url}/v1/schema/Policy", headers={"Authorization": f"Bearer {self.weaviate_token}"})  
                response.raise_for_status()
                return True
        except Exception as e:
            return False
        
    def __create_schema(self):
        """
        Create the Weaviate database schema.

        Returns:
            None
        """
        try:
            with requests.Session() as session:
                schema = {
                    "class": "Policy",
                    "description": "A policy document",
                    "properties": [
                        {
                            "dataType": ["text"],
                            "description": "Title of the policy",
                            "name": "title"
                        },
                        {
                            "dataType": ["text"],
                            "description": "A chunk of text of the policy document",
                            "name": "chunk"
                        },
                        {
                            "dataType": ["text"],
                            "description": "The vectorizer used to generate the embeddings",
                            "name": "vectorizer"
                        }
                    ]
                }
                response = session.post(f"{self.weaviate_url}/v1/schema", json=schema, headers={"Authorization": f"Bearer {self.weaviate_token}"})
                response.raise_for_status()
        except Exception as e:
            print(f"Error creating schema: {e}")
