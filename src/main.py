import nltk

reader = nltk.corpus.reader.BracketParseCorpusReader('../data', 'corpus.txt', detect_blocks='sexpr')

tree = reader.parsed_sents()

print tree

def print_tree(children):
    print children
    return children

nltk.util.breadth_first(tree)