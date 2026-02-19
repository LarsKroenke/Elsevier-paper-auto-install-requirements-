import csv
import os


def write_variables(variable, identifier, precision=None):

    variable = f'{variable:Lx}'

    if precision:
        variable = variable.replace(']', f'round-mode=figures, round-precision={precision}]')

    dict_var = {}

    file_path = os.path.join(os.path.dirname(os.getcwd()), 'TeX', 'Formeln/_variables.dat')

    try: 
        with open(file_path, newline="") as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                dict_var[row[0]] = row[1]
    except FileNotFoundError:
        pass
    
    dict_var[identifier] = variable

    with open(file_path, 'w') as f:
        for key in dict_var.keys():
            f.write(f'{key};{dict_var[key]}\n')