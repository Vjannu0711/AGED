from datetime import datetime
import json
import os
import uuid
from flask import Flask, request
import redis
from hotqueue import HotQueue

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd = redis.Redis(host=redis_ip, port=6379, db=0, decode_responses=True)
q = HotQueue("queue", host=redis_ip, port=6379, db=1)
jdb = redis.Redis(host=redis_ip, port=6379, db=2, decode_responses=True)

def _generate_jid():
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())

def _generate_job_key(jid):
    """
    Generate the redis key from the job id to be used when storing, retrieving or updating
    a job in the database.
    """
    return 'job.{}'.format(jid)
