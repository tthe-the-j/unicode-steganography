import nltk
nltk.download("twitter_samples")
from nltk.corpus import twitter_samples
from threading import Thread
import pickle
import queue

character_dict = {}

samples = iter(twitter_samples.strings("tweets.20150430-223406.json"))

next_chunk = 0

print(samples)

global write_queue
write_queue = queue.Queue(maxsize=1000)

def writer():
    global write_queue
    with open("dataset.csv") as f:
        while True:
            data = write_queue.get()
            string = ",".join(data)
            f.write(string)

def worker():
    global next_chunk
    try:
        while True:
            # chunk = samples[next_chunk]
            chunk = next(samples)
            next_chunk += 1
            for i in range(len(chunk)):
                #get three adjacent characters
    except StopIteration:
        return


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