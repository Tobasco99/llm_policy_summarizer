from fastapi import FastAPI, File, HTTPException
from fastapi.responses import RedirectResponse
from service.splitter import load_and_split_text, vectorize_docs
from service.grobid import grobid_parse_pdf
from typing import Annotated

app = FastAPI()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.post("/documents/")
async def create_upload_file(file: Annotated[bytes, File()]):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    else:
        xml = grobid_parse_pdf(file)
        return {"xml": xml}

@app.post("/chunks/")
async def create_chunks(file: Annotated[bytes, File()], chunk_size: int, chunk_overlap: int, splitter_type: str):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    else:
        chunks = load_and_split_text(file, chunk_size, chunk_overlap, splitter_type)
        return {"chunks": chunks}
    
@app.post("/embeddings/", status_code=201)
async def create_embeddings(docs:list, vectorizer:str, openai_key:str| None = None, title:str = "dummy"):
    if vectorizer == "OpenAI Embeddings" and openai_key is None:
        raise HTTPException(status_code=400, detail="OpenAI key is required for OpenAI Embeddings.")
    vectorize_docs(docs, vectorizer, openai_key, title)
    return {"message": "Embeddings stored in weaviate database."}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
