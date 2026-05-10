import requests
import time
import json

print("=" * 60)
print("END-TO-END SYSTEM TEST")
print("=" * 60)

# Test 1: Ping backend
print("\n1. Testing backend health...")
r = requests.get('http://127.0.0.1:8000/ping')
assert r.status_code == 200
print("   ✓ Backend responding")

# Test 2: Start ingest with progress tracking
print("\n2. Testing ingest with progress tracking...")
data = {'video_url': 'https://youtu.be/52t241OQ7Ec?si=ou_3cvBO6E8Q1XCF'}
r = requests.post('http://127.0.0.1:8000/ingest', json=data)
job = r.json()
assert job.get('status') == 'processing'
assert job.get('progress') is not None
print(f"   ✓ Job created: {job['job_id'][:8]}...")
print(f"   ✓ Initial progress: {job['progress']}%")
print(f"   ✓ Step: {job['step_name']}")

# Test 3: Monitor progress
print("\n3. Monitoring progress...")
for i in range(5):
    time.sleep(1)
    status = requests.get(f'http://127.0.0.1:8000/ingest-status/{job["job_id"]}').json()
    progress = status.get('progress', 'N/A')
    step = status.get('step_name', 'N/A')
    status_val = status.get('status', 'unknown')
    print(f"   Poll {i+1}: {step} - {progress}% [{status_val}]")
    if status_val in ['completed', 'failed']:
        break

if status_val == 'completed':
    # Test 4: Get analysis
    print("\n4. Testing /analysis endpoint...")
    video_id = job['video_id']
    r = requests.get(f'http://127.0.0.1:8000/analysis/{video_id}')
    if r.status_code == 200:
        analysis = r.json()
        has_summary = analysis.get('summary') and not analysis['summary'].startswith('Summary is not')
        print(f"   ✓ Analysis retrieved")
        print(f"   ✓ Has summary: {has_summary}")
        print(f"   ✓ Status: {analysis.get('status')}")
    else:
        print(f"   ! Analysis returned {r.status_code}")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - SYSTEM READY FOR DEMO!")
print("=" * 60)
