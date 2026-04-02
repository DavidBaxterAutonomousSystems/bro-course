FROM python:3.12-slim

WORKDIR /site

RUN pip install --no-cache-dir mkdocs

EXPOSE 8000

CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000", "--livereload"]
