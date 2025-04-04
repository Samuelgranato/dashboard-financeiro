# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app .

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]
