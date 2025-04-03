from opcua import Client, ua
import time
# import EventLogger2
from utils.logging_utils import app_event
import threading
from utils.db_utils import DatabaseConnection
from utils.formulas import calculator
from utils.json_utils import JSONDumper
from utils.json_utils import LOADdata
from datetime import datetime
class OPCUAClient:
    def __init__(self):
        self.server_address = "opc.tcp://192.168.1.2:4840"
        #self.server_address = server_address
        self.client = None
        self.all_data = []
        self.train_type=[]
        self.itr=0
        self.time_seconds=0
        self.totalnoof_axles=0
        self.trainend=None
        self.c1_sensor_values=None
        self.siterations=None
        self.loop1_event = threading.Event()  # Signals Loop 2 to start
        self.loop2_event = threading.Event()  # Signals Loop 1 to continue
        self.loop1_done = False  # Flag to stop both loops
        self.timestamped_data = None
    def connect(self):
        """Connect to the OPC UA server."""
        try:
            self.client = Client(self.server_address)
            self.client.connect()
            print(f"Connected to OPC UA server at {self.server_address}")
        except Exception as e:
            print(f"Failed to connect to OPC UA server: {e}")
            self.client = None
    def testitr(self):
        self.itr="12345"
    def disconnect(self):
        """Disconnect from the OPC UA server."""
        if self.client:
            self.client.disconnect()
            print("Disconnected from OPC UA server.")
        else:
            print("No active connection to disconnect.")

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
            app_event.info(value)
            #print(f"Train End Done {value} to NodeId '{node_id}' in namespace '{namespace_index}'.")
        except Exception as e:
            print(f"Error writing to the node: {e}")



    

    def ExCounter_For_C1_Sen(self, polling_interval=0.00001, timeout=30):
        """
        Continuously read a boolean value from a specific node and print updates when the value changes.
        Print "Logic Ready" only once when the condition is met, starting with the "Value has not changed" block.
        """
  
        node_id = 613  # Replace with the NodeId (integer value)
        namespace_index = 4

        if not self.client:
            print("Client is not connected. Cannot read from the node.")
            return

        last_value = None  # Initialize to None to detect the first read
        last_change_time = time.time() - timeout  # Force the first check into "no change" block
        logic_ready_printed = False  # Ensure "Logic Ready" is printed only once

        try:
            # Get the node using the provided NodeId and namespace index
            node = self.client.get_node(ua.NodeId(node_id, namespace_index))

            # Force the first read to trigger "no change" logic
            try:
                # Read the initial value of the node
                current_value = node.get_value()
                last_value = current_value  # Set the last value to the first read value
                print(f"Train Will End after {timeout} seconds. Current value: {current_value}")
                
                logic_ready_printed = True  # Mark "Logic Ready" as printed
            except Exception as e:
                print(f"Error during initial node read: {e}")
                return

            # Begin monitoring for changes
            while True:
                try:
                    # Read the current value from the node
                    current_value = node.get_value()

                    # Check if the value has changed
                    if current_value != last_value:
                        #print(f"Value changed: {current_value}")
                        if current_value>0:
                            TrainStart="TrainStart"
                            #OPCUAClient.write_TrainEnd_Tojson(TrainStart)
                        
                        #sys_event.info(f"Value changed: {current_value}")
                        #EventLogger2.sys_event.info("Value changed:: %s",current_value)
                        last_value = current_value  # Update the last known value
                        last_change_time = time.time()  # Reset the last change time
                        logic_ready_printed = False  # Reset "Logic Ready" flag for new timeout cycle
                        
                    # Check if the value hasn't changed for the timeout duration
                    if time.time() - last_change_time >= timeout and not logic_ready_printed:
                        print(f"Train Will End After {timeout} seconds. Current value: {current_value}")
                        if current_value!=0:
                            self.write_boolean_TrainEnd()
                            TrainEnd="TrainEnd"
                            #OPCUAClient.write_TrainEnd_Tojson(TrainEnd)
                        #sys_event.info(f"Value has not changed for {timeout} seconds. Current value: {current_value} - Logic Ready")
                        #EventLogger2.sys_event.info("Value has not changed: %s",current_value)
                        logic_ready_printed = True  # Mark "Logic Ready" as printed
                        
                    # Wait for the next polling interval
                    time.sleep(polling_interval)

                except Exception as e:
                    print(f"Error reading value during monitoring: {e}")
                    break

        except Exception as e:
            print(f"Error accessing the node: {e}")
    
    def Test_Bit_C1_Sen(self, polling_interval=2):

        fetch_query="fetchcoachnos"
        self.fetch_all_query(fetch_query)
        # Check if self.all_data is not empty
        if len(self.all_data) == 0:
            print("No elements in self.all_data. Cannot create radio buttons.")
        else:
            pass
            #print("test train else block")
            # Create a variable for radio buttons
            #self.temepvar = value=self.all_data[0]  # Set default value
        for idx, element in enumerate(self.all_data):
                pass
                #print(f"printtttttttttprintttttttt: {element}{idx}")  # Debugging print
        last_index = len(self.all_data) - 1
        last_element=len(element) -1
        #print(f"Last element index: {last_index}last ele:{element}")
        #############################################################
        calc=calculator()
        
        totalnoof_axles=calc.convert_coachto_axles(element)
        ############################################################
        #print("totalnoof_axles",totalnoof_axles)
        node_id = 607  # Replace with the NodeId (integer value)
        namespace_index = 4
        value = True  # Boolean value to write
        iterations = 0  # Counter for iterations
        self.totalnoof_axles=totalnoof_axles
        max_iterations = totalnoof_axles#10  # Maximum iterations to perform
        self.write_boolean_TrainStart()
        ################################################
        SProxy = self.Test_Bit_S_Sen
        
        SProxy_thread = threading.Thread(target=SProxy, daemon=True)
        SProxy_thread.start()
        ###########################################################
        
        if not self.client:
            print("Client is not connected. Cannot write to the node.")
            return

        try:
            
            while iterations < max_iterations :
                #time.sleep(5)
                #time.sleep(5)  # Simulate some processing in Loop 1
                # Increment the iteration counter at the start of each iteration
                iterations += 1
                self.loop1_event.set()  # Signal Loop 2 to start
                self.loop2_event.wait()  # Wait for Loop 2 to finish
                self.loop2_event.clear()  # Reset the event for the next iteration
                # Get the node using the provided NodeId and namespace index
                time.sleep(self.time_seconds)
                node = self.client.get_node(ua.NodeId(node_id, namespace_index))
                
                # Write True to the node
                value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                data_value = ua.DataValue(value_to_write)
                node.set_value(data_value)
                #print(f"Iteration {iterations}: Successfully wrote {value} to NodeId '{node_id}' in namespace '{namespace_index}'.")
                ################################################################
                fetch_query="fetchspeed"
                self.fetch_all_query(fetch_query)
                # Check if self.all_data is not empty
                if len(self.all_data) == 0:
                    print("No elements in self.all_data. Cannot create radio buttons.")
                else:
                    pass
                    #print("test train else block")
                    # Create a variable for radio buttons
                    #self.temepvar = value=self.all_data[0]  # Set default value
                for idx, element in enumerate(self.all_data):
                        pass
                        #print(f"seeeeeeeeeeeeeeeeeeeeeeeeeed: {element}{idx}")  # Debugging print
                last_index = len(self.all_data) - 1
                last_element=len(element) -1
                #print(f"Last element index: {last_index}last ele:{element}")
                #app_event.info(element)
                ################################################################
                try:
                    input_speed = int(float(element))
                except ValueError:
                    print(f"Invalid input: {element}")
                ################################################################
                
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
                    #print("icf")
                    distance_mm = 2800
                elif loadtrain_type == "LHB":
                    #print("lhb")
                    distance_mm = 2400
                elif loadtrain_type == "WAGON":
                    distance_mm = 1900
                else:
                    print("⚠️ Warning: Unknown train type:", loadtrain_type)
                    distance_mm = 0  # ✅ Assign a fallback value to prevent errors
                #print("ddddddddddiiiiiiiiiiiisssssssssssttttttttttttt",distance_mm)
                #app_event.info(f"distance_mm: {distance_mm}, loadtrain_type: {loadtrain_type}")
                app_event.info("loadtrain_type")
                app_event.info(loadtrain_type)
                app_event.info("distance_mm")
                app_event.info(distance_mm)
                
                calc = calculator()
                result = calc.get_time_for_coach_type(input_speed, distance_mm)  # Speed: 60 km/h, Distance: 2800 mm
                #print(result)
                app_event.info("result")
                app_event.info(result)
                coach_type = result['coach_type']
                distance_mm = result['distance_mm']
                speed_kmh = result['speed_kmh']
                time_microseconds = result['time_microseconds']
                time_seconds = result['time_seconds']
                ################################################################
                app_event.info("time_seconds")
                app_event.info(time_seconds)
                double_timefor_delay=time_seconds+time_seconds
                                                  ########################################
                self.time_seconds=0.777777777777778#time_seconds
                app_event.info(f"s: {self.time_seconds}")
                value = False
                value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                data_value = ua.DataValue(value_to_write)
                node.set_value(data_value)
                print(f"C1 Proxy Ping....{iterations}")
                ##################################################################
                self.timestamped_data=            {
                        "timestamp": datetime.now().isoformat()
                        
                    }
                app_event.info(self.timestamped_data)
                ##################################################################
                ###################################################################
                self.itr=iterations
                
                ####################################################################
                
                mapping = {i: i + 3 for i in range(1, 201)}

                # Print first 20 elements to verify
                #print(dict(list(mapping.items())[:20]))
                mapresults = mapping.get(iterations, iterations) 
                #print(f"iterations{mapresults}")
                self.get_C1_Sensor_values(mapresults)
                
                # Reset value and wait before the next iteration
                value = True
                
                
            #time.sleep(5)
            self.loop1_done = True  # Indicate Loop 1 is finished
            self.loop1_event.set()  # Ensure Loop 2 exits if waiting
        except Exception as e:
            print(f"Error writing to the node: {e}")

    def Test_Bit_S_Sen(self, polling_interval=1):
        #app_event.info(f"s: {self.time_seconds}")
        app_event.info(f"s: {self.totalnoof_axles}")
        node_id = 608  # Replace with the NodeId (integer value)
        namespace_index = 4
        value = True  # Boolean value to write
        iterations = 0  # Counter for iterations
        max_iterations = self.totalnoof_axles#10  # Maximum iterations to perform
        
        if not self.client:
            print("Client is not connected. Cannot write to the node.")
            return

        try:          
            
            while iterations < max_iterations and not self.loop1_done:
                

                
                # Increment the iteration counter at the start of each iteration
                iterations += 1
                self.loop1_event.wait()  # Wait for signal from Loop 1
                if self.loop1_done:  # Exit if Loop 1 is done
                    break
                #time.sleep(self.time_seconds)
                # Get the node using the provided NodeId and namespace index
                node = self.client.get_node(ua.NodeId(node_id, namespace_index))
                
                # Write True to the node
                value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                data_value = ua.DataValue(value_to_write)
                node.set_value(data_value)
                #print(f"Iteration {iterations}: Successfully wrote {value} to NodeId '{node_id}' in namespace '{namespace_index}'.")

                # Wait and toggle value
                #time.sleep(10)
                value = False
                value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                data_value = ua.DataValue(value_to_write)
                node.set_value(data_value)
                self.timestamped_data=            {
                        "timestamp": datetime.now().isoformat()
                        
                    }
                app_event.info(self.timestamped_data)
                #print(f"S Proxy Ping....{iterations}")
                self.siterations=iterations
                
                smapping = {i: i + 204 for i in range(1, 201)}
                #app_event.info(smapping)
                smapresults = smapping.get(iterations, iterations) 
                #print(f"iterations{smapresults}")

                self.get_S_Sensor_values(smapresults)
                # Reset value and wait before the next iteration
                value = True
                # time.sleep(2)
                #time.sleep(self.time_seconds)
                print(f"  Loop 2 - Running")
                # time.sleep(1.5)  # Simulate processing time
                
                self.loop1_event.clear()  # Reset the event
                #time.sleep(10)
                self.loop2_event.set()  # Signal Loop 1 to continue
            #time.sleep(2)
        except Exception as e:
            print(f"Error writing to the node: {e}")
    """
    def NoTrhread_Test_Bit_S_Sen(self, polling_interval=1):
        app_event.info(f"s: {self.time_seconds}")
        app_event.info(f"s: {self.totalnoof_axles}")
        node_id = 608  # Replace with the NodeId (integer value)
        namespace_index = 4
        value = True  # Boolean value to write
        iterations = 0  # Counter for iterations
        max_iterations = self.totalnoof_axles#10  # Maximum iterations to perform
        
        if not self.client:
            print("Client is not connected. Cannot write to the node.")
            return

        try:
            
                
            while iterations < max_iterations:
                # Increment the iteration counter at the start of each iteration
                iterations += 1

                # Get the node using the provided NodeId and namespace index
                node = self.client.get_node(ua.NodeId(node_id, namespace_index))
                
                # Write True to the node
                value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                data_value = ua.DataValue(value_to_write)
                node.set_value(data_value)
                #print(f"Iteration {iterations}: Successfully wrote {value} to NodeId '{node_id}' in namespace '{namespace_index}'.")

                # Wait and toggle value
                #time.sleep(1)
                value = False
                value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                data_value = ua.DataValue(value_to_write)
                node.set_value(data_value)
                print(f"S Proxy Ping....{iterations}")
                self.siterations=iterations
                # smapping = {
                #     1: 205,
                #     2: 206,
                #     3: 207,
                #     4: 208,
                #     5: 209,
                #     6: 210,                    
                #     7: 211,
                #     8: 212,
                #     9: 213,
                #     10: 214,

                # }
                smapping = {i: i + 204 for i in range(1, 201)}
                #app_event.info(smapping)
                smapresults = smapping.get(iterations, iterations) 
                #print(f"iterations{smapresults}")

                self.get_S_Sensor_values(smapresults)
                # Reset value and wait before the next iteration
                value = True
                #time.sleep(self.time_seconds)
        except Exception as e:
            print(f"Error writing to the node: {e}")
    """
    def get_C1_Sensor_values(self,mapresults):
        # time.sleep(1)
        #print(mapresults)
        # node=100
        # # OPC UA Server Configuration
        # server_url = "opc.tcp://192.168.1.2:4840"
        # node_ids = range(4, 204)  # Range of node IDs to receive data from
        #node_id = 5  # Replace with the NodeId (integer value)
        node_id=mapresults#iterations
        namespace_index = 4
        try:
            # Get the node using the provided NodeId and namespace index
            node = self.client.get_node(ua.NodeId(node_id, namespace_index))

            # Force the first read to trigger "no change" logic
            try:
                #time.sleep(0.000001)
                # Read the initial value of the node
                current_value = node.get_value()
                self.c1_sensor_values=current_value
                #print(f"current_reading C1 Proxy-  {current_value}")
                #self.write_json(current_value,self.itr)
                app_event.info(current_value)
            except Exception as e:
                print(f"Error during initial node read: {e}")
                return
        except Exception as e:
                    print(f"Error reading value during monitoring: {e}")
        
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
                app_event.info(current_value)
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
                    app_event.info(value)
                
                ##################################################
            except Exception as e:
                print(f"Error during initial node read: {e}")
                return
        except Exception as e:
                    print(f"Error reading value during monitoring: {e}")
        
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
                    #print("Database connection closed.")

# # Example Usage
# if __name__ == "__main__":
#     #server_address = "opc.tcp://192.168.1.2:4840"  # Replace with your server address
#     # # node_id = 616  # Replace with the NodeId (integer value)
#     # # namespace_index = 4
#     # # value = True  # Boolean value to write

#     opcua_client = OPCUAClient()
#     try:
#         opcua_client.connect()
#         opcua_client.write_boolean_TrainEnd()
#     finally:
#         opcua_client.disconnect()


# opcua_client = OPCUAClient()
# opcua_client.connect()
# opcua_client.Test_Bit_C1_Sen()



# opcua_client.Test_Bit_S_Sen()
#opcua_client.write_boolean_TrainEnd()


# if value is not None:
#     print(f"The current value of the node is: {value}")
# else:
#     print("Failed to read the node value.")