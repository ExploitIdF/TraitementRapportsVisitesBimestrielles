# Python image to use.
FROM python:3.8-slim
WORKDIR /app
ENV DASH_DEBUG_MODE True
COPY requirements.txt .
RUN  pip install --upgrade pip
RUN set -ex &&  pip install  -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--reload", "app:server"]


