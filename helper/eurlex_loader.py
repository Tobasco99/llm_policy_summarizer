import requests
import xml.etree.ElementTree as ET
from eurlex import get_html_by_celex_id
import os
from dotenv import load_dotenv

load_dotenv()

EURLEX_USER = os.getenv('EURLEX_USER')
EURLEX_PW = os.getenv('EURLEX_PW')
EURLEX_URL = os.getenv('EURLEX_URL')
query =  "Titel ~ {}"

headers = {
    "Content-Type": "application/soap+xml;charset=UTF-8",
}
 
payload = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
            <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sear="http://eur-lex.europa.eu/search">
    <soap:Header>
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" soap:mustUnderstand="true">
            <wsse:UsernameToken xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="UsernameToken-1">
                <wsse:Username>{}</wsse:Username>
                <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{}</wsse:Password>
            </wsse:UsernameToken>
        </wsse:Security>
    </soap:Header>
    <soap:Body>
        <sear:searchRequest>
            <sear:expertQuery>
                <![CDATA[{}]]>
            </sear:expertQuery>
            <sear:page>1</sear:page>
            <sear:pageSize>1</sear:pageSize>
            <sear:searchLanguage>en</sear:searchLanguage>
        </sear:searchRequest>
    </soap:Body>
</soap:Envelope>"""

def get_html_by_title (title: str) -> str: 
    '''
    Returns a html string of the document with the given title.

            Parameters:
                    title: The title of the requested document

            Returns:
                    html_string: the requested html document or empty if none found
    '''
    response = requests.request("POST", EURLEX_URL, headers=headers, data=payload.format(EURLEX_USER, EURLEX_PW, query.format(title)))

    if response.status_code != 200:
        raise Exception("Error accessing EUR-Lex service:" + response.status_code)
        

    namespaces = {
        'soap': 'http://www.w3.org/2003/05/soap-envelope',
        'sear': 'http://eur-lex.europa.eu/search'
    }

    root = ET.fromstring(response.text)
    celex_element = root.find('.//sear:ID_CELEX', namespaces) 

    celex_value = celex_element[0].text if celex_element is not None else None

    if celex_value is not None:
        html_string = get_html_by_celex_id(celex_value)   
        return html_string

    else:
        return ""