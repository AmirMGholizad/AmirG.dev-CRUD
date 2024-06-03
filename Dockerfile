FROM python:3.9.7

WORKDIR usr/src/app

COPY requirements.txt ./

RUN cat requirements.txt | xargs -n 1 pip install --no-cache-dir

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "8000"]
