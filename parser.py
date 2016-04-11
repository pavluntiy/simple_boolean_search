import sys, os

class Parser:
    def parse(self, text):
        return self.get_or(text)

    def get_or(self, text):
        braces = 0
        text = text.strip()
        for i in range(len(text) - 1, -1, -1):
            if text[i] == ')':
                braces += 1
            if text[i] == '(':
                braces -= 1

            if braces == 0 and text[i] == '|':
                res = Query("|")
                res.left = self.get_or(text[:i])
                res.right = self.get_and(text[i + 1:])
                return res

        return self.get_and(text)

    def get_and(self, text):
        braces = 0
        text = text.strip()
        for i in range(len(text) - 1, -1, -1):
            if text[i] == ')':
                braces += 1
            if text[i] == '(':
                braces -= 1

            if braces == 0 and text[i] == '&':
                res = Query("&")
                res.left = self.get_and(text[:i])
                res.right = self.get_neg(text[i + 1: ])
                return res

        return self.get_neg(text)


    def get_neg(self, text):
        text = text.strip()
        if text[0] == "!":
            res = Query("!")
            res.negated = self.get_item(text[1:])
            return res

        return self.get_item(text)

    def get_item(self, text):
        text = text.strip()
        if text[0] == "(" and text[-1] == ")":
            return self.get_or(text[1:-1])

        res = Query("...")
        res.term = text.decode("utf-8").strip().lower()
        return res



class Query:
    def __init__(self, type):
        self.type = type
        self.negated = None
        self.left = None
        self.right = None
        self.term = None


def print_query( query, shift=0):
    if query.type == "...":
        print "\t"*shift, query.term
        return

    if query.type == "!":
        print "\t"*shift, "[ not "
        print_query(query.negated, shift + 1)
        print "\t"*shift, "]"
        return

    if query.type == "&":
        print "\t"*shift, "[ and"
        print_query(query.left, shift + 1)
        print "\t"*shift, "___"
        print_query(query.right, shift + 1)
        print "\t"*shift, "]"

    if query.type == "|":
        print "\t"*shift, "[ or"
        print_query(query.left, shift + 1)
        print "\t"*shift, "___"
        print_query(query.right, shift + 1)
        print "\t"*shift, "]"


def main():

    parser = Parser()
    line = sys.stdin.readline()
    while line != "":
        q = parser.parse(line)
        print_query(q)
        line = sys.stdin.readline()


    

if __name__ == "__main__":
    main()