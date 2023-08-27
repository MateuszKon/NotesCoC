# start by pulling the python image
FROM python:3.10-slim-bullseye

# set the environment variable
ENV PYTHONPATH "${PYTHONPATH}:/app:/app/NotesApp"

RUN pip install --upgrade pip

# copy the requirements file into the image
COPY requirements.txt /app/NotesApp/requirements.txt

# switch working directory
WORKDIR /app/NotesApp

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY .. /app

RUN chmod +x /app/NotesApp/docker-entrypoint.sh

RUN echo /app/NotesApp/docker-entrypoint.sh

EXPOSE 8000

CMD ["/bin/bash" ,"/app/NotesApp/docker-entrypoint.sh"]
