import numpy as np

from get_word_funcs import *
from word_functions import *


class Quordle:
    def __init__(self, answer = None):
        self.total_words, self.answer_words, self.acceptable_words = get_words(return_all_lists = True)
        if answer == None:
            self.answer = np.random.choice(self.answer_words, 4)
        else:
            self.answer = answer
        self.guesses = []
        self.hints = []
        self.nguesses = 9
        self.nletters = 5
        self.guess_count = 0
        self.over = False
        self.done = [0, 0, 0, 0]
        self.win = 0
    
    def reset(self, answer = None):
        self.guess_count = 0
        self.guesses = []
        self.hints = []
        self.over = False
        self.done = [0, 0, 0, 0]
        self.win = 0
        if answer == None:
            self.answer = np.random.choice(self.answer_words, 4)
        else:
            assert len(answer) == 4
            self.answer = answer
        
    def guess(self, word):
        if len(word) != self.nletters or word not in self.total_words:
            print('Invalid Guess, Try Again!')
            return [word, similarity_value(word, self.answer)]
        self.guess_count += 1
        self.guesses.append(word)
        hint0 = list(similarity_value(word, self.answer[0]))
        hint1 = list(similarity_value(word, self.answer[1]))
        hint2 = list(similarity_value(word, self.answer[2]))
        hint3 = list(similarity_value(word, self.answer[3]))
        hint = [hint0, hint1, hint2, hint3]
        self.hints.append(hint)
        for i in range(4):
            if word == self.answer[i]:
                self.done[i] = 1
        if self.done == [1,1,1,1]:
            self.win = 1
            self.over = True
            return [word, hint]
        else:
            if self.guess_count == self.nguesses:
                self.over = True
            return word, hint
