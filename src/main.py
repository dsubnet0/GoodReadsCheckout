import argparse

from GoodReads import GoodReads
from library_db import LibraryDB
from query_webpage import query_southbury_library_by_isbn
from query_api import query_rakuten_by_isbn13


def print_library_results(isbn: str, format: str = 'book'):
    titles_hit = 0
    if args.verbose: print(f'searching library for {isbn} ({format})...')
    results = query_southbury_library_by_isbn(isbn, format)
    if len(results) > 0:
        print(f'\n{isbn} ({format}):')
        titles_hit += 1
        for r in results:
            print(' | '.join(r.values()))
    return titles_hit


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--books', help='Search for regular books', action='store_true')
    parser.add_argument('--ebooks', help='Search for ebooks', action='store_true')
    parser.add_argument('--verbose', help='Verbose', action='store_true')
    parser.add_argument('--number_of_hits', '-n', help='Stop after this many hits')
    args = parser.parse_args()

    titles_considered = 0
    titles_hit = 0
    page = 0

    my_goodreads = GoodReads(user_string='3696598-doug', verbose=args.verbose)

    for book_dict in my_goodreads.toread_list:
        if args.verbose: print(book_dict)
        title = book_dict['title']
        isbn = book_dict['isbn']
        isbn13 = book_dict['isbn13']
        if args.books:
            my_library = LibraryDB(verbose=args.verbose)
            library_result = my_library.get_book(title=title, isbn=isbn, format='book')
            if library_result:
                print(library_result)
                titles_hit += 1
        if args.ebooks:
            titles_hit += print_library_results(isbn, 'ebook')
            if isbn13:
                titles_hit += print_rakuten_results(isbn13)
        titles_considered += 1
        if args.verbose: print('')
        if args.number_of_hits and titles_hit >= int(args.number_of_hits):
            break
    print(f'titles searched: {str(titles_considered)}')
    print(f'results returned: {str(titles_hit)}')
