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
img_db = redis.Redis(host=redis_ip, port=6379, db=3)
q = HotQueue("queue", host=redis_ip, port=6379, db=1)
jdb = redis.Redis(host=redis_ip, port=6379, db=2, decode_responses=True)

# GENERATE RANDOM JOB ID
def _generate_jid():
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())

# GENERATE REDIS KEY
def _generate_job_key(jid):
    """
    Generate the redis key from the job id to be used when storing, retrieving or updating
    a job in the database.
    """
    return 'job.{}'.format(jid)

# CREATE JOB OBJECT DESCRIPTION
def _instantiate_job(jid, country, field, status, start, end):
    """
    Create the job object description as a python dictionary. Requires the job id, country, field, status,
    start and end parameters.
    """
    if type(jid) == str:
        return {'id': jid,
                'datetime': str(datetime.now()),
                'country': country,
                'field': field,
                'status': status,
                'start': start,
                'end': end
               }
    return {'id': jid.decode('utf-8'),
            'datetime': str(datetime.now()),
            'country': country.decode('utf-8'),
            'field': field.decode('utf-8'),
            'status': status.decode('utf-8'),
            'start': start.decode('utf-8'),
            'end': end.decode('utf-8')
           }

# SAVE JOB IN REDIS DB
def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    jdb.hset(job_key, mapping=job_dict)
    return

# ADD JOB TO QUEUE
def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)
    return

# SUBMITTED JOB
def add_job(country, field, start, end, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, country, field, status, start, end)
    _save_job(_generate_job_key(jid), job_dict)
    _queue_job(jid)
    return job_dict

# RETURN JOB DICT
def get_job_by_id(jid):
    """Return job dictionary given jid"""
    return (jdb.hgetall(_generate_job_key(jid).encode('utf-8')))

# UPDATE JOB STATUS
def update_job_status(jid, status):
    """Update the status of job with job id `jid` to status `status`."""
    job = get_job_by_id(jid)
    if job:
        job['status'] = status
        _save_job(_generate_job_key(jid), job)
    else:
        raise Exception()
