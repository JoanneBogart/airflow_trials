docker run -p 4001:8080 \
  -v /home/jrb/airmarialogs:/home/airmariawork/airtest/logs \
  -v /home/jrb/airmariadags:/home/airmariawork/airtest/dags \
  --name=airflow_maria -d  --network=net_airflow_maria \
  airflow_maria_i \
  /bin/sh -c "(airflow initdb) && (airflow webserver -p 8080)"

# It's not possible to also start scheduler here.  Do it as a
# separate docker exec:

# docker exec -d airflow_maria /bin/sh -c "airflow scheduler"

#   --mount source=airflow-log-vol,target=/home/airmariawork/airtest/logs \
# image name had been airflow_test/maria
