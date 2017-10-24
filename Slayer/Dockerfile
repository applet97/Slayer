FROM hypuk/dockerfile:python

ENV DJANGO_SETTINGS_MODULE = slayer.settings

ENV TZ = Asia/Almaty
RUN mkdir /db && mkdir /static && mkdir /photo && mkdir /django_logs

WORKDIR /code/slayer
COPY ./requirements.txt /code/slayer/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/slayer

CMD bash run.sh