FROM orchardup/python:2.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update -qq && apt-get install -y python-mysqldb mysql-client nodejs npm
RUN ln -s $(which nodejs) /usr/local/bin/node
RUN npm install -g less
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
