### Instructions for initializing Flask App container

FROM python:3.6.1

# Set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Add requirements (Leverages Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# Install requirements
RUN pip install -r requirements.txt

# Add app to root
ADD . /usr/src/app

# Run server (Set host to 0.0.0.0)
CMD python manage.py runserver -h 0.0.0.0
