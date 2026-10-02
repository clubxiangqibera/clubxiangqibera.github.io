import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'const MATCH_URL = [^\n]+', 'const MATCH_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/matches.csv";', text)
text = re.sub(r'const STUDENT_URL = [^\n]+', 'const STUDENT_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/students.csv";', text)
text = re.sub(r'const LADDER_URL = [^\n]+', 'const LADDER_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/students.csv";', text)

# Update action endpoint to Worker for changePassword
worker_action_url = "https://cxb-license.clubxiangqibera.workers.dev/api/action"
text = text.replace("fetch(GAS_API_URL, {", f"fetch('{worker_action_url}', {{")

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# Same for admin.html
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'const MATCH_URL = [^\n]+', 'const MATCH_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/matches.csv";', text)
text = re.sub(r'const STUDENT_URL = [^\n]+', 'const STUDENT_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/students.csv";', text)
text = re.sub(r'const LADDER_URL = [^\n]+', 'const LADDER_URL = "https://cxb-license.clubxiangqibera.workers.dev/api/students.csv";', text)

# For admin.html, replace fetch(GAS_API_URL, ...) with worker action url, EXCEPT for uploads.
# The uploads are: uploadReceipt, updateMatchXQF, updateMatchPhoto, uploadEventPhoto.
text = text.replace("fetch(GAS_API_URL,", f"fetch('{worker_action_url}',")

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
