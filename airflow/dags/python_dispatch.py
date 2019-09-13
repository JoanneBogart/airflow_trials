# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import print_function

import time
from builtins import range
from pprint import pprint
from datetime import datetime, timedelta
import logging

import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator

args = {
    'owner': 'jrb',
    'start_date': datetime(2018, 1, 1),
}

kwdict =  {'msgs' : ['file1.parquet', 'file2.parquet','file3.parquet']}

dag = DAG(
    dag_id='python_dispatch',
    default_args=args,
    schedule_interval=timedelta(days=1),
)



def push(msg, **kwargs):
    logging.info('about to return ' + msg)
    return msg

def munge(upstream, **kwargs):
    msg_passed = kwargs['task_instance'].xcom_pull(task_ids=upstream)
    logging.info('retrieved msg ' + msg_passed)
    
    
def subdispatcher(parent_dag, child_dag, args, **kw):
    dag_subdag = DAG(
        dag_id='%s.%s' % (parent_dag, child_dag),
        default_args=args,
        schedule_interval=None,
        )
    files = kw['msgs']
    for i in range(len(files)):
        # create a task 'push_i' which gets one of the msgs as argument and
        # returns that string, so an automatic xcom push is done
        push_id = 'push_' + str(i)
        push_task = PythonOperator(
            task_id=push_id,
            python_callable=push,
            provide_context=True,
            op_kwargs = {'msg' : files[i]},
            dag=dag_subdag)
        munge_task = PythonOperator(
            task_id = 'munge_' + str(i),
            python_callable=munge,
            provide_context=True,
            op_kwargs = {'upstream' : push_id},
            dag=dag_subdag)
        push_task >> munge_task
    return dag_subdag

def print_context(ds, **kwargs):
    logging.info(kwargs)
    logging.info(ds)
    return 'Something to print in the logs'

start_task = PythonOperator(task_id='start', dag=dag,
                            provide_context=True,
                            python_callable=print_context)
end_task = PythonOperator(task_id='end', dag=dag,
                            provide_context=True,
                            python_callable=print_context)

#startdummy = DummyOperator(task_id='start', dag=dag)

dispatcher = SubDagOperator(
    task_id='dispatcher', #  provide_context=True,
    subdag=subdispatcher('python_dispatch', 'dispatcher', args,      #kwdict,
                         provide_context=True,
                         msgs=['file1.parquet', 'file2.parquet','file3.parquet']),
    dag=dag)
#enddummy = DummyOperator(task_id='end', dag=dag)

start_task >> dispatcher >> end_task





