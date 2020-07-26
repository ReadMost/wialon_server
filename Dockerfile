FROM python:3.6

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

#COPY . /usr/src/app

EXPOSE 8053
COPY . .
#RUN adduser --disabled-password --gecos '' myuser
CMD ["python3", "-u", "server.py"]