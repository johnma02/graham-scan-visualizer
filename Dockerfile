FROM python:3.9.7
SHELL ["/bin/bash", "-c"]
WORKDIR /app/api

COPY app.py ./
COPY requirements.txt convexhull.py ./
ENV FLASK_ENV production

EXPOSE 8000

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", ":8000", "app:app"]
