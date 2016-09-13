# from summarize import summarize
# import sys
# from os import walk
# import os
# from BingTranslator import Translator
#
# # from sum_lib import summarize
# #
# # import nltk
# # nltk.download(['stopwords', 'punkt'])
#
# # def count_num_sen(dir_gold_corpus, dir_out, list_topics):
# #     number_topic = len(list_topics)
# #     out = open(dir_out + "budget_sentence.txt", mode="w+")
# #     for topic in list_topics:
# #         #get the list of file in topic
# #         list_docs = []
# #         for (dirpath, dirnames, filenames) in walk(dir_gold_corpus + (topic[:-9])):
# #             list_docs.extend(filenames)
# #         num_char = 0
# #         for doc in list_docs:
# #             f = open(dir_gold_corpus+topic[:-9]+"/" + doc, mode="r+").read()
# #             num_char += len(f.split("\n"))
# #         budget = int(num_char*1.0/len(list_docs))
# #         out.write(str(budget))
# #         out.write("\n")
# #     out.close()
# #
# mypath = "data/topics"
#
# list_topics = []
# for (dirpath, dirnames, filenames) in walk(mypath):
#     list_topics.extend(filenames)
#
# reload(sys)
# sys.setdefaultencoding('utf-8')
#
# number_topic = len(list_topics)
#
# #count_num_sen(dir_gold_corpus="data/goldvn/", dir_out="data/budget/",list_topics=list_topics)
#
# budget = open("data/budget/budget_sentence.txt","r").read().split("\n")
# # print budget
#
# # ss = summarize.SimpleSummarizer()
#
# client_id = "tuesdayhcm"
# client_secret = "123456789secretkey123456789"
#
# translator = Translator(client_id, client_secret)
#
# for i in range (len(list_topics)):
#     text = open("data/topics/" + list_topics[i],"r+").read()
#     output = open("data/baselinesummary/"+list_topics[i], "w")
#     summary = ""
#     #text=text.encode("utf-8")
#     try:
#         # summary = ss.summarize(text, budget[i])
#         summary = summarize(text=text,sentence_count=int(budget[i]),language='english')
#
#         #translated
#         phrase_translated = translator.translate(summary, "vi") #translating phrase
#         output.write(phrase_translated)
#     except:
#         print(list_topics[i])
#         output.write("")
#         output.close()
#         #os.remove("data/baselinesummary/"+list_topics[i])
#     print(i)
#     #summary = ss.summarize(text,budget[i])

#
#
#
#


# import urllib
#
from textblob import TextBlob
# from translate import translator
# from BingTranslator import Translator
#
#
text = "I am a student"
blob = TextBlob(text)
print blob.translate(to='vi')