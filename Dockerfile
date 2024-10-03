FROM python:3

WORKDIR /workgpt

COPY *.py ./
COPY requirements.txt ./
COPY entrypoint.sh ./
RUN chmod +x ./entrypoint.sh
ADD  https://huggingface.co/unsloth/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf?download=true ./models/

# Streamlit
EXPOSE 8501

# python deps
RUN pip install --no-cache-dir -r requirements.txt

# download embeddings
RUN python3 ./init.py

# persistent vectorstore
VOLUME [ "./db" ]

ENTRYPOINT ["./entrypoint.sh"]