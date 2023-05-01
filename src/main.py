import argparse

from query_webpage import query_southbury_library_by_isbn, get_goodreads_list
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

def print_rakuten_results(isbn13: str):
    titles_hit = 0
    if args.verbose: print(f'searching rakuten for {isbn13}...')
    results = query_rakuten_by_isbn13(isbn13, args.verbose)
    if len(results) > 0 and len(results['Items']) > 0:
        titles_hit += 1
        for r in results['Items']:
            print(f'{r["Item"]["title"]} - {r["Item"]["itemUrl"]}')
    return titles_hit

if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--books', help='Search for regular books', action='store_true')
    parser.add_argument('--ebooks', help='Search for ebooks', action='store_true')
    parser.add_argument('--verbose', help='Verbose', action='store_true')
    parser.add_argument('--number_of_hits', '-n', help='Stop after this many hits')
    parser.add_argument('--scoop-size', '-s', help='GoodReads scoop size')
    args = parser.parse_args()

    titles_considered = 0
    titles_hit = 0
    page = 0
    for book_dict in get_goodreads_list(user_string='3696598-doug', verbose=args.verbose, scoop_size=args.scoop_size):
        if args.verbose: print(book_dict)
        isbn = book_dict['isbn']
        isbn13 = book_dict['isbn13']
        if args.books:
            titles_hit += print_library_results(isbn, 'book')
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
