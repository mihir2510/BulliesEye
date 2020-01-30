from gensim import corpora, models, similarities
from nltk.tokenize import word_tokenize
from collections import defaultdict
from pprint import pprint
from sqlalchemy.engine import create_engine
import json


def loadAffectiveDictionary(affectiveWordFile):
    affectiveWords = {}
    linecount = 0
    for line in open(affectiveWordFile):
        if linecount>2:
            words = line.split("\t")
            if words[0] not in affectiveWords:
                affectiveWords[words[0]] = {'anger': 0, 'anticipation': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'negative': 0, 'positive': 0, 'sadness': 0, 'surprise': 0, 'trust':0 }
            affective_senses = affectiveWords[words[0]]
            affective_senses[words[1]] = int(words[2])
        linecount = linecount + 1
    return affectiveWords

# calculate affective senses counts
def affective_sense_counts(texts, affectivelexicon_dict):
    affective_senses_counts = {'anger': 0, 'anticipation': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'negative': 0, 'positive': 0, 'sadness': 0, 'surprise': 0, 'trust':0 }
    for text in texts:
        for token in text:
            if token in affectivelexicon_dict:
                affective_senses = affectivelexicon_dict[token]
                for sense in affective_senses_counts:
                    affective_senses_counts[sense] = affective_senses_counts[sense] + int(affective_senses[sense])

    return affective_senses_counts

def get_LDAasJSON(texts):
    # Make dictionary
    dictionary = corpora.Dictionary(texts)
    #dictionary.save('test.dict') # store the dictionary, for future reference

    #Create and save corpus
    corpus = [dictionary.doc2bow(text) for text in texts]
    #corpora.MmCorpus.serialize('test.mm', corpus) # store to disk, for later use

    #Run LDA
    model = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=20)

    tmp = model.show_topics(num_topics=20, num_words=10, log=False, formatted=False)

    return tmp

affectivelexicon_dict = loadAffectiveDictionary('NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt')


engine = create_engine("sqlite:///tweets.db")
connection = engine.connect()
print('Connected')
documents = []
sql = "SELECT pbody FROM Tweets WHERE has_bullying=true;"
result = connection.execute(sql)
for row in result:
    documents.append(word_tokenize(row[0]))
bcount = int(connection.execute('select count(tweet_id) from Tweets where has_bullying=true').scalar())
affective_counts_json = affective_sense_counts(documents, affectivelexicon_dict)
for key in affective_counts_json:
    affective_counts_json[key] = int((affective_counts_json[key] / bcount) * 100)
print(affective_counts_json, 'B')
connection.execute('insert into affective_sense values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (affective_counts_json['anger'], affective_counts_json['anticipation'], affective_counts_json['disgust'], affective_counts_json['fear'], affective_counts_json['joy'], affective_counts_json['negative'], affective_counts_json['positive'], affective_counts_json['sadness'], affective_counts_json['surprise'], affective_counts_json['trust'], 'b'))

documents = []
sql = "SELECT pbody FROM Tweets WHERE has_bullying=false;"
result = connection.execute(sql)
for row in result:
    documents.append(word_tokenize(row[0]))

nbcount = int(connection.execute('select count(tweet_id) from Tweets where has_bullying=false').scalar())
affective_counts_json = affective_sense_counts(documents, affectivelexicon_dict)
for key in affective_counts_json:
    affective_counts_json[key] = int((affective_counts_json[key] / nbcount) * 100)
print(affective_counts_json, 'NB')
connection.execute('insert into affective_sense values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (affective_counts_json['anger'], affective_counts_json['anticipation'], affective_counts_json['disgust'], affective_counts_json['fear'], affective_counts_json['joy'], affective_counts_json['negative'], affective_counts_json['positive'], affective_counts_json['sadness'], affective_counts_json['surprise'], affective_counts_json['trust'], 'nb'))

topic_model_json = get_LDAasJSON(documents)






