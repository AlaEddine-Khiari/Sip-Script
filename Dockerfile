FROM python:3.13.0a3-alpine3.19

# Set the working directory in the container
WORKDIR /app

# Copy the script and Flask application into the container at /app
COPY script.py app.py /app/

# Setu up Image
RUN pip install psycopg2-binary==2.7.4
RUN pip install Flask 
# Expose the Flask port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
