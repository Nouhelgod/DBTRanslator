import pymssql
import logging
import sqlite3

class Connection():

    def __init__(self, host: str, username: str, password: str, database: str, port: str= '1433') -> None:
        """
        Initializes a new instance of the class.

        Args:
            host (str): The hostname or IP address of the database server.
            username (str): The username to use for the database connection.
            password (str): The password to use for the database connection.
            database (str): The name of the database to connect to.
            port (str): The port number to use for the database connection.

        Returns:
            None
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

        self.connection: pymssql.Connection = None
        self.cursor: pymssql.Cursor = None


    def __try_connection(self) -> bool:
        """
        Tests the connection to the SQL Server database.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """

        logging.debug('Trying to connect')
        try:
            self.connection = pymssql.connect(
                server=self.host, 
                port=self.port, 
                user=self.username, 
                password=self.password,
                database=self.database
                )
            logging.debug(f'{self.connection}')
            return True

        except (Exception, pymssql.Error) as e:
            logging.error(f"Error while connecting to SQL Server: {e}")
            return False


    def getProductsWithSameTranslation(self) -> pymssql.Cursor | None:
        """
        Retrieves product data from the 'Goods' table in the database where the 'Name2' field is equal to the 'Name' field.

        This function executes a SQL query to retrieve all data from the 'Goods' table where the 'Name2' field is equal to the 'Name' field.

        Returns:
            pymssql.Cursor | None: A cursor object containing the product data, or None if the cursor is not set.
        """
        query = "select * from Goods where Name2 = Name"

        if not self.cursor:
            logging.error(f'No cursor. {self.cursor=}')
            return None

        self.cursor.execute(query)
        return self.cursor


    def getProductData(self) -> pymssql.Cursor | None:
        """
        Retrieves product data from the 'Goods' table in the database.

        Returns:
            pymssql.Cursor | None: A cursor object containing the product data, or None if the cursor is not set.
        """
        if not self.cursor:
            logging.error(f'No cursor. {self.cursor=}')
            return 

        sql_str = f"SELECT BarCode1, Name, Name2 FROM Goods"
        self.cursor.execute(sql_str)
        return self.cursor

    
    def getEmptyProducts(self) -> pymssql.Cursor | None:
        """
        Retrieves product data from the 'Goods' table in the database where the 'Name2' field is empty.

        Returns:
            pymssql.Cursor | None: A cursor object containing the product data, or None if the cursor is not set.
        """
        if not self.cursor:
            logging.error(f'No cursor. {self.cursor=}')
            return 

        sql_str = f"SELECT BarCode1, Name FROM Goods WHERE Name2 = ''"
        self.cursor.execute(sql_str)
        return self.cursor

    
    def getTopProducts(self) -> pymssql.Cursor | None:
        """ 
        Retrieves top 100 product data from the 'Goods' table in the database.

        Returns:
            pymssql.Cursor | None: A cursor object containing the product data, or None if the cursor is not set.
        """
        if not self.cursor:
            logging.error(f'No cursor. {self.cursor=}')
            return 

        sql_str = f"SELECT TOP 100 BarCode1, Name FROM Goods"
        self.cursor.execute(sql_str)
        return self.cursor


    def connect(self) -> bool:
        """
        Establishes a connection to the database.

        This method attempts to establish a connection to the database using the provided connection details.
        If the connection is successful, it initializes a cursor object and executes a query to retrieve the
        database version. The version is then stored in the `db_version` attribute.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """

        if self.__try_connection():
            self.cursor = self.connection.cursor()
            self.cursor.execute('select @@VERSION')
            self.db_version = str(self.cursor.fetchone()[0])
            logging.info(f'Database version: {self.db_version}')
            return True

        return False


class Local():
    def __init__(self) -> None:
        self.connection = sqlite3.connect('local.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.__initDatabase()


    def __initDatabase(self) -> None:
        """
        Initializes the 'Goods' table in the local database.

        This function creates a new table named 'Goods' in the local database if it does not already exist.
        The table has three columns: 'barcode1' (text), 'name' (text), and 'name2' (text).

        Raises:
            Exception: If there is an error creating the table.
        """
        try:
            query = "create table if not exists Goods(barcode1 text, name text, name2 text)"
            self.cursor.execute(query)
            logging.info(f'Created local table')

        except Exception as e:
            logging.error(f'Error while creating table: {e}')


    def dropAndCreateTable(self) -> bool:
        """
        Drops the 'Goods' table from the local database and recreates it.

        This function drops the 'Goods' table from the local database if it exists,
        and then calls the `__initDatabase` function to recreate it.

        Returns:
            bool: True if the table is successfully dropped and recreated, False otherwise.
        """
        try:
            self.cursor.execute("drop table if exists Goods")
            self.__initDatabase()
            return True
        
        except Exception as e:
            logging.error(f'Error while dropping and creating table: {e}')
            return False


    def getProductData(self) -> sqlite3.Cursor | None:
        """
        Retrieves product data from the 'Goods' table in the local database.

        This function executes a SQL query to retrieve all data from the 'Goods' table.

        Returns:
            sqlite3.Cursor | None: A cursor object containing the product data, or None if there is an error.
        """
        try:
            query = "select * from Goods"
            self.cursor.execute(query)
            
            return self.cursor

        except Exception as e:
            logging.error(f'Error while getting data: {e}')

    
    def updateName(self, code: str, name: str) -> bool:
        """
        Updates the name of a product in the 'Goods' table.

        This function executes a SQL query to update the name of a product in the 'Goods' table.
        The product is identified by its barcode1 (code) and the new name is specified by the 'name' parameter.

        Args:
            code (str): The barcode1 of the product to update.
            name (str): The new name to set for the product.

        Returns:
            bool: True if the name was successfully updated, False otherwise.

        Raises:
            Exception: If there is an error executing the SQL query.
        """
        try:
            query = "update Goods set name = ? where barcode1 = ?"
            params = [name, code]

            self.cursor.execute(query, params)
            self.connection.commit()

            return True

        except Exception as e:
            logging.error(f'Error while updating data: {e}')

            return False


    def updateTranslation(self, code: str, translation: str) -> bool:
        """
        Updates the translation of a product in the 'Goods' table.

        This function executes a SQL query to update the translation of a product in the 'Goods' table.
        The product is identified by its barcode1 (code) and the new translation is specified by the 'translation' parameter.

        Args:
            code (str): The barcode1 of the product to update.
            translation (str): The new translation to set for the product.

        Returns:
            bool: True if the translation was successfully updated, False otherwise.

        Raises:
            Exception: If there is an error executing the SQL query.
        """
        try:
            query = "update Goods set name2 = ? where barcode1 = ?"
            params = [translation, code]

            self.cursor.execute(query, params)
            self.connection.commit()

            return True

        except Exception as e:
            logging.error(f'Error while updating data: {e}')

            return False

    
    def addProduct(self, code: str, name: str, translation: str) -> bool:
        """
        Adds a new product to the 'Goods' table in the local database.

        This function executes an SQL query to add a new product to the 'Goods' table in the local database.
        The product is identified by its barcode1 (code), name, and translation.

        Args:
            code (str): The barcode1 of the product to add.
            name (str): The name of the product to add.
            translation (str): The translation of the product to add.

        Returns:
            bool: True if the product was successfully added, False otherwise.

        Raises:
            Exception: If there is an error executing the SQL query.
        """
        try:
            logging.info(f'{self.cursor=}, {code=}, {name=}, {translation=}')

            if self.__checkSameProduct(code):
                return False

            query = "insert into Goods values (?, ?, ?)"
            params = [code, name, translation]

            self.cursor.execute(query, params)
            self.connection.commit()

            return True

        except Exception as e:
            logging.error(f'Error while adding product: {e}')

            return False

    
    def getExactProduct(self, barcode1: str) -> list | None:
        """
        Retrieves product data from the 'Goods' table in the local database based on barcode1.

        This function executes a SQL query to retrieve product data from the 'Goods' table in the local database.
        The product is identified by its barcode1 (barcode1).

        Args:
            barcode1 (str): The barcode1 of the product to retrieve.

        Returns:
            list | None: A list containing the product data, or None if the product is not found.

        Raises:
            Exception: If there is an error executing the SQL query.
        """
        try:
            query = "select * from Goods where barcode1 = ?"
            params = [barcode1]

            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        
        except Exception as e:
            logging.error(f'Error while getting exact product: {e}')

            return None


    def __checkSameProduct(self, code: str) -> bool | None:
        """
        Checks if a product with the given barcode1 exists in the 'Goods' table.

        This function executes a SQL query to check if a product with the given barcode1 exists in the 'Goods' table.

        Args:
            code (str): The barcode1 of the product to check.

        Returns:
            bool: True if the product exists, False otherwise.
            None: If there is an error executing the SQL query.
        """
        try:
            query = "select * from Goods where barcode1 = ?"
            params = [code]

            self.cursor.execute(query, params)

            logging.debug(f'{self.cursor.fetchone()=}')
            if code in self.cursor:
                return True

            else:
                return False

        except Exception as e:
            logging.error(f'Error while checking same product: {e}')
            
            return None


    def compareAndFetch(self, barcode: str) -> list | None:
        """
        Retrieves product data from the 'Goods' table in the local database based on barcode1.

        This function executes a SQL query to retrieve product data from the 'Goods' table in the local database.
        The product is identified by its barcode1 (barcode).

        Args:
            barcode (str): The barcode1 of the product to retrieve.

        Returns:
            list | None: A list containing the product data, or None if the product is not found.

        Raises:
            Exception: If there is an error executing the SQL query.
        """
        try:
            query = "select * from Goods where barcode1 = ?"
            params = [barcode]

            self.cursor.execute(query, params)
            prod = self.cursor.fetchone()

            if prod[1] != '':
                return prod

            else:
                return None
        
        except Exception as e:
            logging.error(f'Error while comparing and delivering: {e}')

            return None


if __name__ == '__main__':
    import os

    host = os.environ['DB_HOST']
    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    database = os.environ['DB_DATABASE']
    
    con = Connection(host, user, password, database)
    con.connect()
    version = con.db_version
    print(version)