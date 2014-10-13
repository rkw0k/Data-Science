"""
You are given two strings. Determine if the second string is a substring of the
first. The second string may contain an asterisk (*) which should be treated as 
a wild card that matches zero or more characters. The asterisk can be escaped by
a \ char in which case it should be interpreted as a literal * character. The 
strings can contain English letters and numbers, *, and \.

Input:
Your program should read lines of text from standard input. Each line will 
contain two strings separated by a comma.

Output:
For each line of input, if the second string is a substring of the first, print 
"true" (lowercase). Otherwise print "false" (lowercase), one per line.

Ricky Kwok, rickyk9487@gmail.com, 2014-10-13."""

import re

def is_sec_in_fir(s, f):
    """ Check if "second" is a substring of "first" with wild letter(s) if
        asterisk (*) appears in "second" without case-sensitivity. """
    s = s.lower()
    f = f.lower()
    boolean = False
    
    if ("*" not in s) and (s in f):
        boolean = True
    elif "*" in s:
        boolean = wildcard(s,f)
        
    return boolean

def wildcard(s, f):
    """ If * appears in the second string, this splits and uses a regular
        expression. The asterisk acts as a wildcard with zero or more symbols
        containing letters, numbers, (*) or (\) literal. Returns true if
        the second string (s) is a substring of the first (f)."""
    Bool = False
    s1, s2 = s.split("*")
    reg_ex = re.compile("%s([\w\\\d\*]*)%s"%(s1,s2))
    if re.findall(reg_ex, f):
        Bool = True
                    
    return Bool
          
def print_tf(Bool):
    if Bool:
        print "true"
    else:
        print "false"

def main():
    """ Reads from the standard input until user breaks with Enter/Return."""
    while True:
        my_input = raw_input("To break, press Enter. Otherwise enter second, first: " )
        if len(my_input) > 0 and "," in my_input:
            s, f = my_input.split(",")
            Bool = is_sec_in_fir(s,f)
            print_tf(Bool)
        elif len(my_input) > 0 and "," not in my_input:
            print "Please seperate two inputs with a single comma."
        else:
            break
            
if __name__ == '__main__':
    main()