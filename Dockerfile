FROM python:3.11.0-slim-buster

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV FLASK_DEBUG=0

CMD [ "python3", "-m", "flask", "--app=src/app.py", "run", "--host=0.0.0.0"]
