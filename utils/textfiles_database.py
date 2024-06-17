import ast

def save_value(input_value, fpath):
    with open(fpath, "w") as file:
        file.write(str(input_value))


def load_data(fpath):
    with open(fpath, "r") as file:
        return ast.literal_eval(file.read()) 


