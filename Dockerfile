FROM alpine:latest

# Install necessary packages
RUN apk add --no-cache python3 python3-dev py3-pip

# Set working directory
WORKDIR /app

# Copy script.py and app.py to the working directory
COPY script.py app.py /app/

# Create and activate a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Flask and psycopg2-binary within the virtual environment
RUN pip install Flask psycopg2-binary

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
