FROM python:3.10.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./saved_models ./src ./

EXPOSE 5000

ENV FLASK_DEBUG=0

CMD [ "python3", "-m", "flask", "--app=src/app.py", "run", "--host=0.0.0.0"]
