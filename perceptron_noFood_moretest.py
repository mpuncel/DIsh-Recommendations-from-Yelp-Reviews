import traceback
import sys
import re

alpha = 1
T = 60
test_snippets_base = 'test/shortSnippets2foodword/'
predictions_base = 'test/predictions4_foodword/'
training_snippets_base = 'training/shortSnippets2foodword/'
training_base = 'training/longSnippets2/'
training_suffix = '_training.txt'
menu_base = 'Menus/'
foodtag = 'FOODWORD'
exclusion_regex = r'[)(\n.?!:,]'
training_restaurants = [
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
	#'Buona_Tavola',
	'Cafe_47',
	'Campo',
	'Celestino',
	'Che_Bella_Pizza',
	'Cinderellas_Restaurant',
	#'DAmicos_Italian_Market_Cafe',
	'DAmores_Pizza',
	'DeFazios_Pizzeria',
	'Dolce_Cafe_&_Bakery',
	'Dominicks',
	'Eno_Terra',
	'Euro_Cafe',
	'Girasole_Restaurant',
	#'Gratzi',
	'Gypsys_Trattoria_Italiano',
	'Italian_Express',
	'La_Parolaccia_Osteria_Italiana',
	'La_Piccoletta',
	'Ledo_Restaurant',
	#'Lido',
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
	#'Pasta_Bene',
	'Pasta_Roma',
	'Piatti_Ristorante_&_Bar',
	'Pisticci',
	'Pizza_House',
	'Pizza_N_Such',
	'Prego',
	'Rialto',
	'Sagra',
	'Salento',
	#'Sezz_Medi',
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
	'''
	'411_West',
	'800_Degrees_Neapolitan_Pizzeria',
	'Al_Forno_Restaurant',
	'Amelias_Trattoria',
	'Babbos_Original_Mediterranean_Bistro',
	'Bacaro_LA',
	'Bettolona',
	#'Buca_Di_Beppo',
	#'Buona_Tavola',
	#'DAmicos_Italian_Market_Cafe',
	'''
]
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
##build food vocabulary
foodVocab = set()
for restaurant_name in restaurants:
        try:
                menu = file(menu_base + restaurant_name + '.txt', 'r')
                for line in menu:
                        menuItem = line.strip().split(';')[0].lower().split(' ')
                        foodVocab = foodVocab.union(set((menuItem)))
        except:
                pass

        
##build vocabulary
vocab = set()

for training_restaurant_name in training_restaurants:
        try:
                snips = file(training_snippets_base + training_restaurant_name + '.txt', 'r')
                for line in snips:
                        vocabWords = re.sub(exclusion_regex, '', line.lower()).split(' ')
                        vocab = vocab.union(set(vocabWords))
                snips.close()
        except:
                pass
        
vocab = vocab.difference(foodVocab)
print len(vocab)
vocab = list(vocab)
weight = [0]*len(vocab)

##get weights
for i in range(0, T):
	for training_restaurant_name in training_restaurants:
		try:
			snips = file(training_snippets_base + training_restaurant_name + '.txt', 'r')
			training = file(training_base + training_restaurant_name + training_suffix, 'r')
			for line in snips:
				label = int(training.readline())
				foodword = line.split(' FOODWORD ')[0]
				tokenset = set(re.sub(exclusion_regex, '', line).split(' '))
				
				vector = [0]*len(vocab)
				for j in xrange(0, len(vocab)):
					if vocab[j] in tokenset:
						vector[j] = 1
				product = [w * x for w, x in zip(weight, vector)]
				if sum(product) >= 0:
					sign = 1
				else:
					sign = -1
				if int(sign) != label:
					adjustment = [v * alpha * label for v in vector]
					weight = [w + a for w,a in zip(weight, adjustment)]
		except:
			pass

tups = zip(weight, vocab)
tups.sort()
print tups

##apply to test data
for restaurant_name in restaurants:
	try:
		snips = file(test_snippets_base + restaurant_name + '.txt', 'r')
		out = file(predictions_base + restaurant_name + '.txt', 'w')
		for line in snips:
			tokenset = set(re.sub(exclusion_regex, '', line).split(' '))
			foodword = line.split(' FOODWORD ')[0]

			vector = [0]*len(vocab)
			for j in xrange(0, len(vocab)):
				if vocab[j] in tokenset:
					vector[j] = 1

			product = [w * x for w, x in zip(weight, vector)]
			out.write(str(sum(product)) + " " + foodword + '\n')

	except:
		#traceback.print_exc(file=sys.stdout)
		continue

