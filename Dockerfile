FROM python:3

WORKDIR /usr/local/projects
COPY requirements.txt .
RUN pip install -r requirements.txt


EXPOSE 8001
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
# gunicorn -w 3 -t 60 -b 127.0.0.1:8004 config.wsgi
CMD ["gunicorn", "-w", "3", "-t", "60", "-b", "0.0.0.0:8000", "config.wsgi"]

COPY . .