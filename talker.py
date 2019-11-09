"""
Author: Grant Mitchell
Date: 10/4/19
PA #2 NLP

In this PA we are attempting to create a random text generator. The program (talker) will learn an N-gram language model
from an arbitrary number of plain text files, and then use the generated model to generate the random sentences. An
N-gram is a probabilistic language model that is trying to predict the next item (in this case a word) based on n
previous words. Talker should be able to work for n values of 1, 2, and 3 (unigrams, bigrams, and trigrams). Talker
should be able to output a user specified number of sentences. Talker should also be able to take any number of text
files passed in by the user. We want talker to get all of this information from command line arguments. No matter the
number of text files we will treat them as a single corpus and learn one n-gram model. Furthermore, talker needs to be
able to identify sentence boundaries in this case we will assume !,., and ? are the only boundaries. The Ngrams should
not cross the sentence boundaries.

Talker is ran by running a command with the following syntax: python3 talker.py n m text_file(s)
where n is the ngram integer, m is the number of sentences to be outputted, and text_file(s) is one or more text files
in the current directory that will be used to create the ngram model.

Here is an example input and it's corresponding output:

input: python3 talker.py 2 10 theraven.txt caskofamontillado.txt fallofthehouseofusher.txt clarissa1.txt clarissa2.txt 

output:
This program generates random sentences based on an Ngram model. CS 4242 by Grant Mitchell.

Command line settings : talker 2 10

1.  heard i was now, belford thing before you making herself an, there need letter from clarissa, who, he should pursue 
    when you advise though by surprise be made >>> sight, all so dearly loved giddy fellows.
2.  by day?
3.  a chairman : a poor hand say, if that i could ]: and i only his displeasure of mr.
4.  the good-for-little magnates horns.
5.  and it might in what relates of your goodness, or for to have her proposed, set wretch, as, that i what i have write.
6.  then accounts, that period, .
7.  with such a out of regard a thousand witnesses longing to hear to raise his never will!
8.  pinion over fabric that i may comfort!
9.  never was there in the dining-room begs he will six words--a religious.
10.  your third article but nevertheless, the person ; , all of, which conceals that it had that at hampstead did i owe 
    and young tumbled of your fine i, (urging shall at least to be proud pausing--and rising from.


Algorithm:
- Grab all of the command line variables and assign them to variables
- Process all of the passed in text files
    - Make all of the text lower case
    - Put a space between all numeric, alphabetic chars, and punctuation so they are all counted as distinct tokens
    - Add each text processed text file to a single corpus so it can be used as if it was one file
- Take the processed corpus and turn it into a list of tokens by splitting on whitespace
- Check to makes sure there is at least 1,000,000 tokens
- Create the Ngram model base off of the list of tokens
    - For each token grab it and the next n token and add them to a sublist of the ngram_model list
    - Do this for all tokens excepts the last n in the list
- Process the Ngram model
    - Turn all of the elements in each sublist into one element by joining them with a space in between
- Generate the random sentences based off of the ngram model
    - Randomly pick a sublist from ngram model and append them into a sentence until you encounter a sentence boundary
    - Process the sentence
        - Remove the space between a punctuation mark and the alphanumeric preceding it
        - Remove any portion of an incomplete sentence at the end of the sentence
    - Print the sentence
"""

import re
import sys
import random


# This method takes in all of the plain text files and does some initial processing to it
def process_text(file_name):
    # We open the text file and refer to is as "file"
    with open(file_name, "r", encoding="utf8") as file:
        text = file.read()  # Reads the files into a String text

        text = text.lower()  # Will make every line lowercase in the file
        # A space is put between a alphanumeric followed by punctuation. We do this to make them distinct tokens
        text = re.sub(r'([a-zA-Z0-9])([,.!\[\]%{}?#&*@":;])', r'\1 \2', text)
        # A space is put between a punctuation followed by an alphanumeric. We do this to make them distinct tokens
        text = re.sub(r'([,.!\[\]%{}#&*@":;])([a-zA-Z0-9])', r'\1 \2', text)
        # A space is put between a numeric followed by a letter. Which will make both distinct tokens
        text = re.sub(r'([0-9])([a-zA-Z])', r'\1 \2', text)
        # A space is put between a letter followed by a numeric. Which will make both distinct tokens
        text = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', text)

    return text  # return the processed text


