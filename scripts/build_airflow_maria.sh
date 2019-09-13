# Typically direct output to log file
#!/bin/sh
cd /home/jrb/airflow_maria
if [-z ${1} ]; then
    docker build -t airflow_maria_i  .
else
    docker build -t airflow_maria_i:${1}  .
    docker tag airflow_maria_i:${1} airflow_maria_i:latest
fi

