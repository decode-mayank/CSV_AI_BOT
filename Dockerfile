FROM python:3.10.0

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY . /app

RUN pip install -r requirements.txt

RUN pip install virtualenv

RUN pip install flask

RUN pip install flask_smorest

RUN virtualenv venv

RUN /bin/bash -c "source venv/bin/activate"

EXPOSE 5000

CMD ["flask-ai/flask db upgrade", "python3", "flask-ai/app.py", "0.0.0.0:5000"]