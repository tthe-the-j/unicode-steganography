import nltk
nltk.download("twitter_samples")
from nltk.corpus import twitter_samples
from threading import Thread
import pickle
import queue
import pandas as pd

character_dict = {}

samples = iter(twitter_samples.strings("tweets.20150430-223406.json"))

next_chunk = 0

print(samples)

write_queue = queue.Queue(maxsize=1000)

df = pd.DataFrame(columns=["previous","current","next"])


def writer():
    while True:
        global write_queue
        global df
        df.append(write_queue.get())


def worker():
    global next_chunk
    try:
        while True:
            # chunk = samples[next_chunk]
            chunk = next(samples)
            next_chunk += 1
            for i in range(len(chunk)):
                current_character = chunk[i]
                try:
                    previous_character = chunk[i-1]
                except IndexError:
                    previous_character = "SOL"
                try:
                    next_character = chunk[i+1]
                except IndexError:
                    next_character = "EOL"
                data = [previous_character, current_character, next_character]
                write_queue.put(data)
    except StopIteration:
        if write_queue.not_empty:
            ...
            #put stuff on queue to stop writer


num_workers = 100

if __name__ == "__main__":
    for i in range(num_workers):
        t = Thread(target=worker)
        t.start()
    print("started threads")

print(character_dict)

"""
with open("unicode_statistics.pickle","wb") as f:
    pickle.dump(character_dict,f)"""