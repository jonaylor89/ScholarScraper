
# install base image
FROM node

# set working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/package.json

RUN npm install
RUN npm install -g @angular/cli

# add app
COPY . /usr/src/app

EXPOSE 4200

# ng build
RUN ng build

# start app
CMD ng serve

