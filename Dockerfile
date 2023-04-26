FROM python:3.10.0

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY . /app

RUN pip install virtualenv

RUN virtualenv venv

RUN /bin/bash -c "source venv/bin/activate"

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "flask_ai/app.py", "0.0.0.0:5000"]