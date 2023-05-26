FROM python:3-alpine
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD fetcher.py .
CMD ["python", "./fetcher.py"]
