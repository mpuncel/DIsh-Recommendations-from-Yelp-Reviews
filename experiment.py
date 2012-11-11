import json
words = []
menu = file('Amelias_Trattoria.txt', 'r')

def clip(amt, length):
	return min(amt, length)

line = menu.readline()
for line in menu:
	for item in line.strip().split(';'):
		words.append(item.lower())

max_length = max([len(x.split(' ')) for x in words])
reviews = file('50_review_restaurants/Amelias_Trattoria.json', 'r')
print words
for line in reviews:
	obj = json.loads(line)
	if obj['type'] == 'review':
		print obj['text']
		text = [x.lower() for x in obj['text'].split(' ')]
		for i in xrange(0, len(text)):
			for j in xrange(0, max_length):
				excerpt = text[i : clip(i + j + 1, len(text))]
				if ' '.join(excerpt) in words:
					print "got a fuckin match for %s" % excerpt
	print '\n\n'
