From alpine:latest

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app

# Copy the script and Flask application into the container at /app
COPY script.py app.py /app/

RUN pip3 --no-cache-dir install Flask psycopg2-binary

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]

