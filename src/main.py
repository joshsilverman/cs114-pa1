import nltk    

class PivotedCorpus:
    
    '''wrapper class for PivotedSent'''
    
    def __init__(self, corpus):
        self.corpus = corpus
        self.sents = []
        
        # set sents
        sent_trees = self.corpus.parsed_sents()
        for sent_tree in sent_trees:
            self.sents.append(PivotedSent(sent_tree))

    def pprint(self):
        for sent in self.sents:
            print sent.tree, "\n\n"

class PivotedSent:
    
    '''wrapper class for nltk.tree.Tree's for sentences'''
    
    # weak verbs list
    weak_verbs = ['like', 'guess', 'thought', 'thinking', 'get', 'think', 'do', 'be', 'is', "'s", 'are', 'have', 'had', 'has', 'was', 'do', 'did', "'re", 'were', "'m", "seems", "doing"]
    
    def __init__(self, tree):
        
        # wrapped obj, pivot
        self.tree = tree
        self.pivot = False
        
        # members used for traversal - could be put in a utility class along with traverse mamber
        self.last_verb = False
        self.last_verb_path = False
        
        #set pivot
        self._set_pivot(self.tree)
            
    def _set_pivot(self, chunk, node_name = 'TREE', path = []):
        
        '''preorder traversal of tree'''
        
        # iterate through children, looking for verb strings
        for i, small_chunk in enumerate(chunk):
            
            # check if word and if verb
            if isinstance(small_chunk, str):
                
                # attempt to set strong pivot
                if node_name.startswith("V") or node_name == 'BES':
                    self.last_verb = chunk
                    self.last_verb_path = path
                    self._set_strong_pivot(small_chunk, node_name)
                    if self.pivot: break
                
            else:
                child_path = path + [i]
                self._set_pivot(small_chunk, small_chunk.node, child_path)
        
        # if strong pivot not found
        if path == [] and self.pivot == False:
            self._set_weak_pivot()
        

    def _set_strong_pivot(self, word, pos):
        
        # check if pivot already set and if weak
        if self.pivot: return False
        if PivotedSent.weak_verbs.count(word) > 0: return False
        self.last_verb = nltk.tree.Tree('PIVOT_STRONG_BEFORE', [self.last_verb])
        self.pivot = self.last_verb
        self.tree[tuple(self.last_verb_path)] = self.last_verb
        return True
    
    def _set_weak_pivot(self):
        
        if not self.last_verb: return False
        self.last_verb = nltk.tree.Tree('PIVOT_WEAK_AFTER', [self.last_verb])
        self.pivot = self.last_verb
        self.tree[tuple(self.last_verb_path)] = self.last_verb
        return True
            
# build corpus with pivots, print
reader = nltk.corpus.reader.BracketParseCorpusReader('../data', 'corpus.txt', detect_blocks='sexpr')
pivoted_corpus = PivotedCorpus(reader)
pivoted_corpus.pprint()