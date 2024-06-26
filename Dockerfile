# demo/Dockerfile

FROM python:3.11-slim

WORKDIR /demo

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "--server.port=8501", "--server.address=0.0.0.0", "demo/chunk_demo.py"]

