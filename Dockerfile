# Use the official Python image from the Docker Hub
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose the port the app will run on (optional, depending on your app)
# EXPOSE 5000

# Define the default command to run your application
# CMD ["python", "app.py"]