import argparse
import os
import ast
import keyword
import re
import random
import astor


def main():
    parser = argparse.ArgumentParser(description="Obfuscates your code SUTD style.")

    parser.add_argument(
        "sourceFile", type=str, help="path to the source file to obfuscate"
    )
    parser.add_argument("outFile", type=str, help="path to the outfile generated")
    parser.add_argument(
        "-r", "--random", action="store_true", help="shuffle the ofsucation items"
    )

    args = parser.parse_args()

    # function definition for reading the source file into an AST
    def convert_source_to_ast(path):
        full_path = os.path.abspath(path)
        f = open(full_path, "r")
        return ast.parse(f.read())

    # try to parse the source file
    try:
        tree = convert_source_to_ast(args.sourceFile)
    except:
        print("Could not read file!")
        raise
        exit(1)

    # create a list of imports so that we dont meme imports unless aliased
    imports = set()

    class ImportLister(ast.NodeVisitor):
        def visit_Import(self, node):
            if len(node.names) > 0:
                for alias in node.names:
                    imports.add(alias.asname or alias.name)

    ImportLister().visit(tree)
    print(imports)
    # set parent nodes for each node in the tree
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    # function definition to check if each node is memeable
    def is_node_memeable(node):
        # naive checking if keyword is a python reserved word
        if isinstance(node, ast.Name):
            name = node.id
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            name = node.name
        elif isinstance(node, ast.arg) or isinstance(node, ast.keyword):
            name = node.arg
        else:
            print(type(node))
        # short-circuit: name cannot be builtins, nonkeywords, globals or imports
        if keyword.iskeyword(name) or name in dir(__builtins__) or name in globals():
            return False
        if name in imports:
            return False
        # short-cicrcuit: do not rename direct class members
        if isinstance(node, ast.FunctionDef) and isinstance(node.parent, ast.ClassDef):
            return False
        if isinstance(node, ast.Name) and isinstance(node.parent, ast.ClassDef):
            return False
        # check if this name is in a safe-to-rename (LE out of LEGB) scope
        last_parent = node.parent
        while not isinstance(last_parent, ast.Module):
            # things that scope
            if not isinstance(last_parent, ast.FunctionDef) and not isinstance(
                last_parent, ast.Lambda
            ):
                last_parent = last_parent.parent
                continue
            else:
                # if this name's parent is a function call AND IT WAS NOT AN ARGUMENT, check if it was defined somewhere above
                # direct member functions of a class CANNOT be renamed
                # if not found, that means it was a global call and should not be fucked with
                if isinstance(node.parent, ast.Call) and node is node.parent.func:
                    last_call_parent = node.parent.parent
                    while name not in [
                        x.name
                        for x in ast.iter_child_nodes(last_call_parent)
                        if isinstance(x, ast.FunctionDef)
                    ]:
                        last_call_parent = last_call_parent.parent
                        if isinstance(last_call_parent, ast.Module):
                            return False
                    return True
                return True
        return False

    memeables = set()
    memeable_nodes = set()

    def judge_and_sort_node(node):
        if isinstance(node, ast.Name):
            if is_node_memeable(node):
                print(node.id, type(node), node.lineno)
                memeables.add(node.id)
                memeable_nodes.add(node)
            else:
                pass
        elif isinstance(node, ast.FunctionDef):
            if is_node_memeable(node):
                print(node.name, type(node), node.lineno)
                memeables.add(node.name)
                memeable_nodes.add(node)
        elif isinstance(
            node, ast.arguments
        ):  # this doesn't include function calls for some reason...
            for arg in node.args + node.kwonlyargs:
                if is_node_memeable(arg):
                    print(arg.arg, type(node))
                    memeables.add(arg.arg)
                    memeable_nodes.add(arg)
        elif isinstance(node, ast.Call):
            for arg in node.args:
                judge_and_sort_node(arg)
            for kw in node.keywords:
                print("caesar!!!", kw.arg, node.lineno)
                if is_node_memeable(kw):
                    memeables.add(kw.arg)
                    memeable_nodes.add(kw)

    # checks if each name is memeable and adds them to the memeables set
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            # print(type(node), node.lineno if hasattr(node,"lineno") else None)
            judge_and_sort_node(node)

    def read_meme_set(path):
        full_path = os.path.dirname(os.path.abspath(__file__)) + "/" + path
        f = open(full_path, "r")
        words = re.sub(r"#.*^", "", f.read(), flags=re.M).split("\n")
        return set(words)

    meme_set = read_meme_set("memes.txt")

    source_mapping = dict()
    meme_list = (
        random.sample(list(meme_set), len(meme_set)) if args.random else list(meme_set)
    )
    for i, memeable in enumerate(memeables):
        newname = meme_list[i % len(meme_list)]
        source_mapping[memeable] = (
            newname if i < len(meme_list) else newname + "_" + str(i // len(meme_list))
        )

    print(source_mapping)

    # walk through the node again, this time replacing the ids
    for node in memeable_nodes:
        if isinstance(node, ast.Name):
            node.id = source_mapping[node.id]
        elif isinstance(node, ast.FunctionDef):
            node.name = source_mapping[node.name]
        elif isinstance(node, ast.arg) or isinstance(node, ast.keyword):
            node.arg = source_mapping[node.arg]

    def generateMemeFile(path, tree):
        full_path = os.path.abspath(path)
        f = open(full_path, "w")
        f.write(astor.to_source(tree, add_line_information=True))
        return full_path

    generateMemeFile(args.outFile, tree)


if __name__ == "__main__":
    code = main()
    exit(code)
