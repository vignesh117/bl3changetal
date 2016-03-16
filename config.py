[init]


trains1 = /Users/vigneshganapathiraman/Documents/Phd/ConvexOptimization/paper/baseline3/experiment1/train_sentences1.txt
trains2 = /Users/vigneshganapathiraman/Documents/Phd/ConvexOptimization/paper/baseline3/experiment1/train_sentences2.txt
tests1=/Users/vigneshganapathiraman/Documents/Phd/ConvexOptimization/paper/baseline3/experiment1/test_sentences1.txt
tests2=/Users/vigneshganapathiraman/Documents/Phd/ConvexOptimization/paper/baseline3/experiment1/test_sentences2.txt

trainfile = /Users/vigneshganapathiraman/Documents/Phd/Courses/fall15/CS521SNLP/ClassProject/corpus/Annotated/corpus1025.txt
testfile = /Users/vigneshganapathiraman/Documents/Phd/Courses/fall15/CS521SNLP/ClassProject/corpus/LabelledFirstSet/allfiles/corpus1025fixed.txt
trainlabels = /Users/vigneshganapathiraman/Documents/Phd/ConvexOptimization/paper/baseline3/experiment1/train_labels.txt
testlabels = /Users/vigneshganapathiraman/Documents/Phd/ConvexOptimization/paper/baseline3/experiment1/test_labels.txt


reportdir = /Users/vigneshganapathiraman/Documents/Phd/Courses/fall15/CS521SNLP/ClassProject/corpus/toReport

[NER]
classifier=/Users/vigneshganapathiraman/Documents/Phd/Courses/fall15/CS521SNLP/ClassProject/StanfordNERTagger/stanford-ner-2015-04-20/classifiers/english.muc.7class.distsim.crf.ser.gz
tagger=/Users/vigneshganapathiraman/Documents/Phd/Courses/fall15/CS521SNLP/ClassProject/StanfordNERTagger/stanford-ner-2015-04-20/stanford-ner.jar

[CV]
cv = 1
perclass = 1
featgroupres = 0

# For LU learning
[LU]
lu = 0