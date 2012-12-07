import traceback
import json
import sys

menu_base = 'Menus/'
baseline_base = 'test/baselinepredictions/'
reviews_base = '50_review_restaurants/'
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

NUM_TRAILING_WORDS = 8
#NUM_LEADING_WORDS = 5
def rightclip(amt, length):
	return min(amt, length)

def leftclip(amt):
	return max(amt, 0)

for restaurant_name in restaurants:
	try:
		words = []
		menu = file(menu_base + restaurant_name + '.txt', 'r')
		if restaurant_name in training_restaurants:
			baseline_preds = file(baseline_base + restaurant_name + '.txt', 'w')

		for line in menu:
			words.append(line.strip().split(';')[0].lower())

		max_length = max([len(x.split(' ')) for x in words])
		reviews = file(reviews_base + restaurant_name + '.json', 'r')
		for line in reviews:
			try:
				obj = json.loads(line)
				if obj['type'] == 'review':
					text = [x.lower() for x in obj['text'].split(' ')]
					stars = obj['stars']
					for i in range(0, len(text)):
						for j in reversed(xrange(0, max_length)):
							excerpt = text[i : rightclip(i + j + 1, len(text))]
							if ' '.join(excerpt) in words:
								string = ' '.join(text[i: rightclip(i + j + 1 + NUM_TRAILING_WORDS, len(text))])
								string = string.encode('ascii', 'ignore')
								if restaurant_name in training_restaurants:
									baseline_preds.write("1" if stars >= 3 else "-1")
									baseline_preds.write('\n')

								break
			except Exception, e:
				#print(e)
				continue
		if restaurant_name in training_restaurants:
			baseline_preds.close()
		menu.close()
		reviews.close()
	except Exception, e:
		#print(e)
		continue
