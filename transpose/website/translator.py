from nltk import CFG
from nltk import Tree
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk import ChartParser

from re import search, match, findall

from text2digits import text2digits
t2d = text2digits.Text2Digits()

math_word_grammar = CFG.fromstring("""

S -> O | L
L -> 'sum' LEADING | 'difference' LEADING | 'product' LEADING | 'quotient' LEADING
LEADING -> NV ',' LEADING | S ',' LEADING | NV 'and' NV | NV 'and' S | S 'and' NV | S 'and' S | 'and' NV | 'and' S
NV -> VAR | NUM
O -> NV EXACT NV | NV REVERSE NV | S EXACT S | S REVERSE S 
O -> S ',' EXACT S | S ',' REVERSE S | S ',' EXACT NV | S ',' REVERSE NV 
O -> NV EXACT S | NV REVERSE S
NUM -> '#NUM#'
VAR -> '#VAR#'
EXACT -> 'add' | 'minus' | 'times' | 'divide'
REVERSE -> 'more' | 'less'

""")

operator = {
    'EXACT':{
        'add': ['plus', 'add', 'increase'], 
        'minus':['subtract', 'minus', 'decrease', 'diminish', 'reduce', 'lost'],
        'times': ['time', 'times', 'multiply'],
        'divide': ['divide']
    },
    'LEADING':{
        'sum': ['sum','total','addition'],
        'difference': ['difference'],
        'product': ['multiplication', 'product'],
        'quotient': ['quotient'],
    },
    'REVERSE':{
        'more': ['greater', 'more'],
        'less': ['fewer', 'less'],
    },
    'MULTIPLIER':{
        '2 times': ['twice'],
        '3 times': ['thrice'],
    },
}
operator_sign = {
    'add': '+',
    'minus': '-',
    'times': '*',
    'divide': '/',
}
keyword = [word for i in operator.keys() for j in operator[i].keys() for word in operator[i][j]]
stopword = ["by", "to", "the", "than", "a", "of"]


# In[4]:


def _preprocess(sentence):
    #simplification
    
    sentence = sentence.lower()
    sentence = sentence.replace('.', '')

    #Tokenization, POS Tagging
    token = word_tokenize(sentence)
    pos = pos_tag(token)
    
    #Lemmatization
    sentence = [WordNetLemmatizer().lemmatize(word, 'v') for word in token]

    temp = []
    #Stopword filtering
    for i in sentence:
        if i not in stopword:
            temp.append(i)
    sentence = ' '.join(temp)
    
    #keyword standardization
    for i in operator.keys():
        for j in operator[i].keys():
            for k in operator[i][j]:
                if(str(k) in sentence):
                    sentence = sentence.replace(k, j)
    sentence = " ".join(sentence.split())
    return sentence


# In[5]:


#for clearing unneccary nested list
def _semi_flattener(tree_list):
    if type(tree_list) is not list:
        return tree_list
    
    elif len(tree_list) > 1: 
        for i in range(len(tree_list)):
            if type(tree_list[i]) == list and len(tree_list[i]) > 0:
                tree_list[i] = _semi_flattener(tree_list[i])
                
    elif (len(tree_list)) == 1:
        tree_list = _semi_flattener(tree_list[0])
        
    return tree_list


# In[6]:


lead_op_sign = {
    'sum': '+',
    'difference': '-',
    'product': '*',
    'quotient': '/',
}
def _word_math_tree_to_list(tree, lead_op = None):
    output = []
    
    #encloses all starts
    if tree.label() in ('S'):
        in_list = []
        in_list.append(_word_math_tree_to_list(tree[0]))
        output.append(in_list)
    
    #combines all words from L to LEADING SEQUENCE, 
    elif tree.label() in ('L'):
        temp = _word_math_tree_to_list(tree[1], lead_op = tree[0])
        
        #small code to put OPERATOR word between VAR/NUM, in a LEADING sequence
        result = [lead_op_sign[tree[0]]] * (len(temp) * 2 - 1)
        result[0::2] = temp
            
        return result
    
    #gets all LEADING words
    elif tree.label() in ('LEADING'):
        for i in tree:
            if type(i) is str:
                continue
                
            elif i.label() in ('NV'):
                output.append(i.leaves()[0])
                
            #recursion, traverses S 
            #goes back to L
            elif i.label() in ('S'):
                output.append(_word_math_tree_to_list(i, lead_op))
            
            #recursion, traverses LEADING 
            #goes back to L
            elif i.label() in ('LEADING'):
                temp = _word_math_tree_to_list(i, lead_op)
                for x in temp:
                    output.append(x)
    
    #for add minus etc...
    elif tree.label() in ('O'):
        in_list = []
        for i in tree:
            if type(i) is str:
                continue
            
            #recursion, gets all NUM VAR add minus etc... from O
            #goes back to S
            elif i.label() in ('NV', 'EXACT', 'REVERSE'):
                in_list.append(i.leaves()[0])
                
            #recursion, traverses S 
            #goes back to S
            elif i.label() in ('S'):
                in_list.append(_word_math_tree_to_list(i))
        output.append(in_list)
    
    return output


