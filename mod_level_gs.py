import io
with io.open('Code.gs', 'r', encoding='utf-8') as f:
    text = f.read()

old = '''      if (data.newPwd) {
        studentSheet.getRange(r + 1, 14).setValue(data.newPwd);
      }'''

new = '''      if (data.newPwd) {
        studentSheet.getRange(r + 1, 14).setValue(data.newPwd);
      }
      if (data.newLevel) {
        studentSheet.getRange(r + 1, 7).setValue(data.newLevel);
      }'''

text = text.replace(old, new)
with io.open('Code.gs', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done")
