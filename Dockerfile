# Python image to use.
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Needs libcairo for PNG rendering
RUN apt update && apt install -y libcairo2

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Run app.py when the container launches
ENTRYPOINT ["python", "app.py"]
