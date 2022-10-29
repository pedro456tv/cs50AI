import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    #if len(sys.argv) != 2:
        #sys.exit("Usage: python pagerank.py corpus")
    #corpus = crawl(sys.argv[1])
    corpus = crawl("corpus0")

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    rdic = dict()
    
    current = corpus[page]
    if(current):
        for link in corpus:
            rdic[link] = (1-damping_factor)/len(corpus)
            if(link in corpus[page]):
                rdic[link] += damping_factor/len(current)
    else:
        for link in corpus:
            rdic[link] = 1/len(corpus)

    return rdic
    
    raise NotImplementedError
    

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    distribution = dict()
    for page in corpus:
        distribution[page] = 0

    firstpage = random.choice(list(corpus.keys()))
    distribution[firstpage] += 1

    for i in range(n):    
        next = transition_model(corpus,firstpage,damping_factor)
        firstpage = random.choices(population = list(next.keys()), weights= list(next.values()),k=1)[0]
        distribution[firstpage] += 1
    
    for every in distribution:
        distribution[every] = distribution[every]/n

    return distribution
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    final = dict()
    n = len(corpus)
    for page in corpus:
        final[page] = 1/n
    
    change = True 

    while(change):
        change = False
        old = final.copy()

        for page in corpus:
            final[page] = ((1-damping_factor)/n) + damping_factor*(page_rank(page,corpus,final))

        for oldy in final:
            if(abs(old[oldy] - final[oldy]) > 0.001):
                change = True

    return final

def page_rank(page,corpus,final):

    result = 0
    for next_page in corpus:
        if(page in corpus[next_page]):
            result = result + final[next_page]/len(corpus[next_page])
        if not corpus[next_page]:
            result += final[next_page]/len(corpus)

    return result




if __name__ == "__main__":
    main()
