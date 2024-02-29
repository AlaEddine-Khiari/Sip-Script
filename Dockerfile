FROM python:3.13.0a3-alpine3.19

# Set the working directory in the container
WORKDIR /app

# Copy the script and Flask application into the container at /app
COPY script.py app.py /app/

# Install Flask
RUN pip install Flask psycopg2-binary

# Expose the Flask port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
