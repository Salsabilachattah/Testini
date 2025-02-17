FROM python:3.12-slim

RUN pip install Flask==3.0.3 Werkzeug==3.0.3 

WORKDIR /app

COPY . /app

RUN chmod +r  -R /app

RUN chmod 777 /app/BLIND_CHALLENGE.db

USER nobody

CMD ["python","app.py"]
