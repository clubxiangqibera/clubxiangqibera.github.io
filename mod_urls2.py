import io
import re

worker_action_url = "https://cxb-license.clubxiangqibera.workers.dev/api/action"

def update_urls(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    text = re.sub(r'const MATCH_URL = [^\n]+', 'const MATCH_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/matches.csv";', text)
    text = re.sub(r'const STUDENT_URL = [^\n]+', 'const STUDENT_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/students.csv";', text)
    text = re.sub(r'const LADDER_URL = [^\n]+', 'const LADDER_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/students.csv";', text)

    # In admin, GAS_API_URL is defined as const GAS_API_URL = "..."
    # We rename GAS_API_URL definition to GAS_UPLOAD_URL.
    if "const GAS_API_URL = " in text:
        text = text.replace("const GAS_API_URL =", "const GAS_UPLOAD_URL =")

    # Now we replace all usages of GAS_API_URL with the worker URL, EXCEPT where it is clearly an upload.
    # Actually, we can just replace ALL `GAS_API_URL` with `'https://cxb-license.clubxiangqibera.workers.dev/api/action'`
    # Then go back and fix the 4 specific upload actions to use `GAS_UPLOAD_URL`.
    text = text.replace("GAS_API_URL", f"'{worker_action_url}'")
    
    # Fix the 4 uploads
    # 1. uploadReceipt
    # 2. updateMatchXQF
    # 3. updateMatchPhoto
    # 4. uploadEventPhoto
    # Wait, in the JS, it's fetch('{worker_action_url}', { ... action: 'uploadReceipt' })
    # We can just regex replace:
    text = re.sub(r"fetch\('[^']+',\s*\{\s*method:\s*'POST',\s*body:\s*JSON\.stringify\(\{\s*action:\s*'uploadReceipt'", 
                  r"fetch(GAS_UPLOAD_URL, { method: 'POST', body: JSON.stringify({ action: 'uploadReceipt'", text)
    
    text = re.sub(r"fetch\('[^']+',\s*\{\s*method:\s*'POST',\s*body:\s*JSON\.stringify\(\{\s*action:\s*'updateMatchXQF'", 
                  r"fetch(GAS_UPLOAD_URL, { method: 'POST', body: JSON.stringify({ action: 'updateMatchXQF'", text)
                  
    text = re.sub(r"fetch\('[^']+',\s*\{\s*method:\s*'POST',\s*body:\s*JSON\.stringify\(\{\s*action:\s*'updateMatchPhoto'", 
                  r"fetch(GAS_UPLOAD_URL, { method: 'POST', body: JSON.stringify({ action: 'updateMatchPhoto'", text)
                  
    text = re.sub(r"fetch\('[^']+',\s*\{\s*method:\s*'POST',\s*body:\s*JSON\.stringify\(\{\s*action:\s*'uploadEventPhoto'", 
                  r"fetch(GAS_UPLOAD_URL, { method: 'POST', body: JSON.stringify({ action: 'uploadEventPhoto'", text)

    with io.open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

update_urls('index.html')
update_urls('admin.html')
