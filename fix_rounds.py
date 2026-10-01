import io
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('CXB 比赛', 'CXQB (Club XiangQi Bera) 比赛')
text = text.replace(
    '<option value="3">3 轮</option><option value="4" selected>4 轮</option><option value="5">5 轮</option><option value="6">6 轮</option><option value="7">7 轮</option>',
    '<option value="2">2 轮</option><option value="3">3 轮</option><option value="4" selected>4 轮</option><option value="5">5 轮</option><option value="6">6 轮</option><option value="7">7 轮</option><option value="8">8 轮</option><option value="9">9 轮</option><option value="10">10 轮</option>'
)

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("done")
