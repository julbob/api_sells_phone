FROM python:3.9.16

COPY src/ /src/
COPY app.py /
COPY requirements.txt /
RUN pip install -r ./requirements.txt

EXPOSE 8080

CMD ["python3", "-u", "/app.py"]