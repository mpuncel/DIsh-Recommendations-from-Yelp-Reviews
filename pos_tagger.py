import codecs
import json
import os

reviews_base = '50_review_restaurants/'
out_base = '50_review_restaurants_POS_tagged/'
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
##	'Cafe_47',
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
##	'Max_Cafe',
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

logFile=codecs.open('LogFile.txt','w','utf-8')

for restaurant_name in restaurants:
    reviews = file(reviews_base + restaurant_name + '.json', 'r')
    count=0
    new_base=out_base+'/'+restaurant_name+'/'
    os.popen3("mkdir {0}".format(new_base))
    for line in reviews:
        try:
            obj = json.loads(line)
            if obj['type']=='review':
                text=obj['text']
                tempFile=codecs.open('Temp.txt','w','utf-8')
                tempFile.write(text)
                tempFile.close()
                in_file,out_file,error_file=os.popen3("java -mx300m -cp 'stanford-postagger-full-2012-11-11/stanford-postagger-3.1.4.jar:' edu.stanford.nlp.tagger.maxent.MaxentTagger -model stanford-postagger-full-2012-11-11/models/wsj-0-18-left3words.tagger -textFile Temp.txt")
                tagFile=file(new_base+restaurant_name+'_review_'+str(count)+'_POS_Tagged.txt','w') 
                tagFile.write(''.join(out_file))
                tagFile.close()
        except:
            logFile=codecs.open('LogFile.txt','a','utf-8')
            logFile.write(restaurant_name+': Line'+str(count-1)+'\n')
            logFile.close()
        count+=1
    reviews.close()
    
