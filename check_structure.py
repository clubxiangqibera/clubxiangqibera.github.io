import io, re
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Events section exists:', 'events' in text)
print('Ladder section exists:', 'ladder' in text)
print('Ladder render js exists:', 'renderPublicLadder' in text)

match = re.search(r'(<section class="section" id="events">.*?</section>)', text, flags=re.DOTALL)
if match:
    idx = text.find(match.group(1))
    print('Events section ends at:', idx + len(match.group(1)))
    print('Next 200 chars:', text[idx + len(match.group(1)):idx + len(match.group(1))+200])
