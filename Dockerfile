FROM python:3.7
EXPOSE 8080
WORKDIR /usr/src/app/
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]