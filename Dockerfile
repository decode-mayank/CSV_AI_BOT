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

CMD ["python3", "flask_ai/app.py", "flask_ai/db.py", "0.0.0.0:5000"]