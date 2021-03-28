FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate
RUN python manage.py mock_data

CMD [ "sh" , "-c" , "python manage.py runserver 0.0.0.0:3000" ]

EXPOSE 3000