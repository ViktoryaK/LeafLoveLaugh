FROM python:3.9-slim

COPY ./app/services/facade/ /opt/lll/app/services/facade/
COPY ./app/*.py /opt/lll/app/
COPY ./app/services/facade/templates /opt/lll/app/services/facade/templates

RUN pip install fastapi requests "uvicorn[standard]"

WORKDIR /opt/lll

ENTRYPOINT [ "uvicorn", "app.services.facade.facade:app", "--host", "0.0.0.0", "--port", "8080"]
