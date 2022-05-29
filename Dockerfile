# Pull base image
FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/app
RUN 

COPY . /home/app


# Set work directory so that next commands executes in /home/app dir
WORKDIR /home/app

# Install dependencies
RUN apt update -y 
RUN pip install -r requirements.txt
RUN apt install lsof -y
RUN apt install -y net-tools

EXPOSE 5000

CMD ["python", "__main__.py"]


