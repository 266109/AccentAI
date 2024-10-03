# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy the project files to the container
COPY . /app/

# Step 5: Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 6: Install Nginx
RUN apt-get update && apt-get install -y nginx

# Step 7: Copy the Nginx configuration file
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Step 8: Collect static files (Django command)
RUN python manage.py collectstatic --noinput

# Step 9: Expose port 8000 for Gunicorn
EXPOSE 3000

# Step 10: Command to run both Gunicorn and Nginx
CMD ["sh", "-c", "service nginx start && gunicorn AccentAI.wsgi:application --bind 0.0.0.0:3000"]
