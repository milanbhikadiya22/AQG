
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import urllib2
from bs4 import BeautifulSoup

class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):
    """
     Initilize the text summarizer.
     Words that have a frequency term lower than min_cut 
     or higer than max_cut will be ignored.
    """
    self._min_cut = min_cut
    self._max_cut = max_cut 
    self._stopwords = set(stopwords.words('english') + list(punctuation))

  def _compute_frequencies(self, word_sent):
    """ 
      Compute the frequency of each of word.
      Input: 
       word_sent, a list of sentences already tokenized.
      Output: 
       freq, a dictionary where freq[w] is the frequency of w.
    """
    freq = defaultdict(int)
    for s in word_sent:
      for word in s:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    for w in freq.keys():
      freq[w] = freq[w]/m
      if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
        del freq[w]
    return freq

  def summarize(self, text, n):
    """
      Return a list of n sentences 
      which represent the summary of text.
    """
    sents = sent_tokenize(text)
    assert n <= len(sents)
    word_sent = [word_tokenize(s.lower()) for s in sents]
    self._freq = self._compute_frequencies(word_sent)
    ranking = defaultdict(int)
    for i,sent in enumerate(word_sent):
      for w in sent:
        if w in self._freq:
          ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, n)    
    return [sents[j] for j in sents_idx]

  def _rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get)
    
    
    


def get_only_text(url):
 """ 
  return the title and the text of the article
  at the specified url
 """
 #page = urllib2.urlopen(url).read().decode('utf8')
 #soup = BeautifulSoup(page)
 #text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
 #return soup.title.text, text
    
#feed_xml = urllib2.urlopen('http://feeds.bbci.co.uk/news/rss.xml').read()
#feed = BeautifulSoup(feed_xml.decode('utf8'))
#to_summarize = map(lambda p: p.text, feed.find_all('guid'))

fs = FrequencySummarizer()
#for article_url in to_summarize[:5]:
text = "Python is a powerful high-level, object-oriented programming language created by Guido van Rossum." \
       " It has simple easy-to-use syntax, " \
       "making it the perfect language for someone trying to learn computer programming for the first time." \
       "This is a comprehensive guide on how to get started in Python, why you should learn " \
       "it and how you can learn it." \
       "Inheritance is a feature of object-oriented programming. " \
       "It specifies that one object acquires all the properties and behaviors of parent object. " \
       "By using inheritance you can define a new class with a little or no changes to the existing class. " \
       "The new class is known as derived class or child class and from which " \
       "it inherits the properties is called base class or parent class." \
       "It provides re-usability of the code. "

  #~ print '----------------------------------'
  #~ print title
for s in fs.summarize(text, 2):
   print '*',s
