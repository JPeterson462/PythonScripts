# Process a grouped list into a flat CSV structure

# Input: A (a, b, c), B (a, b, c)
# Output: A,a \n A,b \n A,c \n B,a \n B,b \b B,c

import argparse
import re
import sys

def process_commandline_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--groupname", default="Group")
    parser.add_argument("--itemname", default="Item")
    parser.add_argument("--delimiter", default=",")
    args = parser.parse_args()
    return args

def parse_groups(whitespace, content):
    pos = 0
    items = {}
    while pos < len(content):
        start_groupname = pos
        while pos < len(content) and content[pos] != '(':
            pos += 1
        end_groupname = pos
        pos += 1 # consume (
        start_groupcontent = pos
        parens = 1
        while pos < len(content) and parens > 0:
            if parens == 1 and content[pos] == ')':
                break
            if content[pos] == '(':
                parens += 1
            if content[pos] == ')':
                parens -= 1
            pos += 1
        end_groupcontent = pos
        pos += 1 # consume )

        groupname = content[start_groupname:end_groupname].strip()
        groupcontent = content[start_groupcontent:end_groupcontent].strip()

        items[groupname] = groupcontent

        while pos < len(content) and content[pos] in whitespace:
            pos += 1 # consume whitespace
        if pos < len(content):
            if content[pos] != ',':
                raise Exception("Invalid character: " + content[pos] + " at position " + str(pos))
            pos += 1 # consume ,
            while pos < len(content) and content[pos] in whitespace:
                pos += 1 # consume whitespace
    return items

def process_comma_delimited_list(content):
    items = content.split(',')
    return list(map(lambda x: x.strip(), items))

def read_input(options):
    data = {}
    with open(options.input, 'r') as f:
        content = f.read()
        groups = parse_groups([' ', '\t', '\r', '\n'], content)
        for groupname in groups:
            items = process_comma_delimited_list(groups[groupname])
            data[groupname] = items
    return data

def write_output(options, data):
    with open(options.output, 'w') as f:
        f.write(options.groupname + options.delimiter + options.itemname)
        for group in data:
            for item in data[group]:
                f.write("\n" + group + options.delimiter + item)


def main():
    opts = process_commandline_options()
    data = read_input(opts)
    write_output(opts, data)

main()
