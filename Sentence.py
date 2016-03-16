__author__ = 'vignesh'

# Imports
#-----------------------------------------
from nltk.tokenize import word_tokenize
import nltk
import jsonrpc
from jsonrpc import *
from json import loads
import re
from nltk.tag.stanford import StanfordNERTagger
import ConfigParser as CP

# Setting for handling the unicode issue
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#-----------------------------------------

class Sentence(object):
    """

    """
    orig_sent = None
    # pos_tags = None # TODO Make these as tuples as opposed to tdicts
    pos_tags = [] # They are currently represented as a list of tuples instead of dicts
    tokens = None
    deps = None # Dependency parsing dependencies
    # nerdict = None # Dictionary of Named entities for a sentenceconfig.py # TODO Make these as tuples as opposed to tdicts
    nerdict = [] # Even though called as dict ; are currently represented as a list of tuples
    labels = None # Class labels
    # candidatepos = [] # Candidate positions in the sentence
    type = 'train' # Tells if the sentence is a training or testing sentence or unlabelled

    config = None

    # set config file
    config = CP.RawConfigParser()
    config = config
    config.read('config.py')

    # Dependency parsing server
    server = None

    # Named entity tagger
    st = None



    def __init__(self, sent, server, st, type = 'train'):

        # Curate annotated sentence
        sent = sent.strip(" \n\r")
        self.type = type
        self.orig_sent = sent
        # self.tokens = self.get_tokens()
        self.server = server
        self.st = st
        self.set_pos_tags()
        self.set_dep()
        self.set_ner()
        self.set_class_labels()


    def get_tokens(self):
         # remove punctuations
        punctuations = [',','//','/','?','.','!','"','\'']
        sent = self.orig_sent
        for p in punctuations:
            sent = sent.replace(p,'')
        tokens = word_tokenize(sent)
        return tokens

    def set_pos_tags(self):

        print 'Making pos tags...\n'

        if self.orig_sent == None:
            raise 'Error! Original sentence empty'
		
		 # remove punctuations
        punctuations = [',','//','/','?','.','!','"','\'']
        sent = self.orig_sent
        for p in punctuations:
            sent = sent.replace(p,'')
        tokens = word_tokenize(sent)
        # tokens = sent.split()
        tagsandwords = nltk.pos_tag(tokens)
        #onlytags = [x[1] for x in tagsandwords]
        # self.pos_tags = dict(tagsandwords)
        self.pos_tags = tagsandwords # List of tuples


    def set_dep(self):

        """
        Get dependency parsing tags
        :return:
        """
        print 'Generating dependency tree ...'

        #TODO: Check if we need to create a word object and store dependencies
        server = self.server
        s = self.orig_sent # Getting
        try:
            result = loads(server.parse(s)) # This generates the dependencies
        except RPCInternalError:
            print 'Corenlp server is not available'
            return
        dependencies = []
        try:
            sentences = result['sentences']
            for i in range(len(sentences)):
                dep = result['sentences'][i]['dependencies'] # Get the dependencies from the json
                dependencies += dep

            self.deps = dependencies
        except KeyError: # happens when the sentence is sometimes too long
            self.deps = []

    def set_ner(self):


        nertags = self.st.tag(self.orig_sent.split())

        # Make a dictionary of the tags and store it
        # nerdict = dict(nertags)
        # self.nerdict = nerdict
        self.nerdict = nertags
        self.tokens = []

        # NER tags define the tokens in the input String
        for i in range(len(nertags)):
            self.tokens.append(nertags[i][0])


    def set_class_labels(self,):
        """
        Sets the class labels for this sentence
        :return:
        """

        # TODO finish this

