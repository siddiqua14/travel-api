# Use the official Python image from Docker Hub
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app
COPY ./app /app
# Copy the requirements file into the container
COPY requirements.txt .
RUN python3 --version
RUN pip3 --version
# Install dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
