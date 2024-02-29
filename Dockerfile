From alpine:latest

RUN apk add --no-cache python3 python3-dev py3-pip

WORKDIR /app

# Copy the script and Flask application into the container at /app
COPY script.py app.py /app/

RUN pip3 install Flask psycopg2-binary

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]

