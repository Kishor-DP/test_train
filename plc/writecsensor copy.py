from opcua import Client, ua
import time
from utils.db_utils import DatabaseConnection
from utils.json_utils import LOADdata

class OPCUAClient:
    def __init__(self, server_address="opc.tcp://192.168.1.2:4840"):
        self.server_address = server_address
        self.client = None

    def connect(self):
        """Connect to the OPC UA server."""
        try:
            self.client = Client(self.server_address)
            self.client.connect()
            print(f"Connected to OPC UA server at {self.server_address}")
        except Exception as e:
            print(f"Failed to connect to OPC UA server: {e}")
            self.client = None

    def disconnect(self):
        """Disconnect from the OPC UA server."""
        if self.client:
            self.client.disconnect()
            print("Disconnected from OPC UA server.")
        else:
            print("No active connection to disconnect.")

    def get_train_type_fromjson(self):
        loadclass = LOADdata()
        json_file = "data/save_preferences/preferences.json"  # Replace with your JSON file path
        data = loadclass.load_json(json_file)
        tikradio = loadclass.get_value(data, "tik_radio")  # Replace with actual keys
        #value_iteration = loadclass.get_value(data, "iteration")
        #print("Value:", tikradio)
        #print("iterations",value_iteration)
        #print(f"Last element index: {last_index}input_speed{input_speed}last ele:{tikradio}")
        cleaned_train_type = tikradio.strip()
        loadtrain_type = cleaned_train_type
        distance_mm = None  # ✅ Initialize distance_mm with a default value
        cleaned_train_type = loadtrain_type.strip()
        if loadtrain_type == "ICF":
            print("icf")
            distance_mm = 2800
        elif loadtrain_type == "LHB":
            print("lhb")
            distance_mm = 2400
        elif loadtrain_type == "WAGON":
            print("wagon")
            distance_mm = 1900
        else:
            print("⚠️ Warning: Unknown train type:", loadtrain_type)
            distance_mm = 0  # ✅ Assign a fallback value to prevent errors
        return loadtrain_type
    
    def write_c_sensor(self):
        ttype=self.get_train_type_fromjson()
        print("ttype:",ttype)
        if ttype=="ICF":
            c_s_timegap=3.605256
        elif ttype=="WAGON":
            c_s_timegap=5.117475
        elif ttype=="LHB":
            c_s_timegap=4.2
        else:
            print("ttype unknown")

            c_s_timegap==1.0
        """Write alternating boolean values to a specified OPC UA node."""
        if not self.client:
            print("Client is not connected. Cannot write to the node.")
            return

        node_idc = 607  # Replace with the correct NodeId
        node_ids = 608
        namespace_index = 4  # Replace with the correct NamespaceIndex

        try:
            nodec = self.client.get_node(ua.NodeId(node_idc, namespace_index))
            nodes = self.client.get_node(ua.NodeId(node_ids, namespace_index))
            print(f"Accessing Node: {node_idc} in Namespace {namespace_index}")

            while True:
                for _ in range(2):  # Iterate exactly 2 times
                    value = True
                    value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                    data_value = ua.DataValue(value_to_write)
                    
                    nodec.set_value(data_value)
                    print(f"Successfully wrote {value} to NodeId '{nodec.nodeid.Identifier}' in Namespace '{nodec.nodeid.NamespaceIndex}'.")

                    time.sleep(0)  # Sleep to mimic delay

                    value = False
                    value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                    data_value = ua.DataValue(value_to_write)
                    
                    nodec.set_value(data_value)
                    print(f"Successfully wrote {value} to NodeId '{nodec.nodeid.Identifier}' in Namespace '{nodec.nodeid.NamespaceIndex}'.")

                    time.sleep(0.6)  # Sleep to mimic delay
                # value=False
                # #for value in [True, False]:  # Toggle values
                # value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                # data_value = ua.DataValue(value_to_write)
                
                # nodec.set_value(data_value)
                    

                # print(f"Successfully wrote {value} to NodeId '{nodec.nodeid.Identifier}' in Namespace '{nodec.nodeid.NamespaceIndex}'.")
                # value=True
                # #for value in [True, False]:  # Toggle values
                # value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                # data_value = ua.DataValue(value_to_write)
                
                # nodec.set_value(data_value)
                print("c_s_timegap:",c_s_timegap)
                time.sleep(c_s_timegap)
                for _ in range(2):
                    value = True
                    value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                    data_value = ua.DataValue(value_to_write)
                    
                    nodes.set_value(data_value)
                    print(f"Successfully wrote {value} to NodeId s_sensor'{nodes.nodeid.Identifier}' in Namespace '{nodec.nodeid.NamespaceIndex}'.")

                    time.sleep(0)  # Sleep to mimic delay

                    value = False
                    value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                    data_value = ua.DataValue(value_to_write)
                    
                    nodes.set_value(data_value)
                    print(f"Successfully wrote {value} to NodeId s_sensor '{nodes.nodeid.Identifier}' in Namespace '{nodec.nodeid.NamespaceIndex}'.")
                    time.sleep(0.6)
                    
                    # # Toggle nodes twice
                    # nodes.set_value(data_value)
                    # print(f"Successfully wrote {value} to NodeId '{nodes.nodeid.Identifier}' in Namespace '{nodes.nodeid.NamespaceIndex}'.")
                    # time.sleep(0.3)
                    # nodes.set_value(ua.DataValue(ua.Variant(not value, ua.VariantType.Boolean)))  # Toggle
                    # print(f"Toggled to {not value} for NodeId '{nodes.nodeid.Identifier}'.")

                    #time.sleep(5)  # Corrected sleep time
        except Exception as e:
            print(f"Error writing value: {e}")
    def fetch_all_query(self,fetch_query):
        #print("fetch_query",fetch_query)
        
        
        if fetch_query=="fetchspeed":
            db = DatabaseConnection()
            try:
                db.connect()
                #print("Database connection established successfully.")
                
                if db.check_connection():
                    #print("Database connection is active before query execution.")
                    
                    fetch_query = """
                    SELECT [id], [speed_km/h] FROM [dbo].[test_train_userinput];
                    """
                    
                    result = db.execute_query(fetch_query)
                    db.connection.commit()
                    #print("Records fetched successfully.", result)

                    # Initialize self.all_data if not already done
                    if not hasattr(self, 'all_data'):
                        self.all_data = []

                    # Extract and store column 2 (coaches)
                    for row in result:
                        coaches_value = row[1]  # Assuming 'coaches' is at index 2
                        self.all_data.append(coaches_value)

                    #print("Updated self.all_data:", self.all_data)

                    db.close()
                    if db.check_connection():
                        print("Database connection is still active after query execution.")
                    else:
                        pass
                        #print("Database connection became inactive after query execution.")

                else:
                    print("Database connection is not active before executing the query.")
                
                return 

            except Exception as e:
                print("Error:", str(e))


            finally:
                db.close()
                #print("Database connection closed.")
        if fetch_query=="fetchcoachnos":
            db = DatabaseConnection()
            try:
                db.connect()
                #print("Database connection established successfully.")
                
                if db.check_connection():
                    #print("Database connection is active before query execution.")
                    
                    fetch_query = """
                    SELECT [id], [coachnos] FROM [dbo].[test_train_userinput];
                    """
                    
                    result = db.execute_query(fetch_query)
                    db.connection.commit()
                    #print("Records fetched successfully.", result)

                    # Initialize self.all_data if not already done
                    if not hasattr(self, 'all_data'):
                        self.all_data = []

                    # Extract and store column 2 (coaches)
                    for row in result:
                        coaches_value = row[1]  # Assuming 'coaches' is at index 2
                        self.all_data.append(coaches_value)

                    #print("Updated self.all_data:", self.all_data)

                    db.close()
                    if db.check_connection():
                        print("Database connection is still active after query execution.")
                    else:
                        pass
                        #print("Database connection became inactive after query execution.")

                else:
                    print("Database connection is not active before executing the query.")
                
                return 

            except Exception as e:
                print("Error:", str(e))


            finally:
                db.close()
                #print("Database connection closed.")
        if fetch_query=="fetchtrain_type":
                db = DatabaseConnection()
                try:
                    db.connect()
                    #print("Database connection established successfully.")
                    
                    if db.check_connection():
                        #print("Database connection is active before query execution.")
                        
                        fetch_query = """
                        SELECT [id], [train_type] FROM [dbo].[test_train];
                        """
                        
                        result = db.execute_query(fetch_query)
                        db.connection.commit()
                        #print("Records fetched successfully.", result)

                        # Initialize self.all_data if not already done
                        if not hasattr(self, 'self.train_type'):
                            self.train_type = []

                        # Extract and store column 2 (coaches)
                        for row in result:
                            coaches_value = row[1]  # Assuming 'coaches' is at index 2
                            self.train_type.append(coaches_value)

                        #print("Updated self.all_data:", self.train_type)

                        db.close()
                        if db.check_connection():
                            print("Database connection is still active after query execution.")
                        else:
                            pass
                            #print("Database connection became inactive after query execution.")

                    else:
                        print("Database connection is not active before executing the query.")
                    
                    return 

                except Exception as e:
                    print("Error:", str(e))


                finally:
                    db.close()
# if __name__ == "__main__":
#     opc = OPCUAClient()
#     opc.connect()
#     opc.write_c_sensor()
#     opc.disconnect()
