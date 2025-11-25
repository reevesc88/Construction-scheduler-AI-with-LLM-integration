FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY .streamlit/ .streamlit/

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]