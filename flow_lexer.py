# Define the tokens that are important to deal with
from dataclasses import dataclass
import argparse
from rply import ParserGenerator, LexerGenerator

# Defining the data here

@dataclass
class Table:
    name : str
    path : str

    def build(self):
        return f"{self.name} = pd.read_csv({self.path})"

@dataclass
class Merge:
    left : str
    left_key : str
    right : str
    right_key : str
    how : str

    def build(self):
        return f"pd.merge({self.left}, {self.right}, how={self.how}, left_on={self.left_key}, right_on={self.right_key})"



# Defining the lexer

lg = LexerGenerator()
lg.add("NUMBER", r'\d+')
lg.add("STRING", r'"(?:[^"\\]|\\.)*"')
lg.add("TABLE", "table")
lg.add("MERGE", "merge")
lg.add("MERGETYPE", r"(inner|outer|right|left|cross)")
lg.add("FILTER", "filter")
lg.add("MAP", "map")
lg.add("SORT", "sort")
lg.add("EXPORT", "export")
lg.add("ON", "on")
lg.add("IDENTIFIER", r"[a-zA-Z_]\w*")
lg.add("DOT", r"\.")

lg.ignore(r"\s+")



# Defining the parser
pg = ParserGenerator(["NUMBER", "IDENTIFIER", "TABLE", "MERGE", "MERGETYPE", "FILTER", "MAP", "SORT", "EXPORT", "DOT", "ON", "STRING"])

@pg.production("main : expr")
def main(p):
    return p[0]

@pg.production("expr : expr expr")
def expr(p):
    return p

# table hello "mergeshell.csv";
# the table is identifier with the identifier and the string contains the file path and the dot closes the definition
@pg.production("expr : TABLE IDENTIFIER STRING DOT")
def table(p):
    return Table(p[1], p[2])


# merge identifier
@pg.production("expr : MERGE IDENTIFIER ON IDENTIFIER IDENTIFIER ON IDENTIFIER MERGETYPE DOT")
def merge(p):
    return Merge(p[1], p[3], p[4], p[6], p[7])




# build the lexer and parser
lexer = lg.build()
parser = pg.build()


# parse the cli arguments

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("path")


args = arg_parser.parse_args()

# print(str(args.path))

with open(str(args.path), "r") as f:
    src = f.read()
    print(src)

    # for token in lexer.lex(src):
    #     print(token)

    tree = parser.parse(lexer.lex(src))



print(tree)
    