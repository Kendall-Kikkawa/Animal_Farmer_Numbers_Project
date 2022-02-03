FROM python:3.8

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8050

ENTRYPOINT ["python3"]
CMD ["app.py"]