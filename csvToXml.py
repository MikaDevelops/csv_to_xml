import re, sys, time

if len(sys.argv) < 2:
    print("Give source file name as parameter. Closing application.")
    quit()

source_file = sys.argv[1]

DEFAULT_DELIMITER = "\t"
XML_HEADER = "<?xml version=\"1.0\" encoding=\"ISO-8859-1\" ?>"

def check_delimiter(delimiter_char: str)->str:
    regular_expression = "[^a-öA-Ö]"
    if delimiter_char == "" :
        return DEFAULT_DELIMITER
    if not re.match(regular_expression, delimiter_char):
        print("Little too weird delimiter!! Closing application")
        quit()
    return delimiter_char

def read_data(source: str, delimiter: str)->dict:
    data_dict = {
        "header": [],
        "data_rows": []
    }

    with open(source,'r') as sfile:
        header_line = sfile.readline()
        header_values = header_line.rstrip().split(delimiter)
        data_dict["header"] = header_values
        for row in sfile:
            row_list = row.rstrip().split(delimiter)
            data_dict["data_rows"].append( row_list )

    return data_dict

def do_mapping(data: dict):
    new_header_values = []
    for value in data["header"]:
        new_value = input(f"Give correct field name to map to for {value}: ")
        new_header_values.append(new_value)

    data["header_mapping"] = new_header_values

def write_xml(data: dict):
    with open("data.xml", "w") as file:
        file.write(XML_HEADER)
        file.write("\n<entityset>\n")

        for row in data["data_rows"]:
            file.write(f"<entity>\n<template code=\"{data["model_code"]}\" name=\"\" />\n")

            for i in range(len(row)):
                file.write(f"<attribute code=\"{data["header"][i]}\">\n")
                file.write(f"<value>{row[i]}</value>\n")
                file.write("</attribute>\n")
            
            file.write('</entity>\n')

        file.write("</entityset>")
    
print("Welcome to csv to xml making application.")
user_delimiter_character = input("Give a delimiter charater that separates values (default=tabulator) : ")
delimiter_character = check_delimiter(user_delimiter_character)

source_data = read_data(source_file, delimiter_character)

is_columns_ok = ""
while True:
    is_columns_ok = input("Is the column names ok in the source? (y for yes, n for no) ")
    if is_columns_ok == "y" or is_columns_ok == "n" or is_columns_ok == "Y" or is_columns_ok == "N": 
        break

if is_columns_ok == "n" or is_columns_ok == "N": do_mapping(source_data)

source_data["model_code"] = input("Model code ")

start_time = time.perf_counter_ns()
write_xml(source_data)
end_time = time.perf_counter_ns()
timeconsumed= (end_time - start_time)/1000000
print(f"Writing xml took: {timeconsumed} milliseconds")
quit()