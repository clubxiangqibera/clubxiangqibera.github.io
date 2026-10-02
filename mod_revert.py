import io

worker_action_url = "https://cxb-license.clubxiangqibera.workers.dev/api/action"

def revert_urls(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace('GAS_UPLOAD_URL', f"'{worker_action_url}'")
    
    with io.open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

revert_urls('index.html')
revert_urls('admin.html')
print('URLs reverted to send everything to Worker!')
