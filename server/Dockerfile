# Sử dụng image chính thức của Python 3.12.7
FROM python:3.12.7-slim

# Cài đặt các thư viện yêu cầu
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

