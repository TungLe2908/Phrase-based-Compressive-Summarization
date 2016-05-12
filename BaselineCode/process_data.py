from textblob import TextBlob
import codecs
import sys
from nltk import tokenize
import os
import numpy as np
import PhraseBaseSummarization
import sentence
from os import walk


mypath = "data/topics"


list_topics = []
for (dirpath, dirnames, filenames) in walk(mypath):
    list_topics.extend(filenames)

reload(sys)
sys.setdefaultencoding('utf8')

number_topic = len(list_topics)
#number_topic= 20
############# PREPARE ###############################################################################
def count_num_sen(dir_gold_corpus, dir_out, list_topics):
    number_topic = len(list_topics)
    out = open(dir_out + "budget", mode="w")
    for topic in list_topics:
        #get the list of file in topic
        list_docs = []
        for (dirpath, dirnames, filenames) in walk(dir_gold_corpus + (topic[:-9])):
            list_docs.extend(filenames)
        num_char = 0
        for doc in list_docs:
            f = open(dir_gold_corpus+topic[:-9]+"/" + doc, mode="r")
            num_char += len(f.read().split())
        budget = int(num_char*1.0/len(list_docs))
        out.write(str(budget))
        out.write("\n")
    out.close()

def split_gold(dir_gold_corpus, dir_out, list_topics):
    number_topic = len(list_topics)
    for topic in list_topics:
        # get the list of file in topic
        list_docs = []
        for (dirpath, dirnames, filenames) in walk(dir_gold_corpus + (topic[:-9])):
            list_docs.extend(filenames)
        num_char = 0
        if not os.path.exists(dir_out+topic[:-9]):
            os.makedirs(dir_out+topic[:-9])
        for doc in list_docs:
            f = open(dir_gold_corpus + topic[:-9] + "/" + doc, mode="r")
            sentences = f.read().decode("utf8", "replace").split('\n')
            out = open(dir_out+topic[:-9]+"/"+doc,"w")
            list_sentece = []
            for i in range(len(sentences)):
                if (i%2 != 0):
                    list_sentece.append(sentences[i])
                    list_sentece.append("\n")
            out.writelines(list_sentece[:-1])
            out.close()
#
# split_gold("data/gold/","data/goldvn/", list_topics[:number_topic])
# count_num_sen("data/goldvn/", "data/budget/", list_topics[:number_topic])

##################################################################################################

def find_index(list_words, phrase, start, end):
    index = -1
    for i in range(start, end, 1):
        if (list_words[i] == phrase[0]):
            index = i
            for j in range(len(phrase)):
                if (list_words[i + j] != phrase[j]):
                    index = -1
            if index != -1: return index

    return index

def translated(list_topics, start_idx, end_idx, dir_topic, dir_out, paramter):
#Translate

    fileBudget = open("data/budget/budget","r")
    budget_string = fileBudget.read().split("\n")
    budget = []
    for i in range(len(budget_string)-1):
        budget.append(int(budget_string[i]))

    number_sentence = 0

    for i in range(start_idx, end_idx,1):
        print("process " + list_topics[i])
        file = open(dir_topic + list_topics[i], mode="rb")
        parameter[-1] = budget[i]
        sentences = file.read().decode("utf8","replace").split('\r\n')
        phrase_sentences = []
        for line in sentences:
            if len(line) != 0:
                number_sentence += 1
                phrase= []
                try:
                    blob = TextBlob(line)
                    translated_blob = blob.translate(to='vi')
                    out_sen = " ".join(translated_blob.tokens)
                    start = 0
                    out_sen_tmp = out_sen.lower().split()
                    end = len(out_sen_tmp)
                    for nphrase in translated_blob.noun_phrases:
                        phrase_ele = []
                        nphrase = nphrase.split()
                        k = find_index(out_sen_tmp,nphrase,start, end)
                        start = k + len(nphrase)
                        for j in range(k,k + len(nphrase),1):
                            phrase_ele.append(j+1)
                        phrase.append(phrase_ele)

                except:
                    out_sen = line
                    phrase = []
            if (out_sen != "" ):
                sen = sentence.sentence(out_sen,phrase)
                phrase_sentences.append(sen)


        summarizer = PhraseBaseSummarization.phrase_based_summarization(phrase_sentences)
        summary =summarizer.summarizer(parameter)

        fileOut = open(dir_out+list_topics[i],"w")
        fileOut.write(summary)

        print("finish " + list_topics[i])
        fileOut.close()

    print "no.sentence: ", number_sentence

parameter=[]
parameter.append(0.025)  # paramter_d
parameter.append(-1.75)  # nuy
parameter.append(-1.75)  # parameter_epi
parameter.append(0.0001)  # parameter_select
parameter.append(0.0001)  # parameter_pre
parameter.append(0.0001)  # paramter_next
parameter.append(0)  # budget

# translated(list_topics[:number_topic],0, number_topic,"data/topics/","data/summary/", parameter)




#
# def expand_data(list_topics, dir_root, dir_topic, dir_translated, dir_out):
#     for i in range(number_topic):
#         file_en = open(dir_root + "/en")
#         file_vn = open(dir_root + "/vn")
#
#         file_en_translated = open(dir_topic + "/" + list_topics[i] , mode="r")
#         file_vn_translated = open(dir_translated + "/" + list_topics[i] , mode="r")
#
#         fileOut = open(dir_out + "/en" + str(i) , mode="w")
#         fileOut.write(file_en.read())
#         sentences = file_en_translated.read().decode("utf8", "replace").split('\n')
#         for line in sentences:
#             words = tokenize.word_tokenize(line)
#             fileOut.write(" ".join(words))
#             fileOut.write("\n")
#         fileOutvn = open(dir_out + "/vn" + str(i), mode = "w")
#         fileOutvn.write(file_vn.read())
#         fileOutvn.write(file_vn_translated.read())
#
#
#         fileOut.close()
#         fileOutvn.close()
#
#         print ("finish "+ list_topics[i])
