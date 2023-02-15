# start from base
FROM ubuntu:20.04

# install system-wide deps for python and node
RUN apt-get -yqq update
RUN apt-get -yqq install python3-pip python3-dev 

# copy our application code
ADD book_app /opt/book_app
WORKDIR /opt/book_app

# fetch app specific deps
RUN pip3 install -r requirements.txt

# expose port
EXPOSE 8080

# start app
CMD [ "python3", "./server.py" ]
