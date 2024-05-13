from typing import List, Any, Dict, TypedDict
from io import StringIO, BytesIO
import requests

class ElementType(TypedDict):
    """Element type as typed dict."""

    url: str
    xpath: str
    content: str
    metadata: Dict[str, str]

class XMLSentenceSplitter:
    """
    Splitting HTML/XML files based on specified custom tags.
    Requires lxml package.
    """

    def __init__(
        self,
        tags_to_split_on: List[str],
        return_each_element: bool = False,
    ):
        """Create a new XMLSentenceSplitter.

        Args:
            tags_to_split_on: list of custom tags we want to track for splitting.
            return_each_element: Return each element w/ associated tags.
        """
        # Output element-by-element or aggregated into chunks w/ common tags
        self.return_each_element = return_each_element
        self.tags_to_split_on = tags_to_split_on

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

        # Loop through each tag to split on
        for tag in self.tags_to_split_on:
            # Retrieve elements based on the current tag
            tag_name = tag[0]
            xpath_expr = f'//tei:{tag_name}'
            elements = tree.xpath(xpath_expr, namespaces=ns)
            
            # Loop through each element and add it as a new chunk
            for element in elements:
                # Convert the element to a string and add it to chunks
                chunks.append(etree.tostring(element, encoding=str))

        return chunks



# Example usage:
if __name__ == "__main__":
    splitter = XMLSentenceSplitter(tags_to_split_on=["head", "p", "table"])
    html_file_path = "your_file.html"  # Change this to your HTML/XML file path
    result = splitter.split_text_from_file(html_file_path)
    print(result)
