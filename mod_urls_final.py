import io
import re

worker_action_url = "https://cxb-license.clubxiangqibera.workers.dev/api/action"

def update_urls(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Update CSV URLs
    text = re.sub(r'const MATCH_URL = [^\n]+', 'const MATCH_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/matches.csv";', text)
    text = re.sub(r'const STUDENT_URL = [^\n]+', 'const STUDENT_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/students.csv";', text)
    text = re.sub(r'const LADDER_URL = [^\n]+', 'const LADDER_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/students.csv";', text)

    # 2. Update GAS_API_URL to point to Worker Action URL
    # Find const GAS_API_URL = '...'; and replace the value with worker_action_url
    text = re.sub(r'const GAS_API_URL = \'[^\']+\';', f"const GAS_API_URL = '{worker_action_url}';", text)
    
    with io.open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

update_urls('index.html')
update_urls('admin.html')
print('Frontend URLs updated to use Worker DB and Action endpoint!')
