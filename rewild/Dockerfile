# Use the official Python image from the Docker Hub
FROM python:latest

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install gdal-bin libgdal-dev libsqlite3-mod-spatialite -y

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose the port the app will run on (optional, depending on your app)
EXPOSE 8000

# ENV SPATIALITE_LIBRARY_PATH=$(spatialite --version)

# Define the default command to run your application
CMD ["python", "manage.py", "runserver"]