FROM python:3.12-slim
WORKDIR /LibraryManagement
COPY . /LibraryManagement

CMD ["python3", "main.py"]