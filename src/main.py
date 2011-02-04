import nltk    

class Corpus:
    
    '''wrapper class for list of sentence trees'''
    
    def __init__(self, path):
        self.sents = []
        
        # set sents
        corpus_text_handle = open(path, 'r')        
        corpus_text = corpus_text_handle.read()
        corpus_lines = corpus_text.split('\n')
        for line in corpus_lines:
            tree = nltk.tree.Tree(line)
            self.sents.append(Sent(tree))

    def pprint(self):
        
        for sent in self.sents:
            sent.pprint()

class Sent:
    
    '''wrapper class for nltk.tree.Tree's for sentences'''
    
    def __init__(self, tree):
        
        '''constructor'''
        
        # wrapped obj
        self.tree = tree
        
        # members used for traversal - could be put in a utility class along with traverse mamber
        self.last_verb = False
        self.last_verb_path = False
        
        # pivot
        self.pivot = False
        
        # weak verbs list
        self.weak_verbs = ['do', 'be', 'is', 'are', 'have' 'had', 'has', 'was', 'get', 'gets', 'getting', 'did', "'re", 'were', 'makes', "'m"]
        
        #set pivot
        self._set_pivot(self.tree)
        
    def pprint(self):
        
        '''print wrapped tree object'''
        
        print self.tree, "\n\n"
            
    def _set_pivot(self, chunk, node_name = 'TREE', path = []):
        
        '''post order traversal of tree'''
        
        # iterate through children, looking for verb strings
        for i, small_chunk in enumerate(chunk):
            
            # check if word and if verb
            if isinstance(small_chunk, str):
                
                # attempt to set strong pivot
                if node_name.startswith("V"):
                    self.last_verb = chunk
                    self.last_verb_path = path
                    self._set_strong_pivot(small_chunk, node_name)
                
            else:
                child_path = path + [i]
                self._set_pivot(small_chunk, small_chunk.node, child_path)
        
        # if strong pivot not found
        if path == [] and self.pivot == False:
            self._set_weak_pivot()
        

    def _set_strong_pivot(self, word, pos):
        
        '''set strong pivot'''
        
        if self.weak_verbs.count(word) > 0: return False
        self.last_verb = nltk.tree.Tree('(PIVOT_STRONG %s)' % self.last_verb)
        self.pivot = self.last_verb
        
        # this is ugly!!!!! how do i access leaf with list of indices????????
        pathString = ''.join(["[%i]" % index for index in self.last_verb_path])
        exec("self.tree%s = self.last_verb" % pathString)
        return True
    
    def _set_weak_pivot(self):
        
        '''set weak pivot'''
        
        if not self.last_verb: return False
        self.last_verb = nltk.tree.Tree('(PIVOT_WEAK %s)' % self.last_verb)
        self.pivot = self.last_verb
        
        # sooooooooooooooooooooooooooooooo ugly
        pathString = ''.join(["[%i]" % index for index in self.last_verb_path])
        exec("self.tree%s = self.last_verb" % pathString)
        return True
            
# build corpus with pivots, print
corpus = Corpus('../data/corpus.txt')
corpus.pprint()