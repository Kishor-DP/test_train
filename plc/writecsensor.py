from opcua import Client, ua
import time
from utils.db_utils import DatabaseConnection
from utils.json_utils import LOADdata
from utils.json_utils import JSONDumper
from utils.formulas import calculator
class OPCUAClient:
    def __init__(self, server_address="opc.tcp://192.168.1.2:4840"):
        self.server_address = server_address
        self.client = None
        self.c1_sensor_values=None
        self.itr=0
        self.siterations=0
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
    def get_coachnos_fromjson(self):
        loadclass = LOADdata()
        json_file = "data/save_preferences/preferences.json"  # Replace with your JSON file path
        data = loadclass.load_json(json_file)
        train_type = loadclass.get_value(data, "train_type")  # Replace with actual keys
        #value_iteration = loadclass.get_value(data, "iteration")
        #print("Value:", tikradio)
        #print("iterations",value_iteration)
        #print(f"Last element index: {last_index}input_speed{input_speed}last ele:{tikradio}")
        cleaned_coachnos = train_type.strip()
        loadtrain_chnos = cleaned_coachnos
        distance_mm = None  # ✅ Initialize distance_mm with a default value
        cleaned_coachnos = loadtrain_chnos.strip()
        return cleaned_coachnos
    
    def write_json(self,json_data):
        sample_data=json_data
        dumper = JSONDumper("data/output_text/output_text.json")
        #sample_data = {"sensor": "temperature", "value": 22.5}
        dumper.dump_with_timestamp(
            data=sample_data,
            c1value=self.c1_sensor_values, 
            iteration=self.itr,
            siterations=self.siterations,
            status="OK", 
            location="Pune"
        )

    def get_S_Sensor_values(self,smapresults):
        
        node_id=smapresults#iterations
        namespace_index = 4
        try:
            # Get the node using the provided NodeId and namespace index
            node = self.client.get_node(ua.NodeId(node_id, namespace_index))

            # Force the first read to trigger "no change" logic
            try:
                #time.sleep(1)
                # Read the initial value of the node
                current_value = node.get_value()
                
                #print(f"current_reading S Proxy-   {current_value}")
                self.write_json(f"SProxy: {current_value}")
                #app_event.info(current_value)
                ##################################################################3
                loadclass = LOADdata()
                json_file = "data/output_text/output_text.json" 
                
                data = loadclass.load_json(json_file)
                if data:
                    value = loadclass.get_value(data, "data")  # Replace with actual keys
                    
                
                if value!="TrainEnd.......Done":
                    pass
                    #self.write_json(f"SProxy: {current_value}", self.itr)
                if value =="TrainEnd.......Done":
                    self.write_json(value)
                    #app_event.info(value)
                
                ##################################################
            except Exception as e:
                print(f"Error during initial node read S: {e}")
                return
        except Exception as e:
                    print(f"Error reading value during monitoring: {e}")


    def write_boolean_TrainStart(self):
        """
        Write a boolean value to a specific node.
        
        :param node_id: The NodeId of the target node.
        :param namespace_index: The namespace index of the NodeId.
        :param value: Boolean value to write (True/False).
        """
        node_id = 829  # Replace with the NodeId (integer value)
        namespace_index = 4
        value = True  # Boolean value to write
        self.write_json(value)
        if not self.client:
            print("Client is not connected. Cannot write to the node.")
            return
        
        try:
            # Get the node using the provided NodeId and namespace index
            node = self.client.get_node(ua.NodeId(node_id, namespace_index))
            # Ensure the value being written is a Boolean
            value_to_write = ua.Variant(value, ua.VariantType.Boolean)
            data_value = ua.DataValue(value_to_write)
            node.set_value(data_value)
            

        except Exception as e:
            print(f"Error writing to the node: {e}")
                
    def write_boolean_TrainEnd(self):
        """
        Write a boolean value to a specific node.
        
        :param node_id: The NodeId of the target node.
        :param namespace_index: The namespace index of the NodeId.
        :param value: Boolean value to write (True/False).
        """
        node_id = 616  # Replace with the NodeId (integer value)
        namespace_index = 4
        value = True  # Boolean value to write
        if not self.client:
            print("Client is not connected. Cannot write to the node.")
            return
        
        try:
            # Get the node using the provided NodeId and namespace index
            node = self.client.get_node(ua.NodeId(node_id, namespace_index))
            # Ensure the value being written is a Boolean
            value_to_write = ua.Variant(value, ua.VariantType.Boolean)
            data_value = ua.DataValue(value_to_write)
            node.set_value(data_value)
            #time.sleep(10)
            value=False
            value_to_write = ua.Variant(value, ua.VariantType.Boolean)
            data_value = ua.DataValue(value_to_write)
            node.set_value(data_value)
            print("TrainEnd.......Done")
            value="TrainEnd.......Done"
            self.trainend=value
            self.write_json(value)
            #app_event.info(value)
            #print(f"Train End Done {value} to NodeId '{node_id}' in namespace '{namespace_index}'.")
        except Exception as e:
            print(f"Error writing to the node: {e}")

    def write_c_sensor(self):
        chno=self.get_coachnos_fromjson()
        print("ccccccccccccooooooooooooaaaaaaaaaachnos",chno)
        chnos=int(chno)
        calc=calculator()
        
        totalnoof_axles=calc.convert_coachto_axles(chnos)
        print("toooooooooootaaaaaaaaaalNNNNNNNNNNoof axles",totalnoof_axles)
        #########################################################
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
        iterations = 0 
        max_iterations = totalnoof_axles#int(chno)#chno#20#self.totalnoof_axles
        self.write_boolean_TrainStart()
        print("write_boolean_TrainStart")
        try:
            nodec = self.client.get_node(ua.NodeId(node_idc, namespace_index))
            nodes = self.client.get_node(ua.NodeId(node_ids, namespace_index))
            print(f"Accessing Node: {node_idc} in Namespace {namespace_index}")

            while iterations < max_iterations:
                iterations += 1
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
                smapping = {i: i + 204 for i in range(1, 201)}
                #app_event.info(smapping)
                smapresults = smapping.get(iterations, iterations) 
                self.get_S_Sensor_values(smapresults)
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
                    print("iterations............................",iterations)
                    self.itr=iterations
                    if max_iterations==iterations:
                        self.write_boolean_TrainEnd()
                        print("write train end in plc")
                        print("loooooooooooop..............break on provided chnos")
                        break
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
