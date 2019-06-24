from pybtex.database import parse_file
import numpy as np
import os
import matplotlib.pyplot as plt

######## VARIABLES ########
show_plots = False
######## VARIABLES ########

def save_csv(path, A, B, title_A, title_B):
  f= open(path,"w", encoding="utf-8")
  f.write(f"{title_A},{title_B}\n")
  for a, b in zip(A, B):
    f.write(f"{a},{b}\n")
  f.close()

filenames = [f for f in os.listdir() if ".bib" in f]

'''
check for repeated entries
'''

for filename in filenames:
  path = './' + filename.replace(".bib","")
  os.makedirs(path, exist_ok=True)
  bib_data = parse_file(filename)

######## PUBLICATIONS PER YEAR    ########
  years = []
  for k in bib_data.entries.keys():
    if "year" in bib_data.entries[k].fields:
      years.append(bib_data.entries[k].fields["year"])
  years = np.array(years, dtype=np.int)
  unique_elements, counts = np.unique(years, return_counts=True)

  save_csv(
    path + "/01_Publications_per_year.csv",
    unique_elements, 
    counts, 
    "Year", 
    "Number of Publications" 
  )

  plt.rcParams['figure.figsize'] = 15, 5 # inches  
  plt.xticks(range(np.min(unique_elements), np.max(unique_elements) + 1))
  plt.grid(which='major', axis='both')
  plt.plot(unique_elements, counts, 'k.-')
  plt.tight_layout()
  plt.savefig(path + "/01_Publications_per_year")
  if show_plots: plt.show()
  plt.close("all")

######## DOCUMENT TYPES           ########
  document_type = []
  for k in bib_data.entries.keys():
    if "document_type" in bib_data.entries[k].fields:
      document_type.append(bib_data.entries[k].fields["document_type"])
  document_type = np.array(document_type, dtype=np.object)
  unique_elements, counts = np.unique(document_type, return_counts=True)
  idxs = np.flip(np.argsort(counts))
  unique_elements = unique_elements[idxs]
  counts = counts[idxs]

  save_csv(
    path + "/02_Document_types.csv",
    unique_elements,
    counts,
    "Type",
    "Number of Publications"
  )

  plt.rcParams['figure.figsize'] = 15, 5 # inches
  plt.grid(which='major', axis='y')
  x = np.arange(counts.shape[0])
  plt.xticks(x, unique_elements)
  plt.gcf().autofmt_xdate()
  plt.bar(x, counts)
  plt.tight_layout()
  plt.savefig(path + "/02_Document_types")
  if show_plots: plt.show()
  plt.close("all")

######## PUBLICATIONS PER AUTHOR  ########
  authors = []
  for k in bib_data.entries.keys():
    if "author" in bib_data.entries[k].persons.keys():
      all_authors = bib_data.entries[k].fields["author"]
      all_authors = all_authors.split("and")
      for a in all_authors:
        authors.append(a.strip())
    elif "editor" in bib_data.entries[k].persons.keys():
      all_authors = bib_data.entries[k].fields["editor"]
      all_authors = all_authors.split("and")
      for a in all_authors:
        clean_a = a.strip()
        clean_a = clean_a.replace(",", ";")
        authors.append(clean_a)
  authors = np.array(authors, dtype=np.object)
  unique_elements, counts = np.unique(authors, return_counts=True)
  idxs = np.flip(np.argsort(counts))
  unique_elements = unique_elements[idxs]
  counts = counts[idxs]

  save_csv(
    path + "/03_Publications_per_author.csv",
    unique_elements,
    counts,
    "Author",
    "Number of Publications"
  )

  lim = 0
  while counts[lim] > 2 and lim < 40:
    lim += 1
  unique_elements = unique_elements[0 : lim]
  counts = counts[0 : lim]
  plt.rcParams['figure.figsize'] = 15, 5 # inches
  plt.grid(which='major', axis='y')
  x = np.arange(counts.shape[0])
  plt.xticks(x, unique_elements)
  plt.gcf().autofmt_xdate()
  plt.bar(x, counts)
  plt.tight_layout()
  plt.savefig(path + "/03_Publications_per_author")
  if show_plots: plt.show()
  plt.close("all")

######## KEYWORD FREQUENCY        ########
  keywords = []
  for k in bib_data.entries.keys():
    if "keywords" in bib_data.entries[k].fields:
      all_keywords = bib_data.entries[k].fields["keywords"]
      all_keywords = all_keywords.split(";")
      for a in all_keywords:
        keywords.append(a.strip().lower())
    if "author_keywords" in bib_data.entries[k].fields:
      all_keywords = bib_data.entries[k].fields["author_keywords"]
      all_keywords = all_keywords.split(";")
      for a in all_keywords:
        keywords.append(a.strip().lower())
  keywords = np.array(keywords, dtype=np.object)
  unique_elements, counts = np.unique(keywords, return_counts=True)
  idxs = np.flip(np.argsort(counts))
  unique_elements = unique_elements[idxs]
  counts = counts[idxs]

  save_csv(
    path + "/04_Keyword_frequency.csv",
    unique_elements,
    counts,
    "Keyword",
    "Frequency"
  )

  lim = 0
  while counts[lim] > 2 and lim < 40:
    lim += 1
  unique_elements = unique_elements[0 : lim]
  counts = counts[0 : lim]

  plt.rcParams['figure.figsize'] = 15, 10 # inches
  plt.grid(which='major', axis='y')
  x = np.arange(counts.shape[0])
  plt.xticks(x, unique_elements)
  plt.gcf().autofmt_xdate()
  plt.bar(x, counts)
  plt.tight_layout()
  plt.savefig(path + "/04_Keyword_frequency")
  if show_plots: plt.show()
  plt.close("all")

######## PUBLICATIONS PER JOURNAL ########
  journals = []
  for k in bib_data.entries.keys():
    if "journal" in bib_data.entries[k].fields:
      journals.append(bib_data.entries[k].fields["journal"].lower())
  journals = np.array(journals, dtype=np.object)
  unique_elements, counts = np.unique(journals, return_counts=True)
  idxs = np.flip(np.argsort(counts))
  unique_elements = unique_elements[idxs]
  counts = counts[idxs]

  save_csv(
    path + "/05_Publications_per_journal.csv",
    unique_elements,
    counts,
    "Journal",
    "Number of Publications"
  )

  lim = 0
  while counts[lim] > 2 and lim < 40:
    lim += 1
  unique_elements = unique_elements[0 : lim]
  counts = counts[0 : lim]

  plt.rcParams['figure.figsize'] = 20, 15 # inches
  plt.grid(which='major', axis='y')
  x = np.arange(counts.shape[0])
  plt.xticks(x, unique_elements)
  plt.gcf().autofmt_xdate()
  plt.bar(x, counts)
  plt.tight_layout()
  plt.savefig(path + "/05_Publications_per_journal")
  if show_plots: plt.show()
  plt.close("all")
  