import ads
 
def get_papers_by_authors(authors_list):
    """
    get_papers_by_authors, function

    Given a list of author names, return a pandas dataframe
    with the list of papers retrieved by the ADSABS service.

    Parameters
    ----------
    authors_list: list or string
        A list containing the names of the authors.

    Returns
    -------
    byauth: dataframe
       A data frame containing the list of authors, number of papers
       and the list of papers as "Article" instances.
    """
 
    fl = ['id', 'bibcode', 'title', 'citation_count',
          'aff', 'author', 'citation', 'pub', 'reference',
          'metrics', 'year', 'read_count', 'pubdate']

    authors = []
    for auth in authors_list:
        print(auth)
        papers = list(ads.SearchQuery(author=auth, rows=500, fl=fl))
        authors.append(papers)

    byauth = pd.DataFrame()
    byauth['authors'] = authors_list
    byauth['ppr_list'] = authors
 
    # cantidad de papers por autor:
    npprs = []
    for p in authors:
        npprs.append(len(p))
    byauth['n_papers'] = npprs

    return byauth
             

def get_papers_by_institution(inst_names):
    """
    get_papers_by_institution, function

    Given a list of institution names, return a pandas dataframe
    with the list of papers retrieved by the ADSABS service.

    Parameters
    ----------
    inst_names: list or string
        A list containing the alternative names for an institution.

    Returns
    -------
    byauth: dataframe
       A data frame containing the list of papers as "Article" instances.
    """
 
    papers = list(ads.SearchQuery(aff="IATE"))
    for p in papers:
        print(p.author)
        print(f"Paper from year {p.year} with "
              f"{len(p.author)} authors and "
              f"{p.citation_count} citations.")
        input() 
                         
 
def staff_institute(article, institution_keys):
    """
    staff_iate, function

    Given a paper (python ads class Article), check if there is at
    least one author which is a member of an institution

    Parameters
    ----------
    article: a class Article object (not a list).
        An object with all the information for an article.

    institution_keys: list of strings
        Keywords that the affilliation can contain for a given
        institution.
        Fro example, for the IATE:
        institution_keys = ['IATE', 'Experimental', 'Córdoba', 
                            'Laprida', '854', 'X5000BGR',
                            'Universidad Nacional de Córdoba',
                            'Instituto de Astronomía Teórica y Experimental']          
    Returns
    -------
    isiate: logical
       If True, there is at least one author which is a member of an
       institution.
    """
 
    isinst = False
    for aff in article.aff:
        thisis = any(word in aff for word in institution_keys)
        isinst = isinst or thisis

    return isinst
