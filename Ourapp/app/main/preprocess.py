import re, string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess(text, stemming=False):

    # Lowercase
    text = text.lower()
    # Remove whitespaces
    text = text.strip()
    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Removing emojis
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Remove stopwords
    text = word_tokenize(text)
    text = [i for i in text if not i in stop_words]

    # Remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    text = [t.translate(table) for t in text]

    # Stemming
    if stemming: 
        text = [stemmer.stem(token) for token in text]
    
    # Removing empty strings
    text = [t for t in text if len(t.strip()) > 0]
    
    return text

if __name__ == '__main__':
    print(preprocess('Hello! amigo, ssup my friend    '))
