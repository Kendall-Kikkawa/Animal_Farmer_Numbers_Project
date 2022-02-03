FROM python:3.8

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt
RUN make /app

EXPOSE 8050

CMD python3 app.py