# GoodReadsCheckout
## Cross-reference an exported GoodReads "to-read" list with your local public library
### USAGE
```
pipenv install
pipenv run python main.py [--books] [--ebooks] [--number_of_hits=n]
```

Currently only queries my library, the Southbury, CT Public Library (via Bibliomation), using my personal Goodreads list, but methods could easily be added to generalize this. Please raise a PR!

### TODO
- Do not display results for books listed as "Checked out".
- Unexpectedly poor performance with serial querying the webpage via GET. Is there an actual API, perhaps for bulk queries