FROM python:3.11.9-alpine3.20

WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev \
    && pip install --upgrade pip 

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

COPY /pdfserializer-firebase-adminsdk-dg309-3fe1c3e6df.json /app/pdfSerializer/

CMD [ "python" , "manage.py", "runserver", "0.0.0.0:8000" ]

