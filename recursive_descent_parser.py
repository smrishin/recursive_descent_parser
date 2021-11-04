'''
This program implements a recursive descent parser for the CFG below:

The grammar has added pi and unary minus to the previous program.
Also, the parse function is now called in a loop, so you can evaluate
one expression after another.
------------------------------------------------------------
1 <exp> → <term>{+<term> | -<term>}
2 <term> → <factor>{*<factor> | /<factor>}
3 <factor> → <number> | pi | -<factor>| (<exp>) | <func>
4 <func> → <func name>(<exp>)
5 <func name> → sin | cos | tan | exp | sqrt | abs
6 <statement> → <id> = <exp>
'''
import math

class ParseError(Exception): pass

#==============================================================
# FRONT END PARSER
#==============================================================

i = 0 # keeps track of what character we are currently reading.
err = None
symbol_table = {}

#---------------------------------------
#<statement> → <id> = <exp>
#
def statement():
    global i, err
    if w[i] == 'display':
        i+=1
        display()
    else:
        if w[i+1] == '=':
            iden=w[i]           
            i+=2
            return assign(iden,exp())
        else:
            return exp()

#---------------------------------------
# Parse an Expression   <exp> → <term>{+<term> | -<term>}
#
def exp():
    global i, err

    value = term()
    while True:
        if w[i] == '+':
            i += 1
            value = binary_op('+', value, term())
        elif w[i] == '-':
            i += 1
            value = binary_op('-', value, term())
        else:
            break

    return value
#---------------------------------------
# Parse a Term   <term> → <factor>{+<factor> | -<factor>}
#
def term():
    global i, err

    value = factor()
    while True:
        if w[i] == '*':
            i += 1
            value = binary_op('*', value, factor())
        elif w[i] == '/':
            i += 1
            value = binary_op('/', value, factor())
        else:
            break

    return value
#---------------------------------------
# Parse a Factor   <factor> → (<exp>) | <number> 
#       
def factor():
    global i, err
    value = None
    
    if w[i] == 'pi':
        i += 1
        return math.pi
    elif w[i] == '-':
        i += 1
        return -factor()
    elif w[i] == '(':
        i +=1
        temp = exp()
        if w[i] == ')':
            i+=1
            return temp
    elif w[i] == func_name(w[i]):
        i +=1    
        value = func()
#    elif w[i] == 'sin' or w[i] == 'cos' or w[i] == 'tan' or w[i] == 'exp' or w[i] == 'sqrt' or w[i] == 'abs':
#        i +=1
#        return func()
    else:
        try:
            value = atomic(w[i])
            i += 1          # read the next character
        except ValueError:
            print('Number or Variable expected')
            value = None
    
    #print('factor returning', value)
    
    if value == None: raise ParseError
    return value

def func():
    global i, err
    value = func_call(func_name(w[i-1]), factor())
    return value

def func_name(x):
    global i, err
    if x == 'sin':
        return 'sin'
    elif x == 'cos':
        return 'cos'
    elif x == 'tan':
        return 'tan'
    elif x == 'exp':
        return 'exp'
    elif x == 'sqrt':
        return 'sqrt'
    elif x == 'abs':
        return 'abs'
    else: return None
    




#==============================================================
# BACK END PARSER (ACTION RULES)
#==============================================================

def binary_op(op, lhs, rhs):
    if op == '+': return lhs + rhs
    elif op == '-': return lhs - rhs
    elif op == '*': return lhs * rhs
    elif op == '/': return lhs / rhs
    else: return None

def func_call(fun_name, exp_value):
    if fun_name == 'sin': return math.sin(exp_value)
    elif fun_name == 'cos': return math.cos(exp_value)
    elif fun_name == 'tan': return math.tan(exp_value)
    elif fun_name == 'exp': return math.exp(exp_value)
    elif fun_name == 'sqrt': return math.sqrt(exp_value)
    elif fun_name == 'abs': return abs(exp_value)
    else: return None

def atomic(x):
    for v in symbol_table:
        if v==x :
            return float(symbol_table[v])
    return float(x)

def assign(iden,value):
    symbol_table[iden]=value
    print("Entry Done",iden,"=",value)
    print("")
    return symbol_table[iden]

def display():
    print('\nSymbol Table')
    print('\n====================')
    for iden in symbol_table:
        print(iden, '\t', symbol_table[iden])
    print()
    
#==============================================================
# User Interface Loop
#==============================================================
w = input('\nEnter expression: ')
while w != '':
    #------------------------------
    # Split string into token list.
    #
    for c in '()+-*/=':
        w = w.replace(c, ' '+c+' ')
    w = w.split()
    w.append('$') # EOF marker

    print('\nToken Stream:     ', end = '')
    for t in w: print(t, end = '  ')
    #print(w[0])
    print('\n')
    i = 0
    try:
        print('Value:           ', statement()) # call the parser
    except:
        print('Parse Error')
    print()
    if w[i] != '$': print('Syntax error:')
    print('read | un-read:   ', end = '')
    for c in w[:i]: print(c, end = '')
    print(' | ', end = '')
    for c in w[i:]: print(c, end = '')
    print()
    w = input('\n\nEnter expression: ')
#print(w[:i], '|', w[i:])