# Creates a ngram model dictated by the integer passed in as n and trains the model on the list of token passed in
def create_ngram_model(n, tokens):
    ngram_result = []  # New list to hold the ngram

    # For every token in the list we will grab the token plus the next n tokens and then append that gram to the model
    # We can grab the next n tokens because it is essentially the same thing as grabbing the previous n tokens. They
    # both will yield the same result. We stop at len(tokens)-n because anything past that won't have n tokens ahead of
    # it.
    for j in range(len(tokens)-n):
        ngram_result.append(tokens[j:j+n+1])

    return ngram_result


# This function processes the model that was just created. The model will be a list of lists that looks something like
# [["x", "y", "z"],...] but we want it to look like [["x y z"],...] so this method does that for us.
def process_model(model):
    processed_model = []  # New list to hold the processed gram

    # For every sublist in the list model we will join each element with a space in between
    for gram in model:
        processed_model.append(' '.join(gram))
    return processed_model


# This method will take the # of sentences to generate and a model to generate off of.
def generate_random_sentences(number_of_sentences, model):
    # Do this for as many sentences are required by number_of_sentences
    for y in range(number_of_sentences):
        sentence = ""

        # This while loop will randomly grab a sublist from the list model until a sentence boundary is encountered
        while not re.search(r'[!.?]', sentence):
            sentence += " " + model[random.randint(0, len(model)-1)]

        # We print the finished sentence with a numerical value stating which sentence it is after some processing on
        # the sentence
        print(str(y+1) + ". " + process_random_sentences(sentence))


# Used to process the random sentence to make it look a little bit more like a real sentence
def process_random_sentences(sentence):
    # This regex will find all punctuation following an alphanumeric and remove the space in between them
    # Example my cat .  -> my cat.
    sentence = re.sub(r'([a-z0-9]+) ([,.!?])', r'\1\2', sentence)

    # These will be used as the starting index of the possible sentence boundaries
    period = 0
    exclamation = 0
    question = 0

    # For each sentence boundary if it is present in the sentence we get the index of it's last occurrence
    if '.' in sentence:
        period = sentence.rindex('.')
    if '!' in sentence:
        exclamation = sentence.rindex('!')
    if '?' in sentence:
        question = sentence.rindex('?')

    # Out of all of the sentence boundaries which ever one has the very last occurrence we take the substring of the
    # sentence all they way to that index+1. We do this so that if the last gram is "a b c. x y" we don't have an
    # incomplete sentence at the end. So it would turn into "a b c."
    if period > (exclamation and question):
        sentence = sentence[:period+1]
    elif exclamation > (question and period):
        sentence = sentence[:exclamation+1]
    elif question > (exclamation and period):
        sentence = sentence[:question+1]

    return sentence


if __name__ == "__main__":

    arg_len = len(sys.argv)  # Get the number of command line arguments
    ngram = int(sys.argv[1])  # An integer that represents the n gram number
    m = int(sys.argv[2])  # An integer that is the number of random sentences to be generated
    corpus = ""  # Our corpus that we will create the ngram model with

    print("This program generates random sentences based on an Ngram model. CS 4242 by Grant Mitchell."
          "\nCommand line settings : talker " + str(ngram) + " " + str(m) + "\n")

    # Iterate through all of the file names passed through and process them and then append them to the corpus
    for i in range(3, arg_len):
        # Adds the processed text file to the pre-existing corpus. A space is added
        # to ensure the last token of the existing corpus is separate from the first toke of the appended text
        corpus += " " + process_text(sys.argv[i])

    # Take our finished corpus and turns it into a list of tokens. This will split on whitespace.
    token_list = corpus.split()

    # A check to make sure the corpus is at least a million tokens
    if len(token_list) < 1000000:
        print("The corpus is less than a million tokens!\n")

    # Create our ngram model and do a little bit of processing to it first
    ngram_model = process_model(create_ngram_model(ngram, token_list))

    # Using our ngram model and the number of sentences we will generate m number of random sentences
    generate_random_sentences(m, ngram_model)
