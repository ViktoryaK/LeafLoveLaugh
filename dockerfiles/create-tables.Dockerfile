FROM cassandra:latest

WORKDIR /opt/lll/

COPY create-tables.sh ./
COPY create-tables.cql ./
COPY create-tables2.cql ./
COPY create-tables3.cql ./

RUN chmod u+x create-tables.sh


ENTRYPOINT ["bash", "-c", "/opt/lll/create-tables.sh"]
