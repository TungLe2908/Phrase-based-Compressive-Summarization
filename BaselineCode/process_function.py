import codecs
import re
import numpy as np
import sentence

def get_align(data):
    '''
    :param data:
        align sentence from giza++
    :return:
        a list example
        [ [1,2,3], [4], ....]
        mean: Null ({ 1 2 3 }) ABC ({ 4 }) ...
    '''

    words = data.split()

    number_align = words.count("({")

    aligns = []

    for i in range(number_align):
        align = []
        start_idx = words.index('({')
        end_idx = words.index('})')

        for j in range(start_idx + 1, end_idx,1):
            align.append(int(words[j]))
        aligns.append(align)
        words[start_idx] = ""
        words[end_idx] = ""
    return aligns

def get_phrase2align(align):
    phrases = []
    align = sorted(align)
    n = len(align)
    mask = np.zeros(n,dtype=int)
    i = 0

    while (i < n - 1):
        for j in range(i, n-1, 1):
            if (align[j] +1 == align[j+1]):
                mask[i] +=1
            else: break
        i += mask[i] + 1
    phrases = []
    for i in range(n - 1):
        if (mask[i] > 0):
            phrase = align[i:i + mask[i] + 1]
            phrases.append(phrase)
    return phrases


def split_phrase(aligns_st, aligns_ts):

    #expand aligns_ev
    number_st = len(aligns_st)
    number_ts = len(aligns_ts)

    for i in range(number_st):
        for j in range(number_ts):
            if (i  in aligns_ts[j]) == True :
                if (j in aligns_st[i]) == False:
                    aligns_st[i].append(j)
        aligns_st[i] = np.sort(aligns_st[i])

    #print (aligns_st)
    # rules: if 1 - n (from source - target) and n words is continuous, they're in same phrase.
                # If not, find the longest continuous substring in list expanded word
    phrases = []
    ############################
    ####### 1: except null
    ####### 0: include null
    #############################
    for i in range(0, len(aligns_st),1):
        align = aligns_st[i]
        tmp_phrase = get_phrase2align(align)
        for tp in tmp_phrase:
            phrases.append(tp)

    return phrases

def get_phrase(source_file, target_file, outputfile):
    """
    :param source_file: the link to source file (in giza++ format)
    :param target_file: like above
    :return:
        the phrases for each sentence
    """
    # get aligns in source data
    f = codecs.open(source_file, encoding="utf-8")
    source_data = f.read().split('\n')
    source_aligns = []
    n = len(source_data)/3
    for i in range(n):
        source_aligns.append(get_align(source_data[2 + i*3]))

    # get aligns in source data
    f = codecs.open(target_file, encoding="utf-8")
    target_data = f.read().split('\n')
    target_aligns = []
    for i in range(n):
        target_aligns.append(get_align(target_data[2 + i * 3]))
    number_sentence = len(target_aligns)
    phrased_sentence = []
    for i in range(number_sentence):
        sen = sentence.sentence(source_data[1 + i*3],split_phrase(source_aligns[i], target_aligns[i]))
        phrased_sentence.append(sen)

    np.save(outputfile,phrased_sentence)
    #f = np.open("data/preprocessing",mode = "w", encoding='utf-8')
    #f.write(phrased_sentence)

# outputfile = "data/preprocessing_nonull.npy"
#
# get_phrase("data/envn.FINAL","data/vnen.FINAL", outputfile=outputfile)
# print "ok"
#
# aligns = np.load(outputfile)
# print aligns[0].__phrase__
#
