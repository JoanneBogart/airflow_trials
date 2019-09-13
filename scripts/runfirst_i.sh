docker run -p 4001:8080 \
  -v /home/jrb/airmarialogs:/home/airmariawork/airtest/logs \
  -v /home/jrb/airmariadags:/home/airmariawork/airtest/dags \
  --name=airflow_maria -a stdout -a stderr  --network=net_airflow_maria \
  airflow_maria_i \
  /bin/sh -c "(airflow initdb) && (airflow webserver -p 8080)"
