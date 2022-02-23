FROM python:3.7-alpine
ENV HOME /home/root
ADD . $HOME
WORKDIR $HOME
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

