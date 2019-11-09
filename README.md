# RandomTalker
You can find plain text versions of many literary works at [Project Gutenberg](http://www.gutenberg.org) which is useful for training this program.

## Description:
In this PA we are attempting to create a random text generator. The program (talker) will learn an N-gram language model
from an arbitrary number of plain text files, and then use the generated model to generate the random sentences. An
N-gram is a probabilistic language model that is trying to predict the next item (in this case a word) based on n
previous words. Talker should be able to work for n values of 1, 2, and 3 (unigrams, bigrams, and trigrams). Talker
should be able to output a user specified number of sentences. Talker should also be able to take any number of text
files passed in by the user. We want talker to get all of this information from command line arguments. No matter the
number of text files we will treat them as a single corpus and learn one n-gram model. Furthermore, talker needs to be
able to identify sentence boundaries in this case we will assume !,., and ? are the only boundaries. The Ngrams should
not cross the sentence boundaries.

## Example Input and Output:
Talker is ran by running a command with the following syntax: `python3 talker.py n m text_file(s)` \
Where n is the ngram integer, m is the number of sentences to be outputted, and text_file(s) is one or more text files
in the current directory that will be used to create the ngram model. 

input: `python3 talker.py 2 10 theraven.txt caskofamontillado.txt fallofthehouseofusher.txt clarissa1.txt clarissa2.txt` 

output: \
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
  
## Algorithm:
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
