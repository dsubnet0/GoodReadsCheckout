import csv

def get_toread_titles():
    title_list = []
    with open('goodreads_library_export.csv', encoding='utf8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['Bookshelves'] == 'to-read':
                title_list.append(f"{row['Title']} {row['Author']}")
    return title_list