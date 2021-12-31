import os
import random
import re
import sys
from decimal import Decimal

DAMPING = 0.85  # represents the damping factor(d); set to initially to 0.85
SAMPLES = 10000 # represents the number of samples used to estimate PageRank using the sampling method; set initially to 10000


def main():
    """
    This function calls a helper function in `crawl`: parses all of the HTML files in the directory,
                                                        and returns a dictionary representing the corpus
    The function then calls for two functions (the output of these two functions should be similar when given the same corpus!):
        1. `sample_pagerank()`   :  Used to estimeate the PageRank of each page by sampling.
        2. `iterative_pagerank()`:  Used to calculate the PageRank of each page by using iterative formula method
        **  Output method of the above functions returns a dictionary where the keys are each page name and the values 
            are each page's estimated PageRank (a number between 0 and 1).
    
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
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

    Parameters:
        • The `corpus` is a Python dictionary mapping a page name to a set of all pages linked to by that page.
        • The `page` is a string representing which page the random surfer is currently on. e.g. "1.html"
        • The `damping_factor` is a floating point number representing the damping factor to be used when generating
            the probabilities.
    """
    probability = dict()
    # In case if the page has links to no other pages
    if corpus[page] is None:
        for current_page in corpus: # iterate over all the keys in the corpus dictionary
            probability[current_page] = 1 / len(corpus[page])
        return probability

    # Else if the page is pointing to other pages
    for current_page in corpus: # iterate over all the keys in the corpus dictionary

        # Every page will have some change which is given by: (1 - damping_factor) / len(corpus)
        # trying to overcome the issues aand limitations of floating-point arithmetic; by using integer arithmetic instead
        probability[current_page] = (100 - damping_factor * 100) / (len(corpus) * 100)

        # If curret_page is linked to the given page (`page`); then add it's chances of being the next one  
        if current_page in corpus[page]:
            # again to eradicate the floating-point arithmetic issue
            # could instead use: probability[current_page] += damping_factor / len(corpus[page])
            probability[current_page] = ((probability[current_page] * 100) + (damping_factor * 100) / len(corpus[page])) / 100
       
    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    Parameters:
        • The `corpus` is a Python dictionary mapping a page name to a set of all pages linked to by that page.
        • The `damping_factor` is a floating point number representing the damping factor to be used by the transition model.
        • `n` is an integer representing the number of samples that should be generated to estimate PageRank values. (n >= 1)
    """
    pagerank = {page: 0 for page in corpus} # dictionary to store the estimated pagerank of each page
    sample = random.choice(list(corpus.keys())) # first page

    for _ in range(n):
        pagerank[sample] += 1
        model = transition_model(corpus, sample, damping_factor)
        # random.choices() has an argument- `weight` which will infulence the outcome based on the value(higher get more chances)
        # random.choices returns list of length equal to the length of the given sequence; so we define k=1 to get only one item
        sample = random.choices(list(model.keys()), weights=list(model.values()), k=1)[0]   # We get a list of unit length so to get the item only use 0 index
    
    for page in pagerank:
        pagerank[page] /= n

    # Check: print(sum(pagerank.values()))
    return pagerank





def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
