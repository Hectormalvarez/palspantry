FROM python:3.11-alpine

WORKDIR /app

COPY requirements*.txt ./

RUN pip install -r requirements.dev.txt

COPY . ./ 

CMD ["python", "src/bot_main.py"]
