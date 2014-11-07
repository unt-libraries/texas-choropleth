FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update -qq && apt-get install -y python-mysqldb mysql-client nodejs npm imagemagick
RUN apt-get build-dep -y  phantomjs
RUN ln -s $(which nodejs) /usr/local/bin/node
RUN npm install -g less phantomjs uglify-js cssmin
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
