from typing import List, Any, Dict, TypedDict
from io import StringIO, BytesIO
import requests

class ElementType(TypedDict):
    """Element type as typed dict."""

    url: str
    xpath: str
    content: str
    metadata: Dict[str, str]

class XMLTagTextSplitter:
    """
    Splitting HTML/XML files based on two tags.
    Requires lxml package.
    """

    def __init__(
        self,
        max_chunk_size: int, 
        first_tag: str, 
        second_tag: str,
        return_each_element: bool = False,
    ):
        """Create a new XMLTagTextSplitter.

        Args:
            max_chunk_size: maximum size of resulting chunks.
            first_tag: the primary tag to split on.
            second_tag: the fallback tag to split on if the chunk size is too large.
            return_each_element: Return each element w/ associated tags.
        """
        # Output element-by-element or aggregated into chunks w/ common tags
        self.return_each_element = return_each_element
        self.max_chunk_size = max_chunk_size
        self.first_tag = first_tag
        self.second_tag = second_tag

    def aggregate_elements_to_chunks(
        self, elements: List[Dict[str, str]]
    ) -> List[str]:
        """Combine elements with common tags into chunks

        Args:
            elements: Content with associated identifying info and tags
        """
        aggregated_chunks: Dict[str, str] = {}

        for element in elements:
            for tag in element["tags"]:
                if tag in aggregated_chunks:
                    aggregated_chunks[tag] += "\n" + element["content"]
                else:
                    aggregated_chunks[tag] = element["content"]

        return list(aggregated_chunks.values())

    def split_text_from_url(self, url: str) -> List[str]:
        """Split HTML/XML from web URL

        Args:
            url: web URL
        """
        r = requests.get(url)
        return self.split_text_from_file(BytesIO(r.content))

    def split_text(self, text: str) -> List[str]:
        """Split HTML/XML text string

        Args:
            text: HTML/XML text
        """
        return self.split_text_from_file(StringIO(text))

    def split_text_from_file(self, file: Any) -> List[str]:
        try:
            from lxml import etree
        except ImportError as e:
            raise ImportError(
                "Unable to import lxml, please install with `pip install lxml`."
            ) from e

        parser = etree.XMLParser(encoding="utf-8")
        tree = etree.parse(file, parser)

        # Define namespace mappings
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}

        # Initialize list to store chunks
        chunks = []

        # Retrieve elements based on the first tag
        first_tag_xpath_expr = f'//tei:{self.first_tag}'
        first_tag_elements = tree.xpath(first_tag_xpath_expr, namespaces=ns)

        # Loop through each element of the first tag to split on
        for first_tag_element in first_tag_elements:
            # Convert the element to a string and get its size
            first_tag_element_str = etree.tostring(first_tag_element, encoding=str)
            chunk_size = len(first_tag_element_str)

            # If the chunk size is smaller than max_chunk_size, add it to chunks
            if chunk_size <= self.max_chunk_size:
                chunks.append(first_tag_element_str)
            else:
                # Split the chunk based on the second tag until each chunk size is smaller than max_chunk_size
                second_tag_xpath_expr = f'.//tei:{self.second_tag}'
                second_tag_elements = first_tag_element.xpath(second_tag_xpath_expr, namespaces=ns)

                for second_tag_element in second_tag_elements:
                    # Convert the second tag element to a string
                    second_tag_element_str = etree.tostring(second_tag_element, encoding=str).strip()
                    # Check if adding this chunk exceeds max_chunk_size, if not, add it to chunks
                    if len(chunks[-1]) + len(second_tag_element_str) <= self.max_chunk_size:
                        chunks[-1] += second_tag_element_str
                    else:
                        # If adding this chunk exceeds max_chunk_size, start a new chunk
                        chunks.append(second_tag_element_str)

        return chunks
