from hotqueue import HotQueue
import json
import os
import redis
import matplotlib.pyplot as plt
import subprocess
from jobs import q, rd, jdb, update_job_status, img_db
import time

@q.worker
def execute_job(jid):
    print('executing job...')
    update_job_status(jid, 'in progress')
    data = jdb.hgetall(f'job.{jid}')

    x_vals = []
    y_vals = []

    for year in range(int(data['start']), int(data['end'])+1):
        result = rd.hget(f"{data['country']}-{year}", data['field'])
        if not result:
            result = 0
        y_vals.append(float(result))
        x_vals.append(int(year))

    plt.xlabel("Year")
    #plt.title(f"{field} Over Time in {country}")
    #plt.ylabel(f"{field}")
    plt.plot(x_vals, y_vals, 'b--')
    plt.savefig('/output_image.png')
    
    with open('/output_image.png', 'rb') as f:
        img = f.read()

    img_db.hset(f'job.{jid}', 'image', img) 

    jdb.hset(f'job.{jid}', 'status', 'finished')

execute_job()
#redis_ip = os.environ.get('REDIS_IP')
#if not redis_ip:
#    raise Exception()
#rd = redis.StrictRedis(host=redis_ip, port=6379, db=0, decode_responses=True)
#q = HotQueue('queue', host=redis_ip, port=6379, db=1)
