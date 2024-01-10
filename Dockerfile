FROM python:3.8

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /authorz

# Install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Bundle app source
COPY . .

# Expose port
EXPOSE 5433

# entrypoint to run the django.sh file
ENTRYPOINT ["./django.sh"]
