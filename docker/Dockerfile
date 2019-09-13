FROM python:3.7.4 as airflow_builder

#RUN sh -c "echo \"BUILD ID: $(date '+%Y%m%d_%H%M%S')\" > /BUILD_ID"

ENV AIRFLOW_HOME=/home/airmariawork/airtest

COPY . /home/airmariawork

WORKDIR /home/airmariawork

# Install Airflow
RUN pip install -r requirements.txt

# Apparently initdb must be run once with the original airflow.cfg.
RUN /bin/bash -c "airflow initdb"

# default web server port is 8080
EXPOSE 8080

# Now overwrite default file to use MySQL backend, executor
# other than sequential.  Save the original first
RUN /bin/bash -c "cp ${AIRFLOW_HOME}/airflow.cfg ${AIRFLOW_HOME}/logs/airflow.cfg-original"
COPY ./my_airflow.cfg  /home/airmariawork/airtest/airflow.cfg

# Need to run initdb again with correct config.  That will be done
# during part of the RUN command when creating the container.
# Also at that time issue
#     airflow webserver -p 8080.
# and need airflow scheduler, either then or subsequently in exec, e.g.
# docker exec -d <container-name> /bin/sh -c "airflow scheduler"

#RUN /bin/bash -c "grep executor /home/airmariawork/airtest/airflow.cfg"
