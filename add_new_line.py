import re
import csv

fn = "my_file.csv"
f = open(fn)
text = f.read()
f.close()
pattern = re.compile(r"[\w\-\#\\\!\?\:\s]+,[\w]+[\s]")
lst = re.findall(pattern, text)
# print len(lst) # Make sure you find all commas in original
new_lst = [l[:-1] for l in lst]
# print new_lst

newfn = fn.split(".")[0]+"_new"+".csv"
with open(newfn, 'wb') as myfile:
    wr = csv.writer(myfile, delimiter="\n", quoting=csv.QUOTE_MINIMAL)
    wr.writerow(new_lst)
    
