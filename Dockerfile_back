FROM gcr.io/google_appengine/python 

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "checklists.py"]

