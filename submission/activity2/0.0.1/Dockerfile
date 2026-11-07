FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY app.py database.db ./
EXPOSE 5000
CMD ["python", "app.py"]
