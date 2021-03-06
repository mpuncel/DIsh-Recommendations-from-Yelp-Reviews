import logging
import json
import sys
import re

logging.basicConfig(filename='snippet_generator.log', level=logging.DEBUG)

length = 'LONGPOS'
menu_base = 'Menus/'
test_output_base = None
if length == "NORMAL":
	print "normal"
	training_output_base = "training/Snippets4foodword/"
	test_output_base = "test/Snippets4foodword/"
	NUM_TRAILING_WORDS = 16
elif length == "SHORT":
	print "short"
	training_output_base = "training/shortSnippets2foodword/"
	test_output_base = "test/shortSnippets2foodword/"
	NUM_TRAILING_WORDS = 8
elif length == "LONG":
	print "long"
	training_output_base = "training/longSnippets2foodword/"
	test_output_base = "test/longSnippets2foodword/"
	NUM_TRAILING_WORDS = 20
elif length == "LONGPOS":
	print "longpos"
	training_output_base = "training/longposSnippets/"
	test_output_base = "test/longposSnippets/"
	NUM_TRAILING_WORDS = 20

reviews_base = '50_review_restaurants_POS_tagged/'
restaurants = [
	'411_West',
	'800_Degrees_Neapolitan_Pizzeria',
	'Al_Forno_Restaurant',
	'Allegro_Pizza',
	'Amelias_Trattoria',
	'Angelinos_Cafe',
	'Antica_Osteria_Restaurant',
	'Antico_Pizza',
	'Aruffos_Italian_Cuisine',
	'Babbos_Original_Mediterranean_Bistro',
	'Bacaro',
	'Bacaro_LA',
	'Bad_Horse_Pizza',
	'Baraonda_Italian_Restaurant',
	'Bertuccis',
	'Bertuccis_Italian_Restaurant_-_Kendall_Square',
	'Bettolona',
	'Buca_di_Beppo',
	'Buona_Tavola',
	'Cafe_47',
	'Campo',
	'Celestino',
	'Che_Bella_Pizza',
	'Cinderellas_Restaurant',
	'DAmicos_Italian_Market_Cafe',
	'DAmores_Pizza',
	'DeFazios_Pizzeria',
	'Dolce_Cafe_&_Bakery',
	'Dominicks',
	'Eno_Terra',
	'Euro_Cafe',
	'Girasole_Restaurant',
	'Gratzi',
	'Gypsys_Trattoria_Italiano',
	'Italian_Express',
	'La_Parolaccia_Osteria_Italiana',
	'La_Piccoletta',
	'Ledo_Restaurant',
	'Lido',
	'Little_Azio',
	'Mama_Palmas_Gourmet_Pizza',
	'Mani_Osteria_&_Bar',
	'Margarita_Pizza_Bar',
	'Max_Cafe',
	'Max_Soha',
	'Mediterra_Restaurant',
	'Milanese_Caffe',
	'Pacci_Ristorante',
	'Pagliacci_Pizza',
	'Palazzo_Giuseppes',
	'Pallino_Pastaria',
	'Panini_Cafe',
	'Pasta_Bene',
	'Pasta_Roma',
	'Piatti_Ristorante_&_Bar',
	'Pisticci',
	'Pizza_House',
	'Pizza_N_Such',
	'Prego',
	'Rialto',
	'Sagra',
	'Salento',
	'Sezz_Medi',
	'Silvios_Organic_Pizza',
	'Skylight_Gardens',
	'Tanino_Restaurant',
	'Teresa_Caffe',
	'Tootsies_At_The_Stanford_Barn',
	'Toscano_&_Sons_Italian_Market',
	'Trattoria_Neapolis',
	'Tutti_Mangia_Italian_Grill',
	'V_&_T_Pizzeria_&_Restaurant',
	'Veni_Vidi_Vici',
	'Viztango_Cafe',
	'Voza',
]

training_restaurants = restaurants
'''[
'411_West',                                    
'800_Degrees_Neapolitan_Pizzeria',
'Babbos_Original_Mediterranean_Bistro',
'Bacaro_LA',
'Al_Forno_Restaurant',
'Bettolona',
'Allegro_Pizza',
'Buca_Di_Beppo',
'Amelias_Trattoria',
'Buona_Tavola',
'DAmicos_Italian_Market_Cafe',
]
'''

#NUM_LEADING_WORDS = 5
def rightclip(amt, length):
	return min(amt, length)

def leftclip(amt):
	return max(amt, 0)

for restaurant_name in restaurants:
	try:
		words = []
		menu = file(menu_base + restaurant_name + '.txt', 'r')
		test_snippets = file(test_output_base + restaurant_name + '.txt', 'w')
		if restaurant_name in training_restaurants:
			training_snippets = file(training_output_base + restaurant_name + '.txt', 'w')

		for line in menu:
			words.append(line.strip().split(';')[0].lower())

		max_length = max([len(x.split(' ')) for x in words])
		reviews = file(reviews_base + restaurant_name + "_POS_tagged" + '.json', 'r')
		for line in reviews:
			try:
				obj = json.loads(line)
				if obj['type'] == 'review':
					text = [x.lower() for x in obj['text'].split(' ')]
					for i in range(0, len(text)):
						for j in reversed(xrange(0, max_length)):
							excerpt = text[i : rightclip(i + j + 1, len(text))]
							if len(re.findall("[a-zA-Z]", text[i][0])) > 0:
								detagged_excerpt = re.findall("[a-zA-Z0-9\-\\\/\\_']+(?=_[a-zA-Z]+[\s]*)", ' '.join(excerpt));
								'''
								if len(detagged_excerpt) != len(excerpt):
									print detagged_excerpt
									print excerpt
									print ' '.join(excerpt)
									print ""
								'''
								if ' '.join(detagged_excerpt) in words:
									#print '|' + ' '.join(detagged_excerpt) + '|'
									#string = ' '.join(text[i: rightclip(i + j + 1 + NUM_TRAILING_WORDS, len(text))])
									string1 = ' '.join(text[i: rightclip(i + j + 1, len(text))]) + " FOODWORD "
									string2 = ' '.join(text[i+j+1:rightclip(i+j+1+NUM_TRAILING_WORDS, len(text))])
									string = string1+string2
									string = string.encode('ascii', 'ignore')
									if restaurant_name in training_restaurants:
										#print string if string.find('\n') < 0 else string[0: string.find('\n')]
										training_snippets.write(string if string.find('\n') < 0 else string[0: string.find('\n')])
										training_snippets.write('\n')
									test_snippets.write(string if string.find('\n') < 0 else string[0: string.find('\n')])
									test_snippets.write('\n')
															
									break
			except Exception, e:
				#logging.exception("inner")
				#print(e)
				continue
		if restaurant_name in training_restaurants:
			training_snippets.close()
		test_snippets.close()
		menu.close()
		reviews.close()
	except:
		logging.exception("outer")
		continue

