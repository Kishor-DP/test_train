import pyodbc
import time
from typing import Any, List, Tuple, Optional
import json

class DatabaseConnection:
    def __init__(self, max_retries: int = 3, retry_delay: int = 2):
        """
        Initialize the database connection.
        :param max_retries: Maximum retry attempts for connection
        :param retry_delay: Delay in seconds between retries
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.connection = None

    def db_configuration(self):
        """Load database connection string from JSON file."""
        with open("config/db_config.json", "r") as dbconfig:
            connection_string = json.load(dbconfig)
            return connection_string['connection_string']
        
    def check_connection(self) -> bool:
        """
        Check if the database connection is active.
        :return: True if the connection is active, False otherwise.
        """
        if self.connection is None:
            #print("Database connection is not established.")
            return False

        try:
            # Execute a simple query to check the connection
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()

            if result:
                #print("Database connection is active.")
                return True
            else:
                print("Database connection check failed: No result from query.")
                return False

        except pyodbc.Error as e:
            print(f"Database connection check failed: {e}")
            return False
        
    def connect(self) -> None:
        """Establish a connection with retry logic."""
        attempt = 0
        while attempt < self.max_retries:
            try:
                connection_string = self.db_configuration()
                self.connection = pyodbc.connect(connection_string)
                #print("Database connection established successfully.")
                return
            except pyodbc.Error as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                attempt += 1
                time.sleep(self.retry_delay)
        raise Exception("Failed to connect to the database after multiple attempts.")

    def execute_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple]:
        """Execute a query and return results."""
        if self.connection is None:
            raise Exception("Database connection is not established.")
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            return []
        except pyodbc.Error as e:
            print(f"Query execution failed: {e}")
            return []
        finally:
            cursor.close()
            #print("cursor closed db")
            #comment execute_query can perform all operations insert update delete methods enable insert update delete methods if needed.
    """
    def insert(self, table: str, columns: List[str], values: Tuple[Any, ...]) -> None:
        
        # Insert a new record into the specified table.
        # :param table: Name of the table
        # :param columns: List of column names
        # :param values: Tuple of values to insert
        
        columns_str = ', '.join(columns)
        placeholders = ', '.join('?' * len(values))
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        self.execute_query(query, values)
        self.connection.commit()
        print("Record inserted successfully.")

    def update(self, table: str, set_columns: List[str], set_values: Tuple[Any, ...], where_condition: str, where_values: Tuple[Any, ...]) -> None:
        #
        # Update records in the specified table.
        # :param table: Name of the table
        # :param set_columns: List of columns to update
        # :param set_values: Tuple of new values
        # :param where_condition: WHERE clause condition
        # :param where_values: Tuple of values for the WHERE clause
        # 
        set_clause = ', '.join([f"{col} = ?" for col in set_columns])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_condition}"
        self.execute_query(query, set_values + where_values)
        self.connection.commit()
        print("Record(s) updated successfully.")

    def delete(self, table: str, where_condition: str, where_values: Tuple[Any, ...]) -> None:
        
        # Delete records from the specified table.
        # :param table: Name of the table
        # :param where_condition: WHERE clause condition
        # :param where_values: Tuple of values for the WHERE clause
        
        query = f"DELETE FROM {table} WHERE {where_condition}"
        self.execute_query(query, where_values)
        self.connection.commit()
        print("Record(s) deleted successfully.")
"""
    def close(self) -> None:
        #Close the database connection.
        if self.connection:
            self.connection.close()
            #print("Database connection closed.")
            self.connection = None
    
# Example usage:
# if __name__ == "__main__":
#     db = DatabaseConnection()
#     try:
#         db.connect()
        
#         # Insert example
#         db.insert("dbo.mvis_videotimingtbl", ["trainid", "class"], ("value1", "value2"))
        
#         # Update example
#         db.update("dbo.mvis_videotimingtbl", ["trainid"], ("class",), "class = ?", ("value2",))
        
#         # Delete example
#         db.delete("dbo.mvis_videotimingtbl", "trainid = ?", ("value1",))
        
#         # Select example
#         result = db.execute_query("SELECT * FROM dbo.mvis_videotimingtbl")
#         print(result)
        
#     finally:
#         db.close()