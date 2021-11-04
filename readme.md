## Recursive Descent Parser

This program implements a recursive descent parser for the CFG below:

The grammar has added pi and unary minus to the previous program.
Also, the parse function is now called in a loop, so you can evaluate
one expression after another.
``` 
 - 1 <exp> → <term>{+<term> | -<term>}
 - 2 <term> → <factor>{*<factor> | /<factor>}
 - 3 <factor> → <number> | pi | -<factor>| (<exp>) | <func>
 - 4 <func> → <func name>(<exp>)
 - 5 <func name> → sin | cos | tan | exp | sqrt | abs
 - 6 <statement> → <id> = <exp>
```