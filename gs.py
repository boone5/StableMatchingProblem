# Hunter Boone & Mac McDaniel
# Python implementation of stable matching problem
# Homework 1 Starter Code
# CS 2123 last modified 8/31/16

def gs(men, women, pref):
    """
    Gale-shapley algorithm, modified to exclude unacceptable matches
    Inputs: men (list of men's names) 
            women (list of women's names)
            pref (dictionary of preferences mapping names to list of preferred names in sorted order)
            blocked (list of (man,woman) tuples that are unacceptable matches)
    Output: dictionary of stable matches
    """
    # preprocessing
    ## build the rank dictionary
    rank = {}
    for w in women:
        rank[w] = {}
        i = 1
        for m in pref[w]:
            rank[w][m]=i
            i+=1
    #print(rank)

    ## create a "pointer" to the next woman to propose
    prefptr = {}
    for m in men:
        prefptr[m] = 0
    #print(prefptr)

    freemen = set(men)    #initially all men and women are free
    numpartners = len(men) 
    S = {}           #build dictionary to store engagements

    #run the algorithm
    while freemen:
        m = freemen.pop()
        #get the highest ranked woman that has not yet been proposed to
        w = pref[m][prefptr[m]]
        prefptr[m]+=1
        if w not in S: S[w] = m
        else:
            mprime = S[w]
            if rank[w][m] < rank[w][mprime]:
                S[w] = m
                freemen.add(mprime)
            else:
                freemen.add(m)
    return S

def gs_block(men, women, pref, blocked):
    """
    Gale-shapley algorithm, modified to exclude unacceptable matches
    Inputs: men (list of men's names)
            women (list of women's names)
            pref (dictionary of preferences mapping names to list of preferred names in sorted order)
            blocked (list of (man,woman) tuples that are unacceptable matches)
    Output: dictionary of stable matches
    """

    rank = {}
    for w in women:
        rank[w] = {}
        i = 1
        for m in pref[w]:
            rank[w][m] = i
            i += 1
    #print(rank)

    prefpointer = {}
    for m in men:
        prefpointer[m] = 0

    freemen = set(men)
    numPartners = len(men)
    
    Start = {}
    Finished = {}
    listBlocked = list(blocked)
    #print(listBlocked)

    while(freemen):
        m = freemen.pop()
        w = pref[m][prefpointer[m]]
        #print(m + ' ' + w)
        prefpointer[m] += 1
        if (m,w) not in listBlocked and w not in Start:
            Start[w] = m
        elif (m,w) not in listBlocked and not Finished:
            mprime = Start[w]
            if rank[w][m] < rank[w][mprime]:
                Start[w] = m
                freemen.add(mprime)
            else:
                freemen.add(m)
        else:     #blocked couple
            freemen.add(m)
        if prefpointer[m] == numPartners and w not in Start:
            prefpointer[m] = 0
            while prefpointer[m] < numPartners:
                w = pref[m][prefpointer[m]]
                if (m,w) not in listBlocked:
                    mprime = Start[w]
                    Start[w] = m
                    Finished[w] = m
                    freemen.pop()
                    freemen.add(mprime)
                prefpointer[m] += 1
    return Start

def gs_tie(men, women, preftie):
    """
    Gale-shapley algorithm, modified to exclude unacceptable matches
    Inputs: men (list of men's names)
            women (list of women's names)
            pref (dictionary of preferences mapping names to list of sets of preferred names in sorted order)
    Output: dictionary of stable matches
    """

    rank = {}
    for w in women:
        rank[w] = {}
        i = 1
        for m in preftie[w]:
            rank[w][tuple(m)] = i
            i += 1
    #print(rank)

    prefpointer = {}
    for m in men:
        prefpointer[m] = 0

    freemen = set(men)
    S = {}

    while(freemen) and prefpointer[m] < len(preftie[m]):
        m = freemen.pop()
        w = preftie[m][prefpointer[m]]
        w = tuple(w)
        #print(m + ' ' + str(w))
        prefpointer[m] += 1
        #print(m + ' ' + str(prefpointer[m]))
        for i in range(len(w)):
            if w[i] not in S:
                S[w[i]] = m
                #print(w[i])
            else: 
                mprime = S[w[i]]
                if m in rank[w[i]] and rank[w[i]][m] < rank[w[i]][mprime]:
                    S[w[i]] = m
                    freemen.add(mprime)
                else:
                    freemen.add(m)
        #print(S)
    return S

if __name__=="__main__":
    #input data
    themen = ['xavier','yancey','zeus']
    thewomen = ['amy','bertha','clare']

    thepref = {'xavier': ['amy','bertha','clare'],
           'yancey': ['bertha','amy','clare'],
           'zeus': ['amy','bertha','clare'],
           'amy': ['yancey','xavier','zeus'],
           'bertha': ['xavier','yancey','zeus'],
           'clare': ['xavier','yancey','zeus']
           }
    thepreftie = {'xavier': [{'bertha'},{'amy'},{'clare'}],
           'yancey': [{'amy','bertha'},{'clare'}],
           'zeus': [{'amy'},{'bertha','clare'}],
           'amy': [{'zeus','xavier','yancey'}],
           'bertha': [{'zeus'},{'xavier'},{'yancey'},],
           'clare': [{'xavier','yancey'},{'zeus'}]
           }
    
    blocked = {('xavier','clare'),('zeus','clare'),('zeus','amy')}

    #eng
    match = gs(themen,thewomen,thepref)
    print(match)
    
    match_block = gs_block(themen,thewomen,thepref,blocked)
    print(match_block)

    match_tie = gs_tie(themen,thewomen,thepreftie)
    print(match_tie)