from pybtex.database import parse_file
import pybtex
import os

name = 'ANNs&StockMarket.bib'

f = open(name,"r", encoding='utf8')
text = f.readlines()
f.close()

first_comment = 0
for i, line in enumerate(text):
  if "@Comment" in line:
    first_comment = i
    break

text = text[first_comment:]

append = ""
for line in text:
  append += line


bib_data = parse_file(name)
clean_bib_data = pybtex.database.BibliographyData()

repeated_keys = []
query = ''
for k1 in bib_data.entries.keys():
  if "title" in bib_data.entries[k1].fields and k1 not in repeated_keys:
    t1 = bib_data.entries[k1].fields["title"]
    t1 = t1.lower().replace(":","").strip()
    for k2 in bib_data.entries.keys():
      if "title" in bib_data.entries[k2].fields and k1 not in repeated_keys:
        t2 = bib_data.entries[k2].fields["title"]
        t2 = t2.lower().replace(":","").strip()
        if t1 == t2 and k1 != k2:
          # bib_data.entries[k1].fields["__markedentry"] = "[tesse:4]"
          # bib_data.entries[k2].fields["__markedentry"] = "[tesse:4]"
          # print(t2)
          repeated_keys.append(k2)

print(f"{len(repeated_keys)} repeated entries found and marked")
for k in repeated_keys:
  bib_data.entries[k].fields["__markedentry"] = "[tesse:5]"

bib_data.to_file(name, "bibtex")

f = open(name,"a")
f.write(append)
f.close()