import json
import urllib
menu_base = 'Menus/'
raw_base = 'RawMenus/'
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

url_file=file('RestaurantURLs.txt','w')

for restaurant_name in restaurants:
##    reviews = file(reviews_base + restaurant_name + '.json', 'r')
##    review_lines = reviews.readlines()
##    obj = json.loads(review_lines[0])
##    menu_URL = urllib.urlopen(str(obj['url']).replace('biz','menu'))
##    url_file.write(str(obj['url']).replace('biz','menu')+'\n')    
##    menu_text = menu_URL.read() 
##    menu_URL.close()
##    menu_file = file(raw_base+restaurant_name+'_MenuScrape.txt','w')
##    menu_file.write(menu_text)
##    reviews.close()
    menu_file=file('NewMenus/'+restaurant_name+'_Menu.txt','r')
    menu_lines=menu_file.readlines()
    menu_file.close()
    newmenu_file=file('NewMenus/'+restaurant_name+'_MenuCorrected.txt','w')
    for i in xrange(len(menu_lines)):
        new_line=menu_lines[i].split('\t')[-1]
        start=new_line.find('>')
        if start!=-1:
            new_line=new_line[start+1:]
        newmenu_file.write(new_line)
    newmenu_file.close()
