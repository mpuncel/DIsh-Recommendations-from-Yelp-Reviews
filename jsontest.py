import json
fp = file('test.json', 'w')
obj1 = {
	'foo' : 'bar',
	'slut' : 'bag',
}
obj2 = {
	'fjsdlk' : 'sofjlaksf',
	'sdljfks' : 'dklfjas;fjlskdjaf',
}
json.dump(obj1, fp)
fp.write('\n')
json.dump(obj2, fp)
	
