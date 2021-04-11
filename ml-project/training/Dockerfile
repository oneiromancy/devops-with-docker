FROM python:3.6.7-slim

WORKDIR /src

COPY . .

RUN pip install --upgrade pip && pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "-u", "train.py"]
