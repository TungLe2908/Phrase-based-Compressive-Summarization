__author__ = 'MichaelLe'

import collections
import process_function
import sentence
from collections import Counter
import numpy as np

class phrase_based_summarization:

    __sentences__ = []

    __number_sentence__ = 0


    def __init__(self, sentences):

        n = len(sentences)
        self.__number_sentence__ = n
        self.__sentences__ = sentences
        list_phrase = []
        for sentence in sentences:
            for phrase in sentence.__phrase__:
                list_phrase.append(phrase[2])

        self.__number__phrase__ = len(list_phrase)

        self.__phrase_frequency__ = Counter(list_phrase)

        list_biword = []
        list_word = []
        for sentence in sentences:
            content = [w.lower() for w in sentence.__content__]
            len_content = len(content)
            for i in range(len_content - 1):
                biword = " ".join(content[i:i+2])
                list_biword.append(biword)

            for i in range(len_content):
                list_word.append(content[i])
        self.__number_word__ = len(list_word)
        self.__number_biword__ = len(list_biword)

        self.__biword_frequency__ = Counter(list_biword)
        self.__word_frequency__ = Counter(list_word)

    def phrase_score_function(self, phrase):
         return self.__phrase_frequency__[phrase]

    def bigram_score(self, content):

        if (content == None): return 0
        if (content == ""): return 0

        k = self.__number_word__*1.0/self.__number_biword__

        len_sen = len(content)
        score = 0
        content = np.char.lower(content)
        for i in range(len_sen-1):
            score = score + k*(self.__biword_frequency__[" ".join(content[i:i + 2])]) /(self.__word_frequency__[content[i]])
        return score

    def dist_sentence(self, sentence, mode = "word"):
        if (mode == "word"):
            content = [ w.lower() for w in (sentence.__content__) ]
            phrase = sentence.__phrase__
            number_phrase = len(phrase)
            sum = 0
            for i in range(number_phrase - 1):
                sum = sum + self.dist_phrase(phrase[i],phrase[i+1])
            return sum
        else:
            return 0

    def dist_phrase(self, phrase1, phrase2):
        return abs(phrase2[0] - phrase1[1] - 1)

    def get_score_bi_phrase(self, previous_phrase, phrase_cur, parameter_d,parameter_epi, phrase_frequency, threshold):
        tmp_content = (previous_phrase[2] + " " + phrase_cur[2]).split()
        bigram_pre = self.bigram_score(tmp_content)
        previous_score = self.phrase_score_function(previous_phrase[2]) * parameter_d * phrase_frequency[
            previous_phrase[2]] + parameter_epi * self.dist_phrase(previous_phrase, phrase_cur) + bigram_pre
        if (previous_score / (len(phrase_cur[2]) + len(previous_phrase[2]))) > threshold:
            return 1
        else:
            return 0

    def get_max_density_compression(self, sent, summary, parameter):
        """

        :param sent:
        :param summary:
        :param parameter:
            parameter_d = parameter[0]
            parameter_epi = parameter[1]
            threshold_select = parameter[2]
            threshold_pre = parameter[3]
            threshold_next = parameter[4]
        :return:
        """
        # build the dictionary for summary as ["phrase": frequency]

        parameter_d = parameter[0]
        parameter_epi = parameter[1]
        threshold_select = parameter[2]
        threshold_pre = parameter[3]
        threshold_next = parameter[4]

        list_phrase = []

        tmp_summary = []
        for sen in summary:
            tmp_summary.append(sen)
        tmp_summary.append(sent)

        for s in tmp_summary:
            for p in s.__phrase__:
                list_phrase.append(p[2])

        phrase_frequency = Counter(list_phrase)

        number_phrase = len(sent.__phrase__)

        phrase = sent.__phrase__

        mask = np.zeros(number_phrase, dtype=int)

        kept = []

        for i in range(len(phrase)):
            p = phrase[i]
            if (self.phrase_score_function(p[2])* parameter_d * phrase_frequency[p[2]] >threshold_select):
                kept.append(p)
                mask[i] = 1

        threshold = 1
        while (np.sum(mask) != number_phrase):
            cur_mask = np.sum(mask)
            for i in range(number_phrase):
                if mask[i] != 0:
                    #mask[i] = 0
                    if (i - 1 >= 0):
                        phrase_cur = phrase[i]
                        previous_phrase = phrase[i - 1]
                        mask[i - 1] = self.get_score_bi_phrase(previous_phrase, phrase_cur, parameter_d,
                                                               parameter_epi, phrase_frequency, threshold_pre)
                    if (i +1 < number_phrase):
                        next_phrase = phrase[i + 1]
                        phrase_cur = phrase[i]
                        mask[i + 1] = self.get_score_bi_phrase(phrase_cur, next_phrase, parameter_d,
                                                               parameter_epi, phrase_frequency, threshold_next)
            if (cur_mask == np.sum(mask)): break
        content = sent.__content__

        cur_idx = 0
        list_word = []
        for i in range(number_phrase):
            for j in range(cur_idx, (phrase[i])[0] - 1, 1):
                list_word.append((content[j], 0))
            if mask[i] != 0:
                for j in range((phrase[i])[0] - 1, (phrase[i])[1], 1):
                    list_word.append((content[j], i + 1))
            cur_idx = (phrase[i])[1]
        for i in range(cur_idx, len(content), 1):
            list_word.append((content[i], 0))

        new_content = []
        n = len(list_word)
        phrases = []
        i = 0

        while (i<n):
            new_content.append((list_word[i])[0])
            if (list_word[i])[1] != 0:
                j = i
                phrase = ""
                label = (list_word[i])[1]
                new_content.pop()
                while (j<n and (list_word[j])[1] == label ):
                    new_content.append ((list_word[j])[0])
                    j += 1
                phrases.append((i + 1, j))
                i = j
            else: i+=1

        if (len(new_content) > 0):
            return sentence.sentence(" ".join(new_content),phrases)
        else: return None

    def scoring_function(self, summary, parameter):
        """

        :param summary: --list--obj:sentence-- the set of sentence is chosen for summary
        :param phrase_set: --dict-- the set of phrase in summary
        :param parameter: --list-- the parameter for this function
            parameter_d = parameter[0]
            nuy = parameter[1]
        :return:
        """
        nuy = parameter[1]
        parameter_d = parameter[0]
        result = 0
        for sen in summary:
            bigramscore = self.bigram_score(sen.__content__)
            dist = self.dist_sentence(sen)
            phrase_score = 0
            #print("----------------------------")
            for ph in sen.__phrase__:
                phrase_score += self.phrase_score_function(ph[2])*parameter_d
                #print(ph[2], ' ', phrase_score)
            #print("----------------------------")
            #print(phrase_score,' ',bigramscore,' ', dist)
            result += phrase_score + bigramscore + nuy*dist
        return result

    def summarizer(self, parameter):
        parameter_d = parameter[0]
        parameter_epi = parameter[1]
        threshold_select = parameter[2]
        threshold_pre = parameter[3]
        threshold_next = parameter[4]
        #######################################
        parameter_d = parameter[0]
        nuy = parameter[1]

        parameter_scoring_function = []
        parameter_scoring_function.append(parameter_d)
        parameter_scoring_function.append(nuy)

        parameter_epi = parameter[2]
        threshold_select = parameter[3]
        threshold_pre = parameter[4]
        threshold_next = parameter[5]

        parameter_max_density = []
        parameter_max_density.append(parameter_d)
        parameter_max_density.append(parameter_epi)
        parameter_max_density.append(threshold_select)
        parameter_max_density.append(threshold_pre)
        parameter_max_density.append(threshold_next)

        budget = parameter[6]

        ######################################
        summary = []
        max_score = 0
        num_sentence = len(self.__sentences__)
        sentences = self.__sentences__
        max_idx = -1
        for i in range(num_sentence):
            tmp_sum = []
            new_sentence = self.get_max_density_compression(sentences[i], summary, parameter_max_density)
            if (new_sentence != None):
                tmp_sum.append(new_sentence)
                tmp_score = self.scoring_function(tmp_sum,parameter_scoring_function)
                if (tmp_score >= max_score):
                    max_idx = i
                    max_score = tmp_score

        sum_one_sentence = []
        sum_one_sentence.append(self.get_max_density_compression(sentences[max_idx], summary, parameter_max_density))

        mask_select = np.ones(num_sentence)

        cur_cost = 0

        while (np.sum(mask_select) != 0):
            max_score = 0
            index = -1
            selected_sentence = None
            for i in range(num_sentence):
                if (mask_select[i] != 0):
                    new_sentence = self.get_max_density_compression(sentences[i],summary,parameter_max_density)
                    tmp_sum = []
                    if (new_sentence != None):
                        tmp_sum.append(new_sentence)
                        tmp_score = self.scoring_function(tmp_sum,parameter_scoring_function)/ len(new_sentence.__content__)
                        if (tmp_score >= max_score):
                            selected_sentence = new_sentence
                            index = i
                            max_score = tmp_score
                    else: mask_select[i] = 0


            #print("selected: ", index)
            if (selected_sentence != None):
                if (cur_cost + len(selected_sentence.__content__) <= budget ):
                    #print("Satisfied")
                    summary.append(selected_sentence)
                    cur_cost += len(selected_sentence.__content__)

            if (index == -1): break
            #else: #print("no")
            mask_select[index] = 0

        final_summary = []

        # if (self.scoring_function(sum_one_sentence,parameter_scoring_function) >= self.scoring_function(summary,parameter_scoring_function)):
        #     final_summary = sum_one_sentence
        #     print("Choose one sentence")
        # else:
        #     final_summary = summary

        final_summary = summary

        result = ""
        for i in range(len(final_summary)-1):
            result+= " ".join(final_summary[i].__content__)
            result +=" "
        result += " ".join(final_summary[len(final_summary)-1].__content__)
        return result


# aligns = np.load("data/preprocessing.npy")
# phrase = phrase_based_summarization(aligns[:15])
#
# np.save("data/summary.npy",phrase)
#phrase = np.load("data/summary.npy")

#
#
# print("ok")
#
#
#
# summary = []
# parameter = []
#
# parameter.append(0.1) #paramter_d
# parameter.append(0.1) #nuy
# parameter.append(0.05) #parameter_epi
# parameter.append(0.5) #parameter_select
# parameter.append(0.5) #parameter_pre
# parameter.append(0.5) #paramter_next
# parameter.append(46)  #budget
#
#
# summary.append(aligns[0])
# summary.append(aligns[2])
# summary.append(aligns[5])
# summary.append(aligns[1])
#
# phrase.summarizer(parameter)
#print phrase.get_max_density_compression(aligns[2],[],parameter)
# #print(phrase.dist_sentence(aligns[1]))
# phrase.get_max_density_compression(aligns[3],summary,0.1, 0.1)