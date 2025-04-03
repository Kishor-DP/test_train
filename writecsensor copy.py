from opcua import Client, ua
import time  # Import missing module

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

    def write_c_sensor(self):
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
                for value in [True, False]:  # Toggle values
                    value_to_write = ua.Variant(value, ua.VariantType.Boolean)
                    data_value = ua.DataValue(value_to_write)
                    nodec.set_value(data_value)
                    #time.sleep(1)
                    nodes.set_value(data_value)
                    print(f"Successfully wrote {value} to NodeId '{node_idc}' in namespace '{namespace_index}'.")

                    time.sleep(0)  # Wait for 5 seconds before toggling
        except Exception as e:
            print(f"Error writing value: {e}")

if __name__ == "__main__":
    opc = OPCUAClient()
    opc.connect()
    opc.write_c_sensor()
    opc.disconnect()
