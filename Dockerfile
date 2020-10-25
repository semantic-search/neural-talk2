FROM docker.pkg.github.com/semantic-search/neural-talk2/kafka-neural-talk:latest

RUN apt-get install -y python3-pip

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


# WORKDIR /neuraltalk2

COPY . .

CMD ["python3", "main.py"]