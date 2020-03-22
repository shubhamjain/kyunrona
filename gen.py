import glob
import os, time
import json, math
import datetime
  
f = open('data.json', 'r+')
data = json.load(f) 
  
for name in glob.glob('static/memes/*'):
    if (not(any(x['src'] == name for x in data))):
        if ("txt" in name):
            txt = open(name, 'r')
            data.append({
                'content': txt.read(),
                'src': name,
                'time': str(os.stat(name).st_ctime)
            })
        else:
            data.append({
                'src': name,
                'time': str(os.stat(name).st_ctime)
            })

data.sort(key=lambda x: x['time'], reverse=True)

f.seek(0)
f.write(json.dumps(data))

template = open('template.html', 'r').read()
paginator = open('page.html', 'r').read()
card = open('card.html', 'r').read()

cards = ''
i = 0
PAGE = 5

IMG_TAG = """
<img src="/__SRC__" class="w-full" />
    <div class="text-right mt-6 mb-4 sm:text-sm px-2 text-gray-600"> — Posted __TIME__</div>
"""

while i <= math.floor(len(data) / PAGE):
    cards = ''

    if i == 0:
        index = open('index.html', 'w')
    else:
        try:
            os.mkdir('./pages/' + str(i))
        except FileExistsError:
            pass
        index = open('./pages/' + str(i) + '/index.html', 'w')
    
    for src in data[(PAGE * (i)):(PAGE * (i + 1))]:
        card_content = ''

        if 'content' in src:
            card_content = src['content']
        else:
            card_content = IMG_TAG.replace('__SRC__', src['src'])

        cards += card.replace('__CONTENT__', card_content).replace(
            '__TIME__', datetime.datetime.fromtimestamp(float(src['time'])).strftime('%b %d, %Y %I:%M %p')
        )
    
    content = template.replace('__CONTAINER__', cards)

    if i == math.floor(len(data) / PAGE):
        content = content.replace('__PAGINATOR__', '')
    else: 
        content = content.replace('__PAGINATOR__', paginator.replace('__page__', str(i + 1)))

    index.write(content)
    i+=1

