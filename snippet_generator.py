import json
words = []
menu_base = 'Menus/'
output_base = 'Snippets/'
reviews_base = '50_review_restaurants/'
restaurants = [
	'Al_Forno_Restaurant',
	'Angelinos_Cafe',
	'Bacaro_LA',
	'Buca_Di_Beppo',
	'Amelias_Trattoria',
]

NUM_TRAILING_WORDS = 12
def rightclip(amt, length):
	return min(amt, length)

def leftclip(amt):
	return max(amt, 0)

for restaurant_name in restaurants:
	menu = file(menu_base + restaurant_name + '.txt', 'r')
	snippets = file(output_base + restaurant_name + '.txt', 'w')
	line = menu.readline()
	for line in menu:
		words.append(line.strip().split(';')[0].lower())
		'''
		for item in line.strip().split(';'):
			words.append(item.lower())
		'''

	max_length = max([len(x.split(' ')) for x in words])
	reviews = file(reviews_base + restaurant_name + '.json', 'r')
	for line in reviews:
		try:
			obj = json.loads(line)
			if obj['type'] == 'review':
				text = [x.lower() for x in obj['text'].split(' ')]
				for i in range(0, len(text)):
					for j in reversed(xrange(0, max_length)):
						excerpt = text[i : rightclip(i + j + 1, len(text))]
						if ' '.join(excerpt) in words:
							string = ' '.join(text[leftclip(i): rightclip(i + j + 1 + NUM_TRAILING_WORDS, len(text))])
							snippets.write(string if string.find('\n') < 0 else string[0: string.find('\n')])
							snippets.write('\n')
							break
		except:
			break
	snippets.close()
	menu.close()
	reviews.close()
