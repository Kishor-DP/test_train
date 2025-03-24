db_management.py

Database Management Module

Overview

The db_management.py module is a database management utility designed to handle database connections, execute queries, and perform basic CRUD (Create, Read, Update, Delete) operations. It includes automatic retry logic for connection attempts and can be used across different modules within a project.

Features

*Establishes and maintains a connection with retry logic.

*Checks if the database connection is active.

*Executes queries from anywhere within the folder structure.

*Supports insert, update, and delete operations.

*Loads database connection details from a JSON configuration file.

*Closes the database connection after query execution.

Installation

pip install pyodbc
--------------------------------------------------------------------------------------
Configuration

The module requires a JSON configuration file located at config/db_config.json with the following structure:

{
  "connection_string": "DRIVER={SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_username;PWD=your_password"
}


------------------------------------------------------------------------------------
Methods

db_configuration()

Loads the database connection string from config/db_config.json.

check_connection()

Checks whether the database connection is active.

connect()

Attempts to establish a database connection with retry logic.

execute_query(query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple]

Executes a SQL query and returns results if applicable.

close()

Closes the database connection.
---------------------------------------------------------------------------------
Example Usage:
---------------------------------------------------------------------------------
from utils.db_management import DatabaseConnection

class testinsert:
       
    def insert_query(self,values_placeholder):
                db = DatabaseConnection()
                try:
                    db.connect()
                    print("Database connection established successfully.")
                    
                    if db.check_connection():
                        print("Database connection is active before query execution.")
                        
                        insert_query = """
                        INSERT INTO dbo.mvis_videotimingtbl ([trainid], [class], [total_video_time])
                        VALUES (?, ?, ?)
                        """

                        db.execute_query(insert_query, values_placeholder)
                        db.connection.commit()
                        print("Record inserted successfully.")
                        db.close()
                        if db.check_connection():
                            print("Database connection is still active after query execution.")
                        else:
                            print("Database connection became inactive after query execution.")

                    else:
                        print("Database connection is not active before executing the query.")

                except Exception as e:
                    print("Error:", str(e))

                finally:
                    db.close()
                    print("Database connection closed.")
value1="1"
value2="2"
value3="3"

values_placeholder=value1,value2,value3
inser=testinsert()
inser.insert_query(values_placeholder)


--------------------------------------------------------------------------
Additional CRUD Operations (Optional)

If uncommented in db_management.py, the following methods can be used:

insert(table: str, columns: List[str], values: Tuple[Any, ...])

Inserts a new record into the specified table.

update(table: str, set_columns: List[str], set_values: Tuple[Any, ...], where_condition: str, where_values: Tuple[Any, ...])

Updates existing records based on the given condition.

delete(table: str, where_condition: str, where_values: Tuple[Any, ...])

Deletes records from the specified table.
--------------------------------------------------------------------------

Notes

Ensure the config/db_config.json file is correctly set up.

Always close the connection using close() after executing queries to prevent connection leaks.

Use exception handling while executing queries to catch potential errors.



fetch and insert used in modules:


def fetch_query(self,trainid):
        db = DatabaseConnection()
        try:
            db.connect()
            print("Database connection established successfully.")
            
            if db.check_connection():
                print("Database connection is active before query execution.")
                
                fetch_query = """
                SELECT [trainid], [class_name], [total_video_time], [new_coach_timestamp], [system_timestamp], [time_difference] FROM [dbo].[mvis_videotimingtbl] WHERE TrainId = ?;
                """

                result=db.execute_query(fetch_query,(trainid,))
                db.connection.commit()
                print("Records fetched successfully.")
                # Initialize a set to keep track of seen timestamps
                if not hasattr(self, 'seen_timestamps'):
                    self.seen_timestamps = set()
                
                # Print results and append only new entries
                for row in result:
                    new_coach_timestamp = row[3]
                    if new_coach_timestamp not in self.seen_timestamps:
                        print(new_coach_timestamp)
                        self.fetched_new_coach_timestamp.append(new_coach_timestamp)
                        self.seen_timestamps.add(new_coach_timestamp)
                        self.fetchedrows = row
                db.close()
                if db.check_connection():
                    print("Database connection is still active after query execution.")
                else:
                    print("Database connection became inactive after query execution.")

            else:
                print("Database connection is not active before executing the query.")
            return 
        except Exception as e:
            print("Error:", str(e))

        finally:
            db.close()
            print("Database connection closed.")

    def insert_query(self,values_placeholder):
                db = DatabaseConnection()
                try:
                    db.connect()
                    print("Database connection established successfully.")
                    
                    if db.check_connection():
                        print("Database connection is active before query execution.")
                        
                        insert_query = """
                        INSERT INTO dbo.mvis_videotimingtbl ([trainid], [class_name], [total_video_time],[new_coach_timestamp],[system_timestamp])
                        VALUES (?, ?, ?,?,?)
                        """

                        db.execute_query(insert_query, values_placeholder)
                        db.connection.commit()
                        print("Record inserted successfully.")
                        db.close()
                        if db.check_connection():
                            print("Database connection is still active after query execution.")
                        else:
                            print("Database connection became inactive after query execution.")

                    else:
                        print("Database connection is not active before executing the query.")

                except Exception as e:
                    print("Error:", str(e))

                finally:
                    db.close()
                    print("Database connection closed.")