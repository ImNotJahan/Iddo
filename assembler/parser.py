import re
from string import whitespace

comment_expr = re.compile("//(.*)")

''' turns a text file into a list of operations (i.e., a list of lists of tokens) '''
def parse(file) -> list[list[str]]:
    cleaned_text = clean(file)
    return [line.split() for line in cleaned_text.split("\n")]

''' reads a file and outputs the content with comments and empty lines removed '''
def clean(file) -> str:
    cleaned_text = ""

    for line in file:
        line = re.sub(comment_expr, "", line) # remove comments
        if all(c in whitespace for c in line): # ignore empty lines
            continue

        cleaned_text += line

    # remove trailing newlines
    if cleaned_text[-1] == "\n":
        cleaned_text = cleaned_text[0:-1]
    
    return cleaned_text

if __name__ == "__main__":
    print(parse(open(input("File to parse: "))))