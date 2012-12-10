import os

predictions_base = 'test/predictions2_moretest/'
baseline_base = 'test/baselinepredictions/'
training_snippets_base = 'training/longSnippets2/'
training_suffix = '_training.txt'

def sign(x):
    x = int(x)
    if x >= 0:
        return 1
    else:
        return -1

for dirpath, dirnames, filenames in os.walk(predictions_base):
    for filename in filenames:
        #if filename == "Angelinos_Cafe.txt":
        #    print filename
        #    continue
        predictions = file(dirpath + filename).read().split('\n')
        del predictions[-1]
        pred = [sign(a) for a in predictions]
        actuals = file(training_snippets_base + filename[:-4] + training_suffix).read().split('\n')        
        del actuals[-1]
        actual = [sign(b) for b in actuals]
        wrongCount = 0
        for i in range(len(pred)):
            if pred[i] != actual[i]:
                wrongCount+=1

##        wrongCount = 0
##        baselines = file(baseline_base + filename).read().split('\n')
##        del baselines[-1]
##        baseline = [sign(b) for b in baselines]
##        for i in range(len(baseline)):
##            if baseline[i] != actual[i]:
##                wrongCount+=1
                
        percentage = ((len(predictions)-wrongCount)*1.0)/(len(predictions)*1.0)
        print filename + ": " + str(percentage)
              
    
