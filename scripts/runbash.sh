docker run -p 4001:8080 \
  -v /home/jrb/airmarialogs:/home/airmariawork/airtest \
  --name=airflow_maria   --network=net_airflow_maria \
  airflow_test/maria \
  /bin/sh 

#   --mount source=airflow-log-vol,target=/home/airmariawork/airtest \
