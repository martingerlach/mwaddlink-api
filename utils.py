import urllib
import urllib.parse as up
import numpy as np

######################
## parsing titles
def normalise_title(title):
    """ 
    Normalising title (links)
    - deal with quotes
    - strip()
    - '_'--> ' '
    - capitalize first letter
    """
    title = up.unquote(title)
    title = title.strip()
    if len(title) > 0:
        title = title[0].upper() + title[1:]
    n_title = title.replace("_", " ")
    if '#' in n_title:
        n_title = n_title.split('#')[0]
    return n_title

def normalise_anchor(anchor):
    '''
    Normalising anchor  (text):
    - strip()
    - lowercase
    Note that we do not do the other normalisations since we want to match the strings from the text
    '''
    # anchor = up.unquote(anchor)
    n_anchor = anchor.strip()#.replace("_", " ")
    return n_anchor.lower()


def wtpGetLinkAnchor(wikilink):
    '''
    extract anchor and link from a wikilink from wikitextparser.
    normalise title and anchor
    '''
    ## normalise the article title (quote, first letter capital) 
    link_tmp = wikilink.title
    link = normalise_title(link_tmp)
    ## normalise the anchor text (strip and lowercase) 
    anchor_tmp = wikilink.text if wikilink.text else link_tmp
    anchor = normalise_anchor(anchor_tmp)
    return link, anchor

##########################
## getting feature-dataset
##########################
from scipy.stats import kurtosis
from Levenshtein import distance as levenshtein_distance
from Levenshtein import jaro as levenshtein_score

def getDistEmb(ent_a, ent_b, embd):
    dst = 0
    try:
        a = embd[ent_a]
        b = embd[ent_b]
        dst = (np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b))
    except:
        pass
    if np.isnan(dst):
        dst=0
    return dst

# Return the features for each link candidate in the context of the text and the page
def get_feature_set(page, text, link, anchors, word2vec, nav2vec):
    ngram = len(text.split()) # simple space based tokenizer to compute n-grams
    freq = anchors[text][link] # How many times was the link use with this text 
    ambig = len(anchors[text]) # home many different links where used with this text
    kur = kurtosis(sorted(list(anchors[text].values()), reverse = True) + [1] * (1000 - ambig)) # Skew of usage text/link distribution
    w2v = getDistEmb(page, link,word2vec) # W2V Distance between the source and target page
    nav = getDistEmb(page, link, nav2vec) # Nav Distance between the source and target page
    leven = levenshtein_score(text.lower(),link.lower())
    return (ngram, freq, ambig, kur, w2v, nav, leven)