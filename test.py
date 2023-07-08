import re

filename = "20230708-173848_pseudo_s123123_i1"

def find_bit_count(filename):
    match_i = re.search(r"_i(\d+).", filename)
    print( match_i.group(1))

find_bit_count(filename)