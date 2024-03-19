import requests
import xml.etree.ElementTree as ET
import eurlex
import os
from dotenv import load_dotenv
from typing import List, Dict


def get_html_by_title (title: str) -> str: 
    """Retrieve a html string based on the title of a document

    Parameters
    ----------
    title : str
        The title of the document for expert search.

    Returns
    -------
    str
        an html string of the requested document.
    """

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
    


def get_documents_date_range(start: str, end: str, types: List[str] = ["REG"], limit: int = -1) -> List[Dict[str, str]]:
    """Retrieve a list of documents of specified types from EUR-Lex that have a CELEX-number and a publication date within a specified range, as a list of dicts.

    Parameters
    ----------
    start : str
        Start date of the date range in the format 'YYYY-MM-DD'.
    end : str
        End date of the date range in the format 'YYYY-MM-DD'.
    types : List[str]
        The by the SparQL-API recognized type of documents to return.
        Examples: ["DIR", "DIR_IMPL", "DIR_DEL", "REG", "REG_IMPL", "REG_FINANC", "REG_DEL"]
    limit : int
        The maximum number of regulations to retrieve. (default: no limit).

    Returns
    -------
    List[dict]
        A list of dicts, containing publication date, publication URL, CELEX number, and type of document.
    """
    query  = "SELECT DISTINCT ?doc ?type ?celex ?date\n"
    query += "WHERE {\n"
    query += "  ?doc cdm:work_has_resource-type ?type.\n"
    query += "  FILTER (\n"
    query += "    " + " ||\n    ".join([f"?type=<http://publications.europa.eu/resource/authority/resource-type/{type}>" for type in types]) + "\n"
    query += "  )\n"
    query += "  FILTER (BOUND(?celex))\n"
    query += "  FILTER (BOUND(?date))\n"  # Exclude documents without a date
    query += "  OPTIONAL {?doc cdm:resource_legal_id_celex ?celex.}\n"
    query += "  OPTIONAL {?doc cdm:work_date_document ?date.\n"
    query += "             FILTER (?date >= '" + start + "'^^<http://www.w3.org/2001/XMLSchema#date> && ?date <= '" + end + "'^^<http://www.w3.org/2001/XMLSchema#date>)}\n"
    query += "}\n"
    if limit > 0:
        query += "LIMIT " + str(limit)

    results = []
    query_results = eurlex.run_query(eurlex.prepend_prefixes(query))
        
    for result in query_results["results"]["bindings"]:
        results.append({
            "celex": result.get("celex", {}).get("value", ""),
            "date": result.get("date", {}).get("value", ""),
            "link": result.get("doc", {}).get("value", ""),
            "type": result.get("type", {}).get("value", "").split("/")[-1]
        })

    return results