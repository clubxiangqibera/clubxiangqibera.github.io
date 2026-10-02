import io

def fix_ladder(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if 'const LADDER_URL =' in line:
            lines[i] = "const LADDER_URL = 'https://cxb-license.clubxiangqibera.workers.dev/api/ladder.csv';\n"
    with io.open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

fix_ladder('index.html')
fix_ladder('admin.html')
print('LADDER_URL fixed.')
