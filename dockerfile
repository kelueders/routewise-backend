FROM python:3.12-bullseye

COPY . .

RUN apt-get update -y
RUN pip install -r requirements.txt \
    && pip install scipy \
    && pip install numpy

CMD ["flask", "run"]