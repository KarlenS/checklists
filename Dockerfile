FROM       ubuntu:latest

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

RUN echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.0.list

# Update apt-get sources AND install MongoDB
RUN apt-get update && apt-get install -y mongodb-org supervisor

RUN apt-get update && apt-get install -y mongodb-org mongodb-org-server mongodb-org-shell mongodb-org-mongos mongodb-org-tools

# Create the MongoDB and supervisor directory
RUN mkdir -p /data/db /var/log/supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


EXPOSE 3306
#EXPOSE 27017

#ENTRYPOINT ["/usr/bin/mongod"]

RUN apt-get install -y vim

RUN apt-get install -y python2.7

RUN apt-get install -y python-pip

#RUN curl https://bootstrap.pypa.io/get-pip.py

#RUN python get-pip.py

ADD . /code

WORKDIR /code

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8080
EXPOSE 5000

CMD ["/usr/bin/supervisord"]
#CMD ["python", "checklists.py", "&"]
