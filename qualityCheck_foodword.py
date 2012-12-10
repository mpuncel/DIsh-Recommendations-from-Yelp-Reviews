import os

predictions_base = 'test/shortpredictions2_foodword/'
baseline_base = 'test/baselinepredictions/'
training_snippets_base = 'training/longSnippets2/'
training_suffix = '_training.txt'
test_restaurants = ['Buona_Tavola','DAmicos_Italian_Market_Cafe','Gratzi','Lido','Pasta_Bene','Sezz_Medi']
def sign(x):
    x = int(x)
    if x >= 0:
        return 1
    else:
        return -1

def extract(y):
    line = y.split(' ')
    label = line[0]
    foodword = ' '.join(line[1:])
    return [label, foodword]
    

for dirpath, dirnames, filenames in os.walk(predictions_base):
    sumPercentage = 0
    sumPrecision = 0
    sumRecall = 0
    sumBPercentage = 0
    sumBPrecision = 0
    sumBRecall = 0
    for filename in filenames:
        #if filename == "Angelinos_Cafe.txt":
        #    print filename
        #    continue
        predictions = file(dirpath + filename).read().split('\n')
        del predictions[-1]
        pred = [extract(a) for a in predictions]
        actuals = file(training_snippets_base + filename[:-4] + training_suffix).read().split('\n')        
        del actuals[-1]
        actual = [sign(b) for b in actuals]
        wrongCount = 0
        truePos = 0
        falsePos = 0
        trueNeg = 0
        falseNeg = 0
        for i in range(len(pred)):
            if sign(pred[i][0]) != actual[i]:
                wrongCount+=1
            if sign(pred[i][0]) >= 0 and actual[i] >=0:
                truePos+=1
            elif sign(pred[i][0]) >= 0 and actual[i] < 0:
                falsePos+=1
            elif sign(pred[i][0]) < 0 and actual[i] < 0:
                trueNeg+=1
            elif sign(pred[i][0]) < 0 and actual[i] >= 0:
                falseNeg+=1

        precision = (truePos)/float(truePos + falsePos)
        recall = (truePos)/float(truePos + falseNeg)
        
        foodReviews = {}
        for label,foodword in pred:
            if foodword in foodReviews.keys():
                foodReviews[foodword] = [foodReviews[foodword][0]+1.0, foodReviews[foodword][1]+float(label)*1.0]
            else:
                foodReviews[foodword] = [1.0, float(label)]

        print "----------------------------------------------------------"
        percentage = ((len(predictions)-wrongCount)*1.0)/(len(predictions)*1.0)
        print filename + ": " + str(percentage)

        sortedByFreq = sorted(foodReviews.iterkeys(), key=foodReviews.get, reverse = True)
        for key in sortedByFreq[0:2]:
            reviewCount = foodReviews[key][0]
            if reviewCount >= 3:
                if foodReviews[key][1] >= 2:
                    print "We recommend: " + key
        sortedByRating = sorted(foodReviews.iterkeys(), key=foodReviews.get, reverse = True)
        for key in sortedByFreq:
            reviewCount = foodReviews[key][0]
            if reviewCount >= 3:
                if foodReviews[key][1] < 0:
                    print "Stay away from: " + key
            

        for key in sorted(foodReviews.iterkeys(), key = str):
            print key + "[" + str(foodReviews[key][0]) + ", " + str(foodReviews[key][1]) + "] : " + str(foodReviews[key][1]/(foodReviews[key][0]*1.0))

        print "PRECISION: " + str(precision)
        print "RECALL: " + str(recall)
        if filename[:-4] in test_restaurants:
            sumPercentage += percentage
            sumPrecision += precision
            sumRecall += recall

        print "__________________________"
        
        # Calculate metrics for baseline
        wrongCount = 0
        baselines = file(baseline_base + filename).read().split('\n')
        del baselines[-1]
        baseline = [sign(b) for b in baselines]
        for i in range(len(baseline)):
            if baseline[i] != actual[i]:
                wrongCount+=1
            if baseline[i] >= 0 and actual[i] >=0:
                truePos+=1
            elif baseline[i] >= 0 and actual[i] < 0:
                falsePos+=1
            elif baseline[i] < 0 and actual[i] < 0:
                trueNeg+=1
            elif baseline[i] < 0 and actual[i] >= 0:
                falseNeg+=1

        precision = (truePos)/float(truePos + falsePos)
        recall = (truePos)/float(truePos + falseNeg)
        percentage = ((len(baseline)-wrongCount)*1.0)/(len(baseline)*1.0)
        print "Baseline Percentage: " + str(percentage)
        print "Baseline Precision: " + str(precision)
        print "Baseline Recall: " + str(recall)

        if filename[:-4] in test_restaurants:
            sumBPercentage += percentage
            sumBPrecision += precision
            sumBRecall += recall

        print "----------------------------------------------------------"
    N = float(len(test_restaurants))
    print "Average Percentage: " + str((sumPercentage/N))
    print "Average Pecision: " + str((sumPrecision/N))
    print "Average Recall: " + str((sumRecall/N))
    print "Average Baseline Percentage: " + str((sumBPercentage/N))
    print "Average Baseline Pecision: " + str((sumBPrecision/N))
    print "Average Baseline Recall: " + str((sumBRecall/N))

                
        
              
    
