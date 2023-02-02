import csv
import sys


def handling_cell(string: str) -> str:
    """ Finding cell value by it`s fild name and index

        Args:
            string::[str]
                String to find it`s value

        Returns:
            Value of cell::str
                Handled value
    """

    splitted = []

    for i in range(len(string)):
        if string[i].isnumeric():
            splitted.append(string[:i])
            splitted.append(string[i:])
            break

    try:
        return str(data_dict[splitted[0]][index_dict[splitted[1]]])
    except IndexError:
        print('Wrong table format!')
        sys.exit()
    except KeyError:
        print('Wrong cell index!')
        sys.exit()


def calculate_expression(string: str) -> str:
    """ Finding cells and calculating string expression

        Args:
            string::[str]
                String to handle cells and calculate expression

        Returns:
            calculated_expression::str
                Handled expression
    """

    sign_index = 0

    for elem in signs:
        if elem in string:
            sign_index = string.index(elem)
    if not sign_index:
        return handling_cell(string)

    array = [handling_cell(string[:sign_index]), string[sign_index], handling_cell(string[sign_index + 1:])]

    try:
        return str(eval(''.join(array)))
    except ZeroDivisionError:
        print('Division by zero is not possible!')
        sys.exit()


with open(sys.argv[1], 'r') as file:  # Reading csv file and convert in to dictionary
    data_reader = csv.DictReader(file)
    data_dict = {}
    for line in data_reader:
        for key, value in line.items():
            data_dict.setdefault(key, [])
            data_dict[key].append(value)

signs = ['+', '-', '/', '*']
index_dict = {}
for element in enumerate(data_dict['']):  # Writing to index_dict map of indexes matching
    index_dict[element[1]] = element[0]

for key, value in data_dict.items():  # Calculating cells
    for index in range(len(value)):
        try:
            if not value[index].isnumeric():
                data_dict[key][index] = calculate_expression(value[index][1:])
        except AttributeError:
            print('Wrong table format!')
            sys.exit()


writer = csv.DictWriter(sys.stdout, fieldnames=data_dict)  # Output calculated dictionary to stdout in csv format
writer.writeheader()
for position in range(len(data_dict[''])):
    extension_dict = {}
    for key in data_dict.keys():
        extension_dict[key] = data_dict[key][position]
    writer.writerow(extension_dict)
