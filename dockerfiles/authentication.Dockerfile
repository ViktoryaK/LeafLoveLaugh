FROM python:3.9-slim

COPY ./app/services/authentication/ /opt/lll/app/services/authentication/
COPY ./app/*.py /opt/lll/app/

RUN pip install fastapi psycopg2-binary passlib "uvicorn[standard]"

WORKDIR /opt/lll

ENTRYPOINT [ "uvicorn", "app.services.authentication.authentication:app", "--host", "0.0.0.0", "--port", "8080" ]
