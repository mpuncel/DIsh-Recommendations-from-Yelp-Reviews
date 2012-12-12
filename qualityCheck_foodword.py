import os
import math

predictions_base = 'test/predictions4_foodword/'
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
    sumNPrecision = 0
    sumNRecall = 0
    sumBPercentage = 0
    sumBPrecision = 0
    sumBRecall = 0
    sumBNPrecision = 0
    sumBNRecall = 0
    sumMCC = 0
    sumBMCC = 0
    
    for filename in filenames:
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
        precision = 0
        recall = 0
        negprec = 0
        negrec = 0
        MCC = 0
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

        try:
            precision = (truePos)/float(truePos + falsePos)
            recall = (truePos)/float(truePos + falseNeg)
            negprec = (trueNeg)/float(trueNeg + falseNeg)
            negrec = (trueNeg)/float(trueNeg + falsePos)
            MCC = (truePos*trueNeg - falsePos*falseNeg)/math.sqrt((truePos+falsePos)*(truePos+falseNeg)*(trueNeg+falsePos)*(trueNeg+falseNeg))

        except:
            pass
        
        foodReviews = {}
        for label,foodword in pred:
            if foodword in foodReviews.keys():
                foodReviews[foodword] = [foodReviews[foodword][0]+1.0, foodReviews[foodword][1]+float(label)*1.0]
            else:
                foodReviews[foodword] = [1.0, float(label)]

        print "----------------------------------------------------------"
        percentage = ((len(actual)-wrongCount)*1.0)/(len(actual)*1.0)
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
        print "NEG PRECISION: " + str(negprec)
        print "NEG RECALL: " + str(negrec)
        if filename[:-4] in test_restaurants:
            sumPercentage += percentage
            sumPrecision += precision
            sumRecall += recall
            sumNPrecision += negprec
            sumNRecall += negrec
            sumMCC += MCC

        print "__________________________"
        
        # Calculate metrics for baseline
        wrongCount = 0
        truePos = 0
        falsePos = 0
        trueNeg = 0
        falseNeg = 0
        precision = 0
        recall = 0
        negprec = 0
        negrec = 0
        MCC = 0
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

        try:
            precision = (truePos)/float(truePos + falsePos)
            recall = (truePos)/float(truePos + falseNeg)
            negprec = (trueNeg)/float(trueNeg + falseNeg)
            negrec = (trueNeg)/float(trueNeg + falsePos)
            MCC = (truePos*trueNeg - falsePos*falseNeg)/math.sqrt((truePos+falsePos)*(truePos+falseNeg)*(trueNeg+falsePos)*(trueNeg+falseNeg))
        except:
            pass
        percentage = ((len(actual)-wrongCount)*1.0)/(len(actual)*1.0)
        print "Baseline Percentage: " + str(percentage)
        print "Baseline Precision: " + str(precision)
        print "Baseline Recall: " + str(recall)
        print "Baseline Negative Precision: " + str(negprec)
        print "Baseline Negative Recall: " + str(negrec)
        
        if filename[:-4] in test_restaurants:
            sumBPercentage += percentage
            sumBPrecision += precision
            sumBRecall += recall
            sumBNPrecision += negprec
            sumBNRecall += negrec
            sumBMCC += MCC

        print "----------------------------------------------------------"
    N = float(len(test_restaurants))
    print "Average Percentage: " + str((sumPercentage/N))
    print "Average Pecision: " + str((sumPrecision/N))
    print "Average Recall: " + str((sumRecall/N))
    print "Average Neg Precision: " + str((sumNPrecision/N))
    print "Average Neg Recall: " + str((sumNRecall/N))
    print "Average MCC: " + str((sumMCC/N))
    print "Average Baseline Percentage: " + str((sumBPercentage/N))
    print "Average Baseline Pecision: " + str((sumBPrecision/N))
    print "Average Baseline Recall: " + str((sumBRecall/N))
    print "Average Baseline Neg Precision: " + str((sumBNPrecision/N))
    print "Average Baseline Neg Recall: " + str((sumBNRecall/N))
    print "Average Baseline MCC: " + str((sumBMCC/N))

                
        
              
    