# In[7]:


def _simplification(pos):
    temp = []
    #unknown nouns to variables
    variable = ['x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v']
    for word, pos in pos:
        #one -> 1, two -> 2
        if pos in ('CD') or word in keyword+['and', ',']:
            
            # if word is 2x, 2y, 4z, etc....
            if match("^[0-9]+[a-z]$", word):
                temp.append(search("[0-9]+", word).group())
                temp.append("times")
                v = search("[a-z]", word).group()
                variable.remove(v)
                temp.append(v)
                temp.append(',')
                continue

            temp.append(word)
            continue
        
        # if it gets here
        # it means word is unknown, and will be turned into a variable
        temp.append(variable[0])
        variable.remove(variable[0])
    return temp

# In[8]:


# ['2y', 'add', ['2', 'product', '4', 'product', '8', 'product', ['2', 'times', 'x']]]
def _mid_operator_convert(s):
    for i in range(len(s)):
        if type(s[i]) is list:
            s[i] = _mid_operator_convert(s[i])
            continue
        #swap i-1 and i+1 then change to EXACT
        if s[i] in operator['REVERSE'].keys():
            if type(s[i+1]) is list:
                s[i+1] = _mid_operator_convert(s[i+1])
            s[i-1], s[i+1] = s[i+1], s[i-1]
            s[i] = 'add' if s[i] == 'more' else 'minus'
        #keyword to signs
        if s[i] in operator['EXACT'].keys():
            s[i] = operator_sign[s[i]]
    return s
    


# In[9]:


def translation(sentence):
    #preprocessing
    sentence = _preprocess(sentence)
    
    #number word conversion
    sentence = t2d.convert(sentence)
    
    ##
    token = word_tokenize(sentence)
    pos = pos_tag(token)
    
    #simplication, variables conversion
    token = _simplification(pos)
    
    #keywords translation
    #get word from pos_transform as token

    # for recognizing constants and variables
    # recreates the original sentence with #VAR# #NUM# replacements
    mod_token = ['#NUM#' if i.isdigit() else i for i in token]
    mod_token = ['#VAR#' if match("^[a-z]$", i) else i for i in mod_token]
    numbers = [i for i in token if i.isdigit()]
    vars = [i for i in token if match("^[a-z]$", i)]

    #converting the token to TREE object
    trees = []
    parser = ChartParser(math_word_grammar)

    for tree in parser.parse(mod_token):
        treestr = str(tree)
        for n in numbers:
            treestr = treestr.replace('#NUM#', str(n), 1)
        for l in vars:
            treestr = treestr.replace('#VAR#', l, 1)
        trees.append(Tree.fromstring(treestr))
        
    
    all_sent = []
    
    if len(trees) == 0:
        return "Input Error: Structure Unidentified"
    for tree in trees:
        temp = _word_math_tree_to_list(tree)
        all_sent.append(_semi_flattener(temp))

    for i in range(len(all_sent)):
        all_sent[i] = _mid_operator_convert(all_sent[i])
    
    #output processing
    if all(all_sent) and type(all_sent[0]) == list and len(all_sent) > 1:
        for i in range(len(all_sent)):
            all_sent[i] = _parenthesis_adder(all_sent[i])
            all_sent[i] = (' '.join(_flatten(all_sent[i])))
        return _semi_flattener(all_sent)
            
    else:
        all_sent[0] = _parenthesis_adder(all_sent[0])
        return(' '.join(_flatten(all_sent[0])))

#output processing
def _flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return _flatten(S[0]) + _flatten(S[1:])
    return S[:1] + _flatten(S[1:])
def _parenthesis_adder(l):
    for i in range(len(l)):
        if type(l[i]) is list:
            if(l[i][0] != '('):
                l[i].insert(0, '(')
                l[i].append(')')
                l[i] = _parenthesis_adder(l[i])
    return l

#making output more readable
#only use on one branch, 
    #if the translation is ambiguous, use this iteratively
def prettier(trans):
    """( 2 * y ) + ( 2 * 4 * 8 * ( 2 * x ) )"""
    txt = trans
    txt = txt.replace("( ", "(")
    txt = txt.replace(" )", ")")
    x = findall("[0-9]+ \* [a-z]", txt)
    if x:
        x = list(set(x))
        y = [i.replace(" * ", "") for i in x]
        for i, j in zip(x, y):
            txt = txt.replace(i, j)

    x = findall("\([0-9]+[a-z]\)", txt)

    if x:
        x = list(set(x))
        y = [i.strip("()") for i in x]
        for i, j in zip(x, y):
            txt = txt.replace(i, j)

    if txt != trans:
        return txt
    else:
        return trans