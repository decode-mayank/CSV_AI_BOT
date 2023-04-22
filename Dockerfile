FROM python:3.10.0

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY ./requirements.txt /app/start.sh

COPY . /app

RUN pip install flask-smorest

RUN pip install -r requirements.txt

RUN pip install virtualenv

RUN virtualenv venv

RUN /bin/bash -c "source venv/bin/activate"

ENV PATH="/app:$PATH"

RUN chmod +x /app/start.sh

EXPOSE 5000

CMD ["start.sh", "0.0.0.0:5000"]