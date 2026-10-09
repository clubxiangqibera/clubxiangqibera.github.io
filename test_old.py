import re
with open('old_school.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'(function renderWeeklyAttendance\(\) \{.*?)(function toggleAttendance)', content, re.DOTALL)
if m:
    print(m.group(1))
