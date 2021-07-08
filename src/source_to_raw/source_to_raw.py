
def read_file(filepath):
    with open(filepath, "r") as my_file:
        data = my_file.readlines()
    return data
