import json
fulldata = 'yelp_academic_dataset.json'
italian = 'italian_restaurants.json'

in_f = file(italian, 'r')

folder30 = '30_review_restaurants/'
folder50 = '50_review_restaurants/'

fps50 = {}
fps30 = {}
line = in_f.readline()
while True:
	try:
		obj = json.loads(line)
		name = obj['name'][:]
		name = name.replace("\'", '').replace(' ', '_')
		if obj['review_count'] > 50:
			fps50[obj['business_id']] = file(folder50 + name + '.json', 'w')
			json.dump(obj, fps50[obj['business_id']])
			fps50[obj['business_id']].write('\n')
		if obj['review_count'] > 30:
			fps30[obj['business_id']] = file(folder30 + name + '.json', 'w')
			json.dump(obj, fps30[obj['business_id']])
			fps30[obj['business_id']].write('\n')
		line = in_f.readline()
			
	except:
		break

in_all = file(fulldata, 'r')
line = in_all.readline()
while True:
	obj = json.loads(line)
	if obj['type'] == 'review':
		if fps30.get(obj['business_id'], None) is not None:
			json.dump(obj, fps30[obj['business_id']])
			fps30[obj['business_id']].write("\n")
		if fps50.get(obj['business_id'], None) is not None:
			json.dump(obj, fps50[obj['business_id']])
			fps50[obj['business_id']].write("\n")
	line = in_all.readline()
