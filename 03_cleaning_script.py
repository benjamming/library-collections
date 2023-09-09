import pandas as pd
import logging as log

# Cleaning raw data from Wikipedia scraping in authors.csv
# Source and target file locations
DWIKI = "data/raw/authors.csv"
CDWIKI = "data/clean/authors.csv"

def fix_wiki_author(name:str) -> str:
    """Change author record like "author (9999 etc.)" to just "author" """
    truncation_index = name.find("(") -1
    return name[:truncation_index]

def fix_authors_dataframe(authors:pd.DataFrame) -> pd.DataFrame:
    """Find and replace author records with extraneous parenthetical codas"""

    #Find subset of author names that need to be cleaned
    to_fix = authors[authors.Name.str.contains("(", regex=False)]
    log.info(f"fixing {len(to_fix)} records")
    #Clean author names and update the input daraframe
    authors.update(to_fix.Name.apply(fix_wiki_author))
    return authors


def clean_wiki_authors(input_csv_path, output_csv_path) -> None:
    """Read in raw authors data, strip parenthetical coda, write clean data"""

    log.info(f"Reading in authors CSV: {input_csv_path}")
    authors = pd.read_csv(input_csv_path)
    authors_clean = fix_authors_dataframe(authors)
    log.info(f"Writing clean authors CSV: {output_csv_path}")
    authors_clean.to_csv(output_csv_path)


#Cleaning books data from  library records
# Source and target file locations
DBOOKS = "data/raw/books.csv.gz"
CDBOOKS = "data/clean/books.csv.gz"

def validate_columns(df:pd.DataFrame) -> None:
    """Verify that the data has the expected structure."""
    EXPECTED_COLUMNS = ['BibNum', 'Title', 'Author', 'ISBN', 'PublicationYear', 'ItemType',
       'ItemCollection', 'ItemLocation', 'ItemPrice', 'ReportDate']
    if not all(item in list(df.columns) for item in EXPECTED_COLUMNS):
        log.error("Unexpected columns in source data")
        exit(1)
    return


def clean_books(input_csv_path, output_csv_path) -> None:
    log.info(f"Reading in books csv: {input_csv_path}")
    books = pd.read_csv(input_csv_path)

    validate_columns(books)

    log.info("Dropping unneeded columns")
    books = books.drop(["ISBN", "ItemType", "ReportDate"], axis=1)




def main():
    #clean_wiki_authors(DWIKI, CDWIKI)

if __name__ == '__main__':
    log.basicConfig(level=log.ERROR, format='%(levelname)s - %(message)s')
    main()