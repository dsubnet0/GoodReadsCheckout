import argparse

from query_goodreads_csv import get_toread_titles
from QueryWebpage import query_southbury_library


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
    for title in get_toread_titles():
        if args.verbose:
            print(f'Searching for {title}...')
        if args.books:
            results = query_southbury_library(title, 'book')
            if len(results) > 0:
                print(f'{title} (book):')
                titles_hit += 1
            for r in results:
                if len(r)>0:
                    print('|'.join(r))
            if len(results) > 0:
                print('')
        if args.ebooks:
            results = query_southbury_library(title, 'ebook')
            if len(results) > 0:
                print(f'{title} (ebook):')
                titles_hit += 1
            for r in results:
                if len(r)>0:
                    print('|'.join(r))
            if len(results) > 0:
                print('')
        titles_considered += 1
        if args.number_of_hits and titles_hit >= int(args.number_of_hits):
            break
    print(f'titles searched: {str(titles_considered)}')
    print(f'results returned: {str(titles_hit)}')
