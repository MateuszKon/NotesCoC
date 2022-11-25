# start by pulling the python image
FROM python:3.10-slim-bullseye

RUN pip install --upgrade pip

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

RUN chmod +x /app/docker-entrypoint.sh

RUN echo /app/docker-entrypoint.sh

EXPOSE 8000

CMD ["/bin/bash" ,"/app/docker-entrypoint.sh"]
