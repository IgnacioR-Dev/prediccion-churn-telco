FROM python:3.14
WORKDIR /app

COPY src/ml/requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt
# pip install python-dotenv
# sqlalchemy 
# pandas
COPY src/ .
ENV PYTHONPATH=/app

CMD ["python", "ml/main.py"]


