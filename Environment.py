import numpy as np

from get_word_funcs import *
from word_functions import *
from Quordle import *

class Environment:
    reward_one_correct = 2
    reward_win = 10
    reward_lose = -10
    
    def __init__(self, answer = None):
        self.score = 0
        self.rewards = [0]
        self.total_words = get_words()
        self.quordle = Quordle(answer)
        self.num_guesses = 0
        self.state = np.zeros(1695)
        self.state[0] = self.quordle.nguesses
        self.guess_to_state()
        self.action_space = np.array(range(len(self.total_words)))
        self.done = [0,0,0,0]
        
    def reset(self, answer = None):
        self.score = 0
        self.rewards = [0]
        self.quordle.reset(answer)
        self.num_guesses = 0
        self.state = np.zeros(1695)
        self.state[0] = self.quordle.nguesses
        self.guess_to_state()
        self.action_space = np.array(range(len(self.total_words)))
        self.done = [0,0,0,0]
        

    def guess_to_state(self):
        """ 
        State is as follows:
        First position is number of guesses left
        Next 26 positions is whether letter has been attempted or not
        Positions 27 + 26*i to 27 + 26*(i+1) for i in (0, 1, 2, 3) have a 1 if the corresponding letter is found in the word
        For positions 131-521, it is as follows:
        A: [No, Maybe, Yes] for first letter
        B: [No, Maybe, Yes] for first letter
        ...
        Until you go through all 5 letters of word.
        """
        if self.num_guesses == 0:
            self.state[0] = self.quordle.nguesses
            #Mark every letter in every position as maybe
            for k in range(4):
                for i in range(130):
                    self.state[131 + 390*k + 1+3*i] = 1
        elif self.num_guesses > 0:
            self.state[0] = self.quordle.nguesses - self.num_guesses
            guess = self.quordle.guesses[-1]
            hint = self.quordle.hints[-1]
            
            #No pass through
            for k in range(4):
                for i in range(5):
                    val = ord(guess[i]) - ord('a')
                    if hint[k][i] == 0:
                        for j in range(5):
                            self.state[131 + 390*k + 26*3*j + 3*val] = 1
                            self.state[131 + 390*k + 26*3*j + 3*val+1] = 0
                            self.state[131 + 390*k + 26*3*j + 3*val+2] = 0
                    if hint[k][i] == 1:
                        self.state[27 + 26*k + val] = 1
                        self.state[131 + 390*k + 26*3*i + 3*val] = 1
                        self.state[131 + 390*k + 26*3*i + 3*val + 1] = 0
                #Yes Pass Through
                for i in range(5):
                    val = ord(guess[i]) - ord('a')
                    self.state[1+val] = 1
                    #If green for a certain letter, make sure all other letters cannot be in that place.
                    if hint[k][i] == 2:
                        self.state[27 + 26*k + val] = 1
                        for j in range(26):
                            self.state[131 + 390*k + 26*3*i + 3*j + 1] = 0
                            self.state[131 + 390*k + 26*3*i + 3*j] = 1
                        self.state[131 + 390*k + 26*3*i + 3*val + 2] = 1
                        self.state[131 + 390*k + 26*3*i + 3*val] = 0
        for j in range(1,5):
            self.state[-j] = self.quordle.done[-j]

        
    def step(self, action):
        self.num_guesses += 1
        guess, hint = self.quordle.guess(self.total_words[action])
        self.guess_to_state()
        reward = 0
        for i in range(4):
            if guess == self.quordle.answer[i] and self.quordle.done[i] != self.done[i]:
                self.done[i] = 1
                reward += self.reward_one_correct
        if self.quordle.win:
            #Reward more for faster wins
            reward += (self.quordle.nguesses + 1 - self.num_guesses)*self.reward_win
        elif not self.quordle.win and self.quordle.over:
            reward += self.reward_lose
        self.rewards.append(reward)
        state = self.state
        over = self.quordle.over
        return state, reward, over
