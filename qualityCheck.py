import os

predictions_base = 'test/predictions/'
training_snippets_base = 'training/Snippets/'
training_suffix = '_training.txt'

def sign(x):
    x = int(x)
    if x >= 0:
        return 1
    else:
        return -1

for dirpath, dirnames, filenames in os.walk(predictions_base):
    for filename in filenames:
        if filename == "Angelinos_Cafe.txt":
            continue
        predictions = file(dirpath + filename).read().split('\n')
        del predictions[-1]
        pred = [sign(a) for a in predictions]
        actuals = file(training_snippets_base + filename[:-4] + training_suffix).read().split('\n')
        del actuals[-1]
        actual = [int(b) for b in actuals]
        wrongCount = 0
        for i in range(len(pred)):
            if pred[i] != actual[i]:
                wrongCount+=1
        percentage = ((len(predictions)-wrongCount)*1.0)/(len(predictions)*1.0)
        print filename + ": " + str(percentage)
              
    
