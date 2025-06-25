FROM python:3.10-slim

WORKDIR /titan

COPY . /titan

RUN pip install --no-cache-dir \
    torch \
    transformers \
    numpy \
    scipy \
    faiss-cpu \
    websockets \
    cryptography \
    grpcio \
    scikit-learn

CMD ["python", "main.py"]
