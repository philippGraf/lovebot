import numpy as np
import math

class HashtagOptimizer():
    """
    The hashtag optimizer selects a hashtag from a given list of hashtags 
    using the UCB1 algorithm in order to find posts with a lot of hate speech. 
    """
    def __init__(self, alpha=1.0) -> None:
        self.num_pulls = []
        self.total_rewards = []
        self.number_of_hashtags = 0
        self.t = 1
        self.alpha = alpha

    def select_hashtag(self, hashtags:list) -> str: 
        # If the list of hashtags grows during runtime,
        # we extend the UCB1.
        while self.number_of_hashtags < len(hashtags):
            self.num_pulls.append(1)
            self.total_rewards.append(0)
            self.number_of_hashtags += 1 

        ucbs = np.zeros(self.number_of_hashtags)

        for i in range(self.number_of_hashtags):
            mean_reward = self.total_rewards[i] / self.num_pulls[i]
            confidence_bound = self.alpha * math.sqrt(2 * math.log(self.t) / self.num_pulls[i])
            ucbs[i] = mean_reward + confidence_bound
        index = np.argmax(ucbs)

        self.num_pulls[index] += 1
        self.t += 1

        return hashtags[index]

    def update(self, all_hashtags:list, selected_hashtag:str, reward:int):
        for i, hashtag in enumerate(all_hashtags):
            if hashtag == selected_hashtag:
                self.total_rewards[i] += reward
                break
    
