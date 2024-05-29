import os
import nltk
from nltk.corpus import wordnet as wn
from textblob import TextBlob

# Function to get sentiment from email content
def get_email_sentiment(email_content):
    # You might want to customize this function based on how you want to analyze the sentiment of email content
    blob = TextBlob(email_content)
    return blob.sentiment.polarity

# Function to get synonyms of a word
def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

# Function to analyze sentiments of files
def analyze_file_sentiments(files):
    sentiments = {}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            sentiments[file] = get_email_sentiment(content)
    return sentiments

# Function to search files based on query
def search_files(files, query):
    query_sentiment = get_email_sentiment(query)
    print(f"Search Query Sentiment: {query_sentiment}")

    words = nltk.word_tokenize(query)
    synonyms = {word: get_synonyms(word) for word in words}

    print(f"Query Synonyms: {synonyms}")

    results = {}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            content_sentiment = get_email_sentiment(content)
            matches = [word for word in words if word in content]
            for word, syns in synonyms.items():
                if any(syn in content for syn in syns):
                    matches.append(word)
            if matches:
                results[file] = {'matches': matches, 'sentiment': content_sentiment}
    return results

# Main function
def main():
    # Gather all text files in the current directory
    text_files = [f for f in os.listdir('.') if f.endswith('.txt')]
    
    # Display initial sentiment analysis of each file
    sentiments = analyze_file_sentiments(text_files)
    for file, sentiment in sentiments.items():
        print(f"File: {file}, Sentiment: {sentiment}")
    
    # Prompt for search query
    query = input("Enter your search query: ")
    
    # Search files based on query and synonyms
    results = search_files(text_files, query)
    
    # Display results
    for file, data in results.items():
        print(f"File: {file}")
        print(f"  Matches: {data['matches']}")
        print(f"  Sentiment: {data['sentiment']}")
        
if __name__ == "__main__":
    main()
