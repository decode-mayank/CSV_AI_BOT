FROM python:3.10.0


WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY . /app

RUN pip install -r requirements.txt

RUN pip install virtualenv

RUN virtualenv venv

RUN /bin/bash -c "source venv/bin/activate"

EXPOSE 8000

CMD ["python3", "examples/chatbot-framework/discord_bot.py", "0.0.0.0:8000"]