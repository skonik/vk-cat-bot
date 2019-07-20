FROM python:3.7-alpine3.7

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python3", "source/main.py"]