import nltk
nltk.download("twitter_samples")
from nltk.corpus import twitter_samples
from threading import Thread
import pickle

character_dict = {}

samples = iter(twitter_samples.strings("tweets.20150430-223406.json"))

next_chunk = 0

print(samples)

def worker():
    global next_chunk
    try:
        while True:
            # chunk = samples[next_chunk]
            chunk = next(samples)
            next_chunk += 1
            for character in chunk:
                if not character in character_dict.keys():
                    character_dict[character] = 1
                else:
                    character_dict[character] += 1
    except StopIteration:
        return


num_workers = 100

if __name__ == "__main__":
    for i in range(num_workers):
        t = Thread(target=worker)
        t.start()
    print("started threads")

print(character_dict)

with open("unicode_statistics.pickle","wb") as f:
    pickle.dump(character_dict,f)