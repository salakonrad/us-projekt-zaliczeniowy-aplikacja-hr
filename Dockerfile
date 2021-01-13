FROM python:3.8
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["flask"]
CMD ["run", "--host", "0.0.0.0"]
