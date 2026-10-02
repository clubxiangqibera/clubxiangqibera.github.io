import io

with io.open('Code.gs', 'r', encoding='utf-8') as f:
    text = f.read()

target = "studentSheet.getRange(r + 1, 9).setValue('⏳ 待核实 (收据已上传)');"
replacement = "studentSheet.getRange(r + 1, 9).setValue('⏳ 待核实 (收据已上传)|' + imgUrl);"

if target in text:
    text = text.replace(target, replacement)
    with io.open('Code.gs', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Code.gs updated successfully")
else:
    print("Target not found")
