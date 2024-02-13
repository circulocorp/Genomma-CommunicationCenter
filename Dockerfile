FROM python:3.8

WORKDIR /genommaCommunicationCenter

COPY requirements.txt /genommaCommunicationCenter/
RUN pip install --no-cache-dir -r requirements.txt
ENV ENVIRONMENT development

COPY . /genommaCommunicationCenter/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
