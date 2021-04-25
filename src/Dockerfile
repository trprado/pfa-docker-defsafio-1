FROM python:3.8-alpine


WORKDIR /src/

COPY . .
RUN pip install -r requirements.txt

CMD [ "python", "-u", "server.py" ]

EXPOSE 8000
