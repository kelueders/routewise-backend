FROM python:3.11.9-bullseye

COPY . .

RUN apt-get update -y
RUN pip install -r requirements.txt \
    && pip install scipy \
    && pip install numpy

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]