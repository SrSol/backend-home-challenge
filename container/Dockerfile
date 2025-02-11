# Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install awscli
RUN apt-get install -y jq

EXPOSE 8000

ENV USER app
ENV USER_HOME /opt/$USER


ADD app.tar $USER_HOME

WORKDIR $USER_HOME

RUN pip install -r requirements.txt

RUN mv container/run.sh .
RUN chmod +x run.sh

RUN useradd -r -d $USER_HOME $USER
RUN chown -R $USER:$USER $USER_HOME

USER $USER

ENV PYTHONPATH="${PYTHONPATH}:/opt/app"

CMD ["./run.sh"]
