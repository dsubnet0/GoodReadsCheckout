# GoodReadsCheckout
## Cross-reference an exported GoodReads "to-read" list with your local public library
### USAGE
With "goodreads_library_export.csv" in place locally:
```
pipenv install
pipenv run python main.py [--books] [--ebooks] [--number_of_hits=n]
```
[Here's how to export your GoodReads list](https://help.goodreads.com/s/article/How-do-I-import-or-export-my-books-1553870934590)

Currently only queries my library, the Southbury, CT Public Library (via Bibliomation), but methods could easily be added to generalize this. Please raise a PR!

### TODO
- Pull ToRead shelf from GoodReads via web scraping
- Query Rakuten API for purchasable ebooks
- Do not display results for books listed as "Checked out".
- In general, better, more specific searching, making use of both title and author from the CSV. And/Or use ISBN.
- Unexpectedly poor performance with serial querying the webpage via GET. Is there an actual API, perhaps for bulk queries