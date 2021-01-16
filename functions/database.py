import psycopg2
import pandas as pd


def create_tables():
    """
    This function creates two SQL type tables for scraped items from ebay webpage in Heroku database:
    category (id: int, category: str)

    ebay (id: serial, category: int, title: varchar, price: varchar, urlItem: varchar, urlImage: varchar)

    Parameters:

    None

    Returns:

    None
    """

    # connecting to the database
    connection = psycopg2.connect(
        database="d8agtv34e8as8v",
        user="khrbktgjasltxt",
        password="ce6001a6731cda5f63778855fef76b54521d18fe8388bdf9ca41a61efccbdb3a",
        host="ec2-79-125-59-247.eu-west-1.compute.amazonaws.com",
        port="5432",
    )

    drop_ebay = "DROP TABLE ebay CASCADE"
    drop_categories = "DROP TABLE categories CASCADE"
    create_ebay = "CREATE TABLE IF NOT EXISTS ebay (\
    id serial PRIMARY KEY,\
    category int, \
    title varchar(5000), \
    price varchar(5000), \
    urlItem varchar(5000), \
    urlImage varchar(5000),\
    FOREIGN KEY (category) REFERENCES categories(id)\
    )"
    create_categories = "CREATE TABLE IF NOT EXISTS categories (\
    category varchar(15),\
    id int PRIMARY KEY\
    )"

    print("Tables ebay and categories are being created")
    cur = connection.cursor()
    cur.execute(drop_categories)
    cur.execute(drop_ebay)
    cur.execute(create_categories)
    cur.execute(create_ebay)
    connection.commit()
    print("Tables ebay and categories have been successfully created")


def insert_data_into_categories():
    """
    This function inserts data into previously created categories table in Heroku database for scraped items from the ebay website.
    The inputs for id and category are as follows:
    (1, bracelet),
    (2, shoes),
    (3, dress)

    Parameters:

    None

    Returns:

    None
    """
    # connecting to the database
    connection = psycopg2.connect(
        database="d8agtv34e8as8v",
        user="khrbktgjasltxt",
        password="ce6001a6731cda5f63778855fef76b54521d18fe8388bdf9ca41a61efccbdb3a",
        host="ec2-79-125-59-247.eu-west-1.compute.amazonaws.com",
        port="5432",
    )

    commands = "INSERT INTO categories(id, category) \
        VALUES (1, 'bracelet'), \
        (2, 'shoes'), \
        (3,'dress');"

    print("Bracelet, shoes and dress categories are being inserted..")

    cur = connection.cursor()
    cur.execute(commands)

    print("Bracelet, shoes and dress categories have been successfully inserted")

    connection.commit()


def insert_data_into_ebay(dataframe):
    """
    This function inserts data into previously created ebay table in Heroku database for scraped items from the ebay website.

    Parameters:

    dataframe: a pandas dataframe with the following columns: category (int), title (str), price (str),
    urlItem (str), urlImage (str)

    Returns:

    None
    """

    # connecting to the database
    connection = psycopg2.connect(
        database="d8agtv34e8as8v",
        user="khrbktgjasltxt",
        password="ce6001a6731cda5f63778855fef76b54521d18fe8388bdf9ca41a61efccbdb3a",
        host="ec2-79-125-59-247.eu-west-1.compute.amazonaws.com",
        port="5432",
    )

    print("Data from the table loading to the postgreSQL database..")

    # inserting data into the ebay table using row iterations
    cur = connection.cursor()

    for index, row in dataframe.iterrows():
        cur.execute(
            "INSERT INTO ebay (category, title, price, urlItem, urlImage) values(%s, %s, %s, %s, %s)",
            (row.category, row.title, row.price, row.urlItem, row.urlImage),
        )

    print("Data well uploaded to Heroku database!")

    connection.commit()


def join_to_csv():
    """
    This function joins ebay and categories tables into a single table using LEFT JOIN and exports to ebay_data.csv file

    Parameters:

    None

    Returns:

    ebay_data.csv file
    """

    # connecting to the database
    connection = psycopg2.connect(
        database="d8agtv34e8as8v",
        user="khrbktgjasltxt",
        password="ce6001a6731cda5f63778855fef76b54521d18fe8388bdf9ca41a61efccbdb3a",
        host="ec2-79-125-59-247.eu-west-1.compute.amazonaws.com",
        port="5432",
    )
    cur = connection.cursor()

    print("Tables are being joined..")

    # joining both tables into one
    cur.execute(
        "select categories.category, ebay.title, ebay.price, ebay.urlItem, ebay.urlImage from ebay LEFT JOIN categories on ebay.category = categories.id"
    )

    print("Tables have been successfully joined!")
    print("The joined table is being exported to csv format..")

    # exporting table into .csv file
    query = "select categories.category, ebay.title, ebay.price, ebay.urlItem, ebay.urlImage from ebay LEFT JOIN categories on ebay.category = categories.id"
    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
    with open("ebay_data.csv", "w", encoding="utf-8") as f:
        cur.copy_expert(outputquery, f)

    print("Table has been sucessfully exported")
