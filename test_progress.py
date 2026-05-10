import requests
import time

data = {'video_url': 'https://youtu.be/52t241OQ7Ec?si=ou_3cvBO6E8Q1XCF'}
r = requests.post('http://127.0.0.1:8000/ingest', json=data)
job = r.json()
job_id = job['job_id']
print('Job started:', job_id[:8] + '...')
print('Status:', job.get('status'))
print('Step:', job.get('step_name'))

for i in range(5):
    time.sleep(1)
    status = requests.get(f'http://127.0.0.1:8000/ingest-status/{job_id}').json()
    print(f"Poll {i+1}: {status.get('step_name')} - {status.get('progress')}% (status: {status.get('status')})")
    if status.get('status') in ['completed', 'failed']:
        print('Job finished!')
        break
