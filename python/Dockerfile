FROM python:3.10.10-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN python init_db.py

CMD python main.py

