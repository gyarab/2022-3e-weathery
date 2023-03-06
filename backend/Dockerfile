FROM python:3.10

WORKDIR /

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--port", "5000"]

