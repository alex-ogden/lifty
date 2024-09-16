# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 4848 available to the world outside this container
EXPOSE 4848

# Define environment variables
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

# Run run.py when the container launches
CMD ["python", "run.py"]