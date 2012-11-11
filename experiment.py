import json
words = []
menu = file('Menus/Amelias_Trattoria.txt', 'r')

def rightclip(amt, length):
	return min(amt, length)

def leftclip(amt):
	return max(amt, 0)

line = menu.readline()
for line in menu:
	for item in line.strip().split(';'):
		words.append(item.lower())

max_length = max([len(x.split(' ')) for x in words])
reviews = file('50_review_restaurants/Amelias_Trattoria.json', 'r')
for line in reviews:
	obj = json.loads(line)
	if obj['type'] == 'review':
		#print obj['text']
		text = [x.lower() for x in obj['text'].split(' ')]
		for i in range(0, len(text)):
			for j in reversed(xrange(0, max_length)):
				excerpt = text[i : rightclip(i + j + 1, len(text))]
				if ' '.join(excerpt) in words:
					print ' '.join(text[leftclip(i - 5): rightclip(i + j + 6, len(text))])
					break
