import numpy as np
import copy

def min(a, b):
    if a> b: return b
    else: return a
def max(a,b):
    if a<b: return b
    else: return a
def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

class sentence:
    __content__ = []


    def __init__(self, content, phrase):
        self.__content__ = content.split()

        n = len(self.__content__)
        words = np.char.lower(content.split())

        self.__phrase__ = []

        ## intersection/union phrase
        num_phrase = len(phrase)
        i = 0
        while (i < num_phrase):
            for j in range(num_phrase):
                if (i != j):
                    tmp_set = intersect(phrase[i], phrase[j])
                    if len(tmp_set) > 0:
                        phrase[min(i,j)] = union(phrase[i], phrase[j])
                        phrase[max(i, j)] = ()
                        #i = max(i - 1, 0)

            i += 1

        tmp_phrase = []
        for i in range(num_phrase):
            if (len(phrase[i]) != 0):
                tmp_phrase.append(phrase[i])
        phrase = tmp_phrase
        num_phrase = len(phrase)
        ## order phrase list
        mask = np.zeros(n, dtype=int)
        order_phrase = []
        for i in range(num_phrase):
            mask[(phrase[i])[0] - 1] = i + 1
        new_phrase = []
        for i in range(n):
            if mask[i] != 0:
                new_phrase.append(phrase[mask[i] - 1])


        # i = 0
        for p in new_phrase:
            list_word_in_phrase = []
            for i in range(p[0] - 1, p[-1],1):
                list_word_in_phrase.append(words[i])
                #words[i] = ""
            self.__phrase__.append([p[0], p[-1], " ".join(list_word_in_phrase)])

    def set_phrase(self, new_phrase):
        self.__phrase__ = new_phrase

        ######## INCLUDE WORDS AS PHRASE #############
        ##############################################
        # self.__phrase__ = []
        #
        #
        # mask = np.zeros(n, dtype=int)
        # order_phrase = []
        # for i in range(len(phrase)):
        #     mask[(phrase[i])[0] - 1] = i + 1
        #
        # i = 0
        # while (i < n):
        #     if (mask[i] != 0):
        #         tmp_phrase = phrase[mask[i] - 1]
        #         order_phrase.append(tmp_phrase)
        #         i = i + len(tmp_phrase)
        #     else:
        #         tmp_phrase = [i + 1]
        #         order_phrase.append(tmp_phrase)
        #         i = i + 1
        #
        # for p in order_phrase:
        #     list_word_in_phrase = []
        #     for i in range(p[0] - 1, p[-1],1):
        #         list_word_in_phrase.append(words[i])
        #         words[i] = ""
        #     self.__phrase__.append(" ".join(list_word_in_phrase))


