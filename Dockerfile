FROM node:18-alpine AS build

COPY /vite/package.json /app/vite/package.json

WORKDIR /app/vite

RUN npm install

RUN npm i -g serve

COPY /vite /app/vite

RUN npm run build



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

COPY --from=build /app/vite/dist/assets/index-*.js /app/static/js/index-*.js

CMD ["/bin/bash" ]

#
## rebuild front-end
#WORKDIR /app/vite
#RUN npm run build
#
##RUN chmod +x /app/docker-entrypoint.sh
##
##RUN echo /app/docker-entrypoint.sh
##
##EXPOSE 8000

#CMD ["/bin/bash" ,"/app/docker-entrypoint.sh"]
