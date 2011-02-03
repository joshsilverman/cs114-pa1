import nltk
    
verbs = ['raised', 'figure', 'be', 'doing', 'is', 'talking', 'see', 'decided', 'are', 'have', 'go', 'seen', 'seem', 'dress', 'thought', 'guess', 'thinking', 'make', 'give', 'had', 'combine', 'has', 'was', 'do', 'play', 'get', 'hang', 'grew', 'lives', "'m", 'trying', 'gets', 'figured', 'like', 'getting', 'did', 'try', "'re", 'were', 'hear', 'went', 'makes', 'think', 'mean']
weak_verbs = ['be', 'is', 'are', 'have' 'had', 'has', 'was', 'do', 'get', 'gets', 'getting', 'did', "'re", 'were', 'went', 'makes', "'m"]
    
def pivot_on_first_strong(tree):
    traverse_tree(tree, tree, is_pivot)
        
def traverse_tree(tree, chunk, leaf_function, node_name = 'TREE', path = [0]):
    for i, small_chunk in enumerate(chunk):
        if isinstance(small_chunk, str):
            leaf_function(small_chunk, node_name, path)
        else:
            child_path = path + [i]
            traverse_tree(tree, small_chunk, leaf_function, small_chunk.node, child_path)
            
def is_pivot(word, pos, path):    
    if not pos.startswith("V"): return False
    elif weak_verbs.count(word) > 0: return False
    print '"%s", ' % word,
        
# read corpus, parse sentences, add pivots
reader = nltk.corpus.reader.BracketParseCorpusReader('../data', 'corpus.txt', detect_blocks='sexpr')
tree = reader.parsed_sents()
tree = pivot_on_first_strong(tree)