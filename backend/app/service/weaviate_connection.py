import os
from dotenv import load_dotenv, find_dotenv
import requests

class WeaviateConnection:
    """
    A class representing a connection to the Weaviate database.

    This class provides methods to store embeddings, chunks, and titles in a Weaviate database.
    """

    def __init__(self, schema_name: str = "Policy", schema_name_knowledge: str = "Policy_Knowledge"):
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
        self.schema_name_knowledge = schema_name_knowledge
        if not self.weaviate_url or not self.weaviate_token:
            raise ValueError("Weaviate URL or token is missing, please specify in .env file.")
        # check for database and schema
        if not self.__is_existing():
            raise ValueError("Weaviate database does not exist")
        if not self.__is_schema_existing():
            print("Schema does not exist, creating schema...")
            self.__create_schema()
        if not self.__is_schema_existing(self.schema_name_knowledge):
            print("Schema knowledge does not exist, creating schema...")
            self.__create_schema_knowledge()

    def get_knowledge(self, slash_notation:str):
        """
        Retrieves the knowledge from the Weaviate database using a GraphQL query.

        Args:
            slash_notation (str): The slash notation of the policy document.

        Raises:
            Exception: If there is an error retrieving the knowledge.

        Returns:
            str: The abstract of the policy document.
        """
        try:
            query = '''
            {
              objects(where: {class: "%s", slash_notation: "%s"}) {
                abstract
              }
            }
            ''' % (self.schema_name_knowledge, slash_notation)
            payload = {
                "operationName": "",
                "query": query,
                "variables": {}
            }
            with requests.Session() as session:
                response = session.post(f"{self.weaviate_url}/v1/graphql", json=payload, headers={"Authorization": f"Bearer {self.weaviate_token}"})
                response.raise_for_status()
                response_json = response.json()
                knowledge = response_json["data"]["objects"][0]["abstract"]
                return knowledge
        except Exception:
            print(f"Entity not found: {slash_notation}")
            return None


    def store_knowledge(self, slash_notation:str, abstract:str):
        """
        Stores the knowledge in the Weaviate database.

        Args:
            slash_notation (str): The slash notation of the policy document.
            abstract (str): The abstract of the policy document.

        Raises:
            Exception: If there is an error storing the knowledge.

        Returns:
            None
        """
        try:
            object_props = {
                "class": self.schema_name_knowledge,
                "properties": {
                    "slash_notation": slash_notation,
                    "abstract": abstract
                }
            }
            payload = {"objects": [object_props]}
            with requests.Session() as session:
                response = session.post(f"{self.weaviate_url}/v1/batch/objects?consistency_level=ALL", 
                                        json=payload, headers={"Authorization": f"Bearer {self.weaviate_token}"})
                response.raise_for_status()
        except Exception as e:
            print(f"Error storing knowledge: {e}")  

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
                        "position": i,            
                    },
                    "vectors": {
                        vectorizer: embeddings[i]
                    }
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
        
    def __is_schema_existing(self, schema_name: str = "Policy"):
        """
        Check if the Weaviate database collection is existing.

        Returns:
            bool: True if the schema exists, False otherwise.
        """
        try:    
            with requests.Session() as session:
                response = session.get(f"{self.weaviate_url}/v1/schema/{schema_name}", headers={"Authorization": f"Bearer {self.weaviate_token}"})  
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
                    "class": self.schema_name,
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
                            "dataType": "int",
                            "description": "The position of the chunk in the policy document",
                            "name": "position"
                        },
                    ]
                }
                response = session.post(f"{self.weaviate_url}/v1/schema", json=schema, headers={"Authorization": f"Bearer {self.weaviate_token}"})
                response.raise_for_status()
        except Exception as e:
            print(f"Error creating schema: {e}")

    def __create_schema_knowledge(self):
        """
        Create the Weaviate database schema.

        Returns:
            None
        """
        try:
            with requests.Session() as session:
                schema = {
                    "class": self.schema_name_knowledge,
                    "description": "Abstract of a policy document",
                    "properties": [
                        {
                            "dataType": ["text"],
                            "description": "Slash notation of the policy",
                            "name": "slash_notation"
                        },
                        {
                            "dataType": ["text"],
                            "description": "An abstract of the policy document",
                            "name": "abstract"
                        },
                    ]
                }
                response = session.post(f"{self.weaviate_url}/v1/schema", json=schema, headers={"Authorization": f"Bearer {self.weaviate_token}"})
                response.raise_for_status()
        except Exception as e:
            print(f"Error creating schema: {e}")
