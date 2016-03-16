__author__ = 'vignesh'

import ConfigParser as CP
from Sentence import Sentence
from jsonrpc import *
from nltk.tag.stanford import StanfordNERTagger
from Pair import Pair
import pickle
import scipy.io as sio


# set config file
config = CP.RawConfigParser()
config = config
config.read('config.py')

# Get the train and test file names
trains1fname = config.get('init','trains1') # Sentence1
trains2fname = config.get('init','trains2') # Sentence 2
trains1 = open(trains1fname).readlines()
trains2 = open(trains2fname).readlines()

tests1fname = config.get('init','tests1')
tests2fname = config.get('init','tests2')
tests1 = open(tests1fname).readlines()
tests2 = open(tests2fname).readlines()

# Get the class labels
trainlabelsfname = config.get('init','trainlabels')
testlabelsfname = config.get('init','testlabels')
trainlabels = open(trainlabelsfname).readlines()
testlabels = open(testlabelsfname).readlines()

# Make sentence objects out of both sentences in train and test
trainsentences1 = []
trainsentences2 = []
testsentences1 = []
testsentences2 = []
trainpairs = []
testpairs = []

# LIst of all postags and ners for creating the indicator variables for pairs
allpostags = []
allners = []


# Make objects of the corenlp server handler and
# NER tagger

server = ServerProxy(JsonRpc20(),TransportTcpIp(addr=("127.0.0.1", 8080), timeout=200.0))
tagger = config.get('NER','tagger') # gets the path of the stanford tagger from the config file
classifier = config.get('NER','classifier') # gets the path of the stanford classifier
st = StanfordNERTagger(classifier,tagger)



"""
Assumption is that the number of sentences in s1 and s2 should be the same
"""

for i in range(len(trains1))[:2]:
    trains1obj = Sentence(trains1[i], server, st, 'train')
    trains2obj = Sentence(trains2[i], server, st, 'train')

    tests1obj = Sentence(tests1[i], server, st, type = 'test')
    tests2obj = Sentence(tests2[i], server, st, type = 'test')

    # Add all of them to the corresponding arrays
    trainsentences1.append(trains1obj)
    trainsentences2.append(trains2obj)
    testsentences1.append(tests1obj)
    testsentences2.append(tests2obj)

    # populate the alltags and allners

    allpostags += trains1obj.pos_tags
    allpostags += trains2obj.pos_tags

    allners += trains1obj.nerdict
    allners += trains2obj.nerdict


# Make the allpostags and allners as unique
allpostags = list(set(allpostags))
allners = list(set(allners))


# Since they are now list of tuples, let us only extract the
# pos tags and ner dicts and store them

allpostags = [x[1] for x in allpostags]
allners = [x[1] for x in allners]
# Now construct the pairs

for i in range(len(trainsentences1)):
    s1 = trainsentences1[i]
    s2 = trainsentences2[i]

    # Create the pair object
    p = Pair(s1,s2, trainlabels[i], allpostags, allners)

    trainpairs.append(p)


for i in range(len(testsentences1)):

    s1 = testsentences1[i]
    s2 = testsentences2[i]

    # Create the pair object
    p = Pair(s1,s2, testlabels[i], allpostags, allners)
    testpairs.append(p)


# Store the train and test pairs in a pickle file
pickle.dump(trainpairs, open('trainpairs.pickle','wb'))
pickle.dump(testpairs, open('testpairs.pickle','wb'))


# TODO convert these dictionary objects into matlab mat files
# Scipy has some functionarlity to convert simple python objects to mat files

# We Cannot use these dicts as it is. Scipy does not understand complex datastructures
# We need to save the featurenames seperately and the matrix seperately

# Dumping the training features as a matlab structure
trainvarnames = []
trainfvs = []
for i in range(len(trainpairs)):
    t = trainpairs[0]
    f = t.mappingfvdict
    for (k,v) in f.items():
        trainvarnames.append(k)
        trainfvs.append(v)


sio.savemat('trainmappingfeatnames.mat',{'trainvarnames':trainvarnames})
sio.savemat('trainmappintfeatmat.mat', {'trainfvs' : trainfvs})