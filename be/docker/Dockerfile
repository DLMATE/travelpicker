FROM python:3.12-alpine

WORKDIR /travelpicker

COPY requirements.txt travelpicker ./
RUN pip install -r requirements.txt

CMD python main.py