import inflect
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


class TextCleaner:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def read_file(self):
        with open(self.input_file, 'r') as file:
            text = file.read()
            return text.lower()

    def filter_text(self, text):
        text = self.process_nums(text)
        text = self.process_punctuations(text)
        text = self.process_whitespace(text)
        text = self.process_stopwords(text)
        text = self.process_stemming_lemmatize(text)
        return text
    
    
    def process_nums(self, text):
        p = inflect.engine()
        words = text.split()
        processed_words = []
        for word in words:
            if word.isdigit():
                word = p.number_to_words(word)
                processed_words.append(word)
            else:
                processed_words.append(word)
        return ' '.join(processed_words)
    
    def process_punctuations(self, text):
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)
    
    def process_whitespace(self, text):
        return ' '.join(text.split())
    
    def process_stopwords(self, text):
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        filtered_words = [word for word in words if word not in stop_words]
        return ' '.join(filtered_words)
    
    def process_stemming_lemmatize(self, text):
        #stemmer = PorterStemmer()
        words = word_tokenize(text)
        #stemmed_words = [stemmer.stem(word) for word in words]
        lemmatizer = WordNetLemmatizer()
        stemmed_words = [lemmatizer.lemmatize(word) for word in words]
        return ' '.join(stemmed_words)

    def write_file(self, text):
        with open(self.output_file, 'w') as file:
            file.write(text)

    def process(self):
        text = self.read_file()
        filtered_text = self.filter_text(text)
        self.write_file(filtered_text)
        return self.output_file
    


# Usage
input_file = '/Users/irfanfirosh/Library/Mobile Documents/.Trash/data/sampleTranscript.txt'
output_file = '/Users/irfanfirosh/Library/Mobile Documents/.Trash/data/cleaned_output.txt'
cleaner = TextCleaner(input_file, output_file)
cleaner.process()
