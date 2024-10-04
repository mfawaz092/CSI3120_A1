import os
from typing import Union, List, Optional

alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
all_valid_chars = var_chars + ["(", ")", ".", "\\"]
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"


def read_lines_from_txt(fp: [str, os.PathLike]) -> List[str]:
    """
    :param fp: File path of the .txt file.
    :return: The lines of the file path removing trailing whitespaces
    and newline characters.
    """
    lines = []
    with open(fp, 'r') as file:
        for line in file:
            lines.append(line.rstrip()) 
    return lines


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """
    # Check if the string is not empty
    if not s:
        return False

    # Check if the first character is a valid character
    if s[0] not in alphabet_chars:
        return False

    # Check if all other characters are valid
    for c in s[1:]:
        if c not in var_chars:
            return False

    return True



class Node:
    """
    Nodes in a parse tree
    Attributes:
        elem: a list of strings
        children: a list of child nodes
    """
    def __init__(self, elem: List[str] = None):
        self.elem = elem
        self.children = []


    def add_child_node(self, node: 'Node') -> None:
        self.children.append(node)


class ParseTree:
    """
    A full parse tree, with nodes
    Attributes:
        root: the root of the tree
    """
    def __init__(self, root):
        self.root = root

    def print_tree(self, node: Optional[Node] = None, level: int = 0) -> None:
        # TODO
        print("")
        


def parse_tokens(s_: str) -> Union[List[str], bool]:
    """
    Gets the final tokens for valid strings as a list of strings, only for valid syntax,
    where tokens are (no whitespace included)
    \\ values for lambdas
    valid variable names
    opening and closing parenthesis
    Note that dots are replaced with corresponding parenthesis
    :param s_: the input string
    :return: A List of tokens (strings) if a valid input, otherwise False
    """

    # check before unmatched paranthesis before tokenizing
    open_count = 0  # Count of opening parentheses
    for i, char in enumerate(s_):
        if char == '(':
            open_count += 1
        elif char == ')':
            open_count -= 1
            if open_count < 0:  # More closing than opening parentheses
                print(f'Bracket ) at index : {i} is not matched with a ( .')
                return False

    # After iterating, check if there are unmatched opening parentheses
    if open_count > 0:
        print(f'Bracket ( at index: {s_.rfind("(", 0, len(s_))} is not matched with a ) .')
        return False

    s = s_ 
    tokens = []
    i = 0  # Pointer for the current index

    while i < len(s):
        char = s[i]

        if char == '\\' and (len(s) <= 1 or i + 1 > len(s)):
            print(f'Missing complete lambda expression starting at index {i}.')


        if char == '\\':
            # Check if the next character is a whitespace
            if i + 1 < len(s) and s[i + 1] == ' ':
                print(f'Invalid space inserted after \ at index {i}.')
                return False

        # Skip whitespace characters
        if char.isspace():
            i += 1
            continue

        # Handle numbers at the start
        if char in numeric_chars:
            print(f'Error at index {i}, variables cannot begin with digits.')
            return False


        # Handle dots at the start 
        if char == '.' and i == 0:
            print(f'Encountered dot at invalid index {i}.')
            return False

        # Handle dots 
        if char == '.':
            # Check if the character before is a valid variable name
            if i - 1 < len(s) and s[i - 1] not in var_chars:
                print(f'Must have a variable name before character . at index {i - 1}.')
                return False
            
        # Handle opening parenthesis
        if char == '(':
            # Check if the next character is a valid variable name
            if i + 1 < len(s) and s[i + 1] == ')':
                print(f'Missing expression for parenthesis at index {i}.')
                return False
            else:
                tokens.append('(')
                i += 1
                continue

        # Handle closing parenthesis
        elif char == ')':
            tokens.append(')')
            i += 1
            continue

        # Handle backslash 
        elif char == '\\':
            # Check if the next character is a valid variable name
            if i + 1 < len(s) and is_valid_var_name(s[i + 1]):
                tokens.append('\\')
                tokens.append(s[i + 1])  # Append the variable name after backslash
                i += 2  # Move past the backslash and variable
            else:
                print(f'Backlashes not followed by a variable name at {i}')
                return False

        # Handle variable names
        elif char.isalpha():
            start = i
            while i < len(s) and s[i] in var_chars:
                i += 1
            var_name = s[start:i]
            if is_valid_var_name(var_name):
                tokens.append(var_name)
            else:
                return False

        # Handle dot operator
        elif char == '.':
            # replace dot with an opening parenthesis
            if tokens and tokens[-1] not in ['(', '\\']:  
                tokens.append('(') 
                i += 1
            else:
                return False

        # Handle invalid characters
        else:
            return False

    # Close any opened parentheses 
    open_count = tokens.count('(')
    close_count = tokens.count(')')

    while open_count > close_count:
        tokens.append(')')
        close_count += 1

    return tokens if open_count == close_count else False


def read_lines_from_txt_check_validity(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string  to yield a tokenized list of strings for printing, joined by _ characters
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens funct ion).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string {l} is {'_'.join(tokens)}")
    if len(valid_lines) == len(lines):
        print(f"All lines are valid")



def read_lines_from_txt_output_parse_tree(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string to yield a tokenized output string, to be used in constructing a parse tree. The
    parse tree should call print_tree() to print its content to the console.
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            print("\n")
            parse_tree2 = build_parse_tree(tokens)
            parse_tree2.print_tree()




def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    An inner recursive inner function to build a parse tree
    :param tokens: A list of token strings
    :param node: A Node object
    :return: a node with children whose tokens are variables, parenthesis, slashes, or the inner part of an expression
    """

    if not tokens:
        return None

    node = Node(tokens[:1])
    tokens = tokens[1:]

    while tokens:
        token = tokens.pop(0)
        if token == '(':
            child_node = build_parse_tree_rec(tokens)
            if child_node:
                node.add_child_node(child_node)
        elif token == ')':
            break
        else:
            child_node = Node([token])
            node.add_child_node(child_node)

    return node


def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Build a parse tree from a list of tokens
    :param tokens: List of tokens
    :return: parse tree
    """
    pt = ParseTree(build_parse_tree_rec(tokens))
    return pt


if __name__ == "__main__":

    print("\n\nChecking valid examples...")
    read_lines_from_txt_check_validity(valid_examples_fp)
    read_lines_from_txt_output_parse_tree(valid_examples_fp)

    print("Checking invalid examples...")
    read_lines_from_txt_check_validity(invalid_examples_fp)