import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Make Dark Mode definitely BLUE, not black.
# We will use a solid rich navy blue for --bg so it works with CSS vars easily, 
# or we can redefine body background in dark mode.
# Let's use a solid deep vibrant navy for --bg: #071C33
text = text.replace('--bg:#030B14;', '--bg:#071C35;')

# Make the cards distinctly visible with a lighter translucent blue
text = text.replace('--card:#0C1A29;', '--card:#113155;')
text = text.replace('--border:#162C45;', '--border:#225080;')

# To make the Hero banner pop even more against #071C35, we can adjust .public-hero 
# but it's already #071A27 to #1A5276. We can make .public-hero slightly brighter.
new_hero = """.public-hero {
      width: 100%;
      background: linear-gradient(145deg, #0C3052 0%, #185A8A 100%);"""
text = re.sub(r'\.public-hero\s*\{\s*width:\s*100%;\s*background:\s*linear-gradient\([^)]+\);', new_hero, text)

# For the cards (podium), let's make them look glassy in dark mode by adding a global class for them,
# actually, solid #113155 is already very nice and matches the blue aesthetic.

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated to True Blue Dark Mode')
