import io

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix CSS focus
text = text.replace('.gate-input:focus{border-color:var(--primary-mid);background:#fff;}', '.gate-input:focus{border-color:var(--primary-mid);}')

# 2. Fix password extraction from CSV
text = text.replace("password: (r[13]||'1234').trim()", "password: (r[13]||'').trim()")

# 3. Fix validPwd logic
# Previous logic: const validPwd = found.password && found.password !== defaultPwd ? found.password : (found.password || defaultPwd);
old_valid = "const validPwd = found.password && found.password !== defaultPwd ? found.password : (found.password || defaultPwd);"
new_valid = "const validPwd = found.password || defaultPwd;"
if old_valid in text:
    text = text.replace(old_valid, new_valid)
else:
    print("Could not find validPwd logic")

# In changePassword(), we need to apply the same logic fix if it exists there:
old_valid_2 = "const currentPwd = stu.password && stu.password !== defaultPwd ? stu.password : (stu.password || defaultPwd);"
new_valid_2 = "const currentPwd = stu.password || defaultPwd;"
if old_valid_2 in text:
    text = text.replace(old_valid_2, new_valid_2)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Fixes applied to index.html")
