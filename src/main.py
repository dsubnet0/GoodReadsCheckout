import argparse

from goodreads_list import GoodReadsList
from library_db import LibraryDB
from rakuten_querier import RakutenQuerier


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

    my_goodreads = GoodReadsList(user_string='3696598-doug', verbose=args.verbose)
    rakuten_application_id = 1093196333123354205
    rakuten_base_url = f'https://app.rakuten.co.jp/services/api/Kobo/EbookSearch/20170426'
    rq = RakutenQuerier(rakuten_base_url, rakuten_application_id, verbose=args.verbose)

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
            if isbn13:
                result = rq.query_by_isbn13(isbn13)
                if result['count'] > 0:
                    if args.verbose: print('results found by isbn13')
                    print(rq.format_results(result))
                    titles_hit += len(result)
                else:
                    if args.verbose: 'Falling back to querying by title'
                    result = rq.query_by_title(title)
                    if result and result['count'] > 0:
                        if args.verbose: 'results found by title'
                        print(rq.format_results(result))
                        titles_hit += len(result)
        titles_considered += 1
        if args.number_of_hits and titles_hit >= int(args.number_of_hits):
            break
    print(f'titles searched: {str(titles_considered)}')
    print(f'results returned: {str(titles_hit)}')
