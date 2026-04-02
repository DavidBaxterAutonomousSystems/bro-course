FROM python:3.12-slim

WORKDIR /site

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 8000

CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000", "--livereload"]
