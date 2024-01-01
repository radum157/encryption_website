# An alpine image is used
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 80 for the Flask server
EXPOSE 80

# Set the Flask environment variable
ENV FLASK_APP=server.py

# Start the Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
