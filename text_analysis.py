# -*- coding: utf-8 -*-
"""
This program is a text content analyzer. It is used by writers to compute
statistics such as word or sentence counts on essays or articles. It can
accept a filename from the standard input or a file input at the command line.

The code below outputs
1. The total word count
2. The count of unique words
3. The number of sentences
4. Average sentence length in words
5. Freqently used phrases (a phrase of 3 or more words used over 3 times)
6. A frequency list of words used in descending order.
7. Accepts input from STDIN, or from a file specified on the command line.

Ricky Kwok, rickyk9487@gmail.com, 2014-10-08. """
import sys
import re
import collections

def word_count_dict(filename):
    """ Returns a (word,count) dictionary for filename. """
    word_dict = {}  
    f = open(filename, 'r')
    text = f.read()
    f.close() 
    sen_count = len(re.findall(r"[\.?!]", text))
    """ Counts sentences by assuming periods, question marks, and exclamation 
        marks end sentences. """
    # counts words separated by white space, hyphens 
    #words = re.findall(r"[\w\'\`]+", text) 
    # counts words separated by white space 
    #words = re.findall(r"[^\s]+", text)
    # counts words separated by white space, apostrophes
    pattern = re.compile("""
        (?:
            [a-zA-Z]+(?:['`-]+[a-zA-Z]+)*  # word
            |                              # or
            \d+(?:\.\d+)?                  # number
        )
    """, re.X)
    words = re.findall(pattern, text)
    words = [word.lower() for word in words]
    info = [0,len(words),sen_count] # unique words, total_words, total sentences
    phrases = {}

    for word in words:
        if word not in word_dict:
            word_dict[word] = 1
            info[0] += 1
        else:
            word_dict[word] += 1
            
    return word_dict, info, phrases, words
    
def print_words(filename):
    """ Prints statistics of the filename."""
    word_dict, info, phrases, words = word_count_dict(filename)
    uniques = info[0]
    total_count = info[1]
    sen_count = info[2]
    sen_avg = float(total_count)/sen_count
    phrase_length = 6 # Phrases consisting of words from 3 to 6 consecutively.

    print "1. The total word count: %d." %total_count
    print "2. The count of unique words: %d." %uniques
    print "3. The number of sentences: %d." %sen_count
    print "4. Average sentence length in words: %f." %sen_avg
    for k in range(3, phrase_length + 1):
        phrases = []
        print "\n5. TOP 5 COMMONLY USED PHRASES OF LENGTH %d: " %k
        phrases = get_phrases(words, k)
        print phrases[:5],

    n = 10 # the top n most frequently used words are printed
    print "\n6. List of %d most frequently used words in descending order:" %n
    sort_descending(word_dict, n)
    print " \n7. Requires file specified on the command line.",
    print "\n8. Usage: text_analysis.py <filename>."

def get_phrases(words, size):
    """ Finds often used phrases with a common phrase is  3 or more words used 
        over 3 times. """
        
    phrase_str = ""
    phrase_size = []
    common_phrases = []
    length = len(words) - size + 1
    phrase_list = [" "]*length
    for i in range(len(words)-size+1):
        phrase_size = words[i:i+size]
        phrase_str = " ".join(phrase_size)
        phrase_list[i] = phrase_str
    phrase_dict = collections.Counter(phrase_list)
    phrase_desc_freq = sorted(phrase_dict.items(), key=get_count, reverse=True)
    for (x,y) in phrase_desc_freq:
        if y > 2:
            common_phrases.append((x,y))
    return common_phrases

def sort_descending(word_dict, n):
    """ Prints the n most frequently used words in word_count
        Each item is a (word, count) tuple.
        Sort them so the big counts are first using key=get_count() to extract 
        count. """
    desc_freq = sorted(word_dict.items(), key=get_count, reverse=True)
    if n > len(word_dict):
        print "Choose a smaller n."
    else:
        for pair in desc_freq [:n]:
            print pair[0], pair[1], "|",

def get_count(word_count_tuple):
    """ Returns the count from dict word_count for custom sort. """
    return word_count_tuple[1]

def main():
    if len(sys.argv) != 2:
        print "Usage: text_analysis.py <filename>"
        sys.exit(1)
    elif sys.argv[1] == "" :
        print "must provide input file "
        sys.exit(1)
    else:
        filename = sys.argv[1]
        print_words(filename)

if __name__ == '__main__':
    main()
    