__author__ = 'vignesh'
from Sentence import Sentence
from collections import OrderedDict
import sys

class Pair(object):
    """
    This class holds the s1-s1 pair for a particular
    pair of sentences along with the following
    1. Class label ( whether they were a paraphrase or not
    2. hidden variable features ( all the 4 hidden variable feature types )

    """

    s1 = None
    s2 = None
    labels = None
    allpostags = None
    allners = None

    # Features of the pair

    """
    Word mapping features
    """
    wnsim = None
    NEind = None # Indicators ( binary vector ) of all th pos tags we have observed
    posind = None # Indicators ( binary vector ) of all the pos tags we have observed
    mappingfvdict = OrderedDict()

    """
    Word Deletion features
    """
    postags1 = None
    NE1 = None
    postags2 = None
    NE2 = None
    deletionfvdict = OrderedDict()

    """
    Edge mapping features
    """
    depind = None # This must be some sort of indicators of dependencies
    edgemappingfvdict = OrderedDict()

    """
    Edge Deletion featurs
    """

    dep1 = None
    dep2 = None
    edgedeletionfvdict = OrderedDict()



    def __init__(self, s1, s2, labels, allpostags, allners):
        """
        Sets the two sentences that constitute the pair
        :return:
        """

        self.s1 = s1
        self.s2 = s2
        self.labels = labels
        self.allpostags = allpostags
        self.allners = allners

        # Setting the token variables
        self.s1tokens = s1.tokens
        self.s2tokens = s2.tokens

        # Get the word mapping features
        self.get_word_mapping_features()

        # Get the word deletion featurse for sent1

        self.get_word_del_featuers() # deletion features for both the sentences are handled here
        # Get edge mapping features


        # Get edge deletion featurs for sent1


        # Get edge deletion featurse for sent 2

    def getS1(self):
        return self.s1

    def getS2(self):
        return self.s2

    def getLabels(self):
        return self.labels

    def setS1(self,s1):
        self.s1 = s1

    def setS2(self, s2):
        self.s2 = s2

    def setLabels(self, labels):
        self.labels = labels


    def edit_distance(self, s1, s2):
        """
        Gives the edit distance between two words
        :param s1: word 1
        :param s2: word 2
        :return: Edit distance between s1 and s2
        """
        m=len(s1)+1
        n=len(s2)+1

        tbl = {}
        for i in range(m): tbl[i,0]=i
        for j in range(n): tbl[0,j]=j
        for i in range(1, m):
            for j in range(1, n):
                cost = 0 if s1[i-1] == s2[j-1] else 1
                tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

        return tbl[i,j]

    def get_indicators(self, l, s):
        """
        Creates an indicator array by finding the index
        position of each element in the small array in the
        large array
        :param l: The large array
        :param s: The small arry
        :return: Indicator array
        """

        indicarray = [0 for i in range(len(l))]
        for i in range(len(s)):
            temp = s[i]
            try:
                idx = l.index(temp)
            except ValueError:
                continue
            indicarray[idx] = 1

        return indicarray


    def get_word_mapping_features(self):
        """
        Go through every word in s1 and s2 and generate mapping
        features between s1 and s2

        :return:
        """

        # Go through the words in s1 and map it
        # with words in s2

        # Get the tokens assosiated with s1
        tempdict = {}
        ne1 = self.s1.nerdict
        ne2 = self.s2.nerdict

        pos1 = self.s1.pos_tags
        pos2 = self.s2.pos_tags

        s1tokens = self.s1.tokens
        s2tokens = self.s2.tokens

        for i in range(len(s1tokens) ):

            # Named entity features and pos features
            n1 = ne1[i][1]
            p1 = pos1[i][1]

            # Now go through the tokens in the second sentence

            for j in range(len(s2tokens) ):
                wnsim = 0 # TODO need to create function to implement wnsim
                n2 = ne2[j][1]
                p2 = pos2[j][1]

                # Now make the feature vector for mapping between words i and j
                # in sentences s1 and s2 respectively.

                # TODO Currently this code adds the pos and ner tags of
                # both the words. Do we need to add the common ones only?

                posindarr = self.get_indicators(self.allpostags, [p1,p2])
                nerindarr = self.get_indicators(self.allners, [n1,n2])

                # Get the edit distance between the words
                ed = self.edit_distance(s1tokens[i], s2tokens[j])

                # Make the feature vector
                fv = [wnsim] + posindarr + nerindarr +[ed]

                # Add it to the mapping feature vector dictionary
                # self.mappingfvdict[s1tokens[i] + ':' + s2tokens[j]] = fv
                tempdict[s1tokens[i] + ':' + s2tokens[j]] = fv

        self.mappingfvdict = tempdict


    def get_word_del_featuers(self):
        """
        This gives us the word deletion features.
        We will be adding features lik this.

        if we are adding deletion features for words in s1,

        'word: ' : '[ ]'

        If we are adding deletion features for words in s2,

        ' :word' : '[]'

        the [] is the vector of  deletion features.


        :return:
        """


        # Get the tokens assosiated with s1
        ne1 = self.s1.nerdict
        ne2 = self.s2.nerdict

        pos1 = self.s1.pos_tags
        pos2 = self.s2.pos_tags

        s1tokens = self.s1.tokens
        s2tokens = self.s2.tokens

        for i in range(len(s1tokens)):

            # Corresponding pos and ner features are

            p = pos1[i][1]
            n = ne1[i][1]

            # Create the corresponding indicator arrays
            posindarray = self.get_indicators(self.allpostags, p)
            nerindarray = self.get_indicators(self.allners, n)

            # Make a feature vector and add it to the dictionary
            fv = posindarray + nerindarray
            self.deletionfvdict[s1tokens[i] + ': '] = fv


        # Similarly construct the feature vector dictionary for s2 tokens

        for i in range(len(s2tokens)):

            # Corresponding pos and ner features are

            p = pos2[i][1]
            n = ne2[i][1]

            # Create the corresponding indicator arrays
            posindarray = self.get_indicators(self.allpostags, p)
            nerindarray = self.get_indicators(self.allners, n)

            # Make a feature vector and add it to the dictionary
            fv = posindarray + nerindarray
            self.deletionfvdict[ ': '+s2tokens[i]] = fv

    def make_objective_matrix(self):
        """
        This accumulates the feature matrices of the various hidden
        variables and creates a feature matrix that can be consumed
        by the optimization algorithm
        :return:
        """






