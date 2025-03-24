import tkinter as tk
from tkinter import ttk
import threading
import time
import json
import logging
# from tkinter import Toplevel
from utils.common_utils import ToolTip
from utils.styles import styles
from plc.TestTrain import OPCUAClient 
from utils.db_utils import DatabaseConnection
from utils.json_utils import LOADdata
from utils.formulas import calculator



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log"
)

# Tooltip class
# class ToolTip:
#     def __init__(self, widget, text):
#         self.widget = widget
#         self.text = text
#         self.tooltip = None
#         self.widget.bind("<Enter>", self.show_tooltip)
#         self.widget.bind("<Leave>", self.hide_tooltip)

#     def show_tooltip(self, event=None):
#         x, y, _, _ = self.widget.bbox("insert")
#         x += self.widget.winfo_rootx() + 25
#         y += self.widget.winfo_rooty() + 25

#         self.tooltip = Toplevel(self.widget)
#         self.tooltip.wm_overrideredirect(True)
#         self.tooltip.wm_geometry(f"+{x}+{y}")

#         label = ttk.Label(self.tooltip, text=self.text, background="#FFFFE0", relief="solid", borderwidth=1)
#         label.pack()

#     def hide_tooltip(self, event=None):
#         if self.tooltip:
#             self.tooltip.destroy()
#             self.tooltip = None

# Main application class
class ModernUIApp:
    def __init__(self, root):
        self.total_values=None
        self.root = root
        self.root.title("TestTrain UI")
        self.root.geometry("1024x720")
        self.root.configure(bg='#2E3440')
        self.all_data=[]
        self.fetchedrows=None
        # Configure styles
        # self.theme_var = tk.StringVar(value="dark")
        style=styles()
        style.configure_styles()
        self.configure_styles=style.configure_styles()
        self.theme_var=style.theme_var
        # Create a main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Add a label
        #self.label = ttk.Label(self.main_frame, text="Welcome to Novius Test System UI")
        self.label = ttk.Label(self.main_frame, text="Enter Train Speed into km/h")
        self.label.grid(row=0, column=0, pady=10, sticky="w")

        # Add an entry widget
        self.entry = ttk.Entry(self.main_frame,width=15)
        self.entry.grid(row=1, column=0, pady=10, sticky="w")
        self.entry.bind("<KeyRelease>", self.on_entry_change)
        ToolTip(self.entry, "Enter Train Speed into km/h here.")
        ##############################################################
        self.label = ttk.Label(self.main_frame, text="Enter Coach nos.")
        self.label.grid(row=2, column=0, pady=10, sticky="w")
        # Add an entry widget
        self.entrycoach = ttk.Entry(self.main_frame,width=15)
        self.entrycoach.grid(row=3, column=0, pady=5, sticky="w")
        self.entrycoach.bind("<KeyRelease>", self.on_entry_change)
        ToolTip(self.entrycoach, "Enter Coach nos. here")
        # Add a dropdown for Tik options (1 to 5)
        # self.tik_label = ttk.Label(self.main_frame, text="Select (Dropdown):")
        # self.tik_label.grid(row=2, column=0, pady=5, sticky="w")
        # self.tik_options = [str(i) for i in range(1, 6)]  # Options: 1 to 5
        # self.tik_dropdown = ttk.Combobox(self.main_frame, values=self.tik_options, state="readonly")
        # self.tik_dropdown.current(0)  # Set default selection to the first option
        # self.tik_dropdown.grid(row=3, column=0, pady=5, sticky="ew")
        # ToolTip(self.tik_dropdown, "Select a Tik option from the dropdown.")

        # Add radio buttons for Tik options (1 to 5)
        self.radio_label = ttk.Label(self.main_frame, text="Select (Train Type):")
        self.radio_label.grid(row=4, column=0, pady=5, sticky="w")
        self.tik_var = tk.StringVar(value="1")  # Default selection
        # Ensure self.all_data has values
        self.fetch_all_query()
        #print("All Data:", self.all_data)

        # Check if self.all_data is not empty
        if len(self.all_data) == 0:
            print("No elements in self.all_data. Cannot create radio buttons.")
        else:
            # Create a variable for radio buttons
            self.tik_var = tk.StringVar(value=self.all_data[0])  # Set default value

            # Loop through self.all_data and create radio buttons
            for idx, element in enumerate(self.all_data):
                #print(f"Creating radio button: {element}")  # Debugging print
                ttk.Radiobutton(self.main_frame, text=element, variable=self.tik_var, value=element).grid(row=5+idx, column=0, sticky="w")
        # Add checkboxes for Tik options (1 to 5)
        # self.checkbox_label = ttk.Label(self.main_frame, text="Select Tik (Checkboxes):")
        # self.checkbox_label.grid(row=11, column=0, pady=5, sticky="w")
        # self.tik_check_vars = [tk.BooleanVar() for _ in range(5)]  # BooleanVars for checkboxes
        # for i in range(5):
        #     ttk.Checkbutton(self.main_frame, text=f"Tik {i+1}", variable=self.tik_check_vars[i]).grid(row=12+i, column=0, sticky="w")

        # Add a button
        self.button = ttk.Button(self.main_frame, text="Start Test", command=self.on_button_click)
        self.button.grid(row=11, column=0, pady=20)
        ToolTip(self.button, "Click to process the selected options.")

        # Add a progress bar (initially hidden)
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=12, column=0, pady=20)
        self.progress.grid_remove()  # Hide initially

        # Add an output label
        self.output_label = ttk.Label(self.main_frame, text="", wraplength=400)
        self.output_label.grid(row=13, column=0, pady=10)

        # Add a save button
        self.save_button = ttk.Button(self.main_frame, text="Save Preferences", command=self.save_preferences)
        self.save_button.grid(row=24, column=0, pady=10)

        # Add a theme toggle button
        self.theme_button = ttk.Checkbutton(self.main_frame, text="Toggle Theme", variable=self.theme_var, onvalue="light", offvalue="dark", command=self.toggle_theme)
        self.theme_button.grid(row=25, column=0, pady=10)

        # Load preferences on startup
        self.load_preferences()

    # # Configure styles
    # def configure_styles(self):
    #     style = ttk.Style()
    #     style.theme_use('clam')  # Use the 'clam' theme as a base

    #     if self.theme_var.get() == "dark":
    #         self.apply_dark_theme(style)
    #     else:
    #         self.apply_light_theme(style)

    # def apply_dark_theme(self, style):
    #     style.configure('TFrame', background='#2E3440')
    #     style.configure('TLabel', background='#2E3440', foreground='#D8DEE9', font=('Helvetica', 12))
    #     style.configure('TButton', background='#4C566A', foreground='#D8DEE9', font=('Helvetica', 12), borderwidth=1)
    #     style.map('TButton', background=[('active', '#5E81AC')])
    #     style.configure('TEntry', fieldbackground='#3B4252', foreground='#D8DEE9', font=('Helvetica', 12))
    #     style.configure('TCombobox', fieldbackground='#3B4252', foreground='#D8DEE9', font=('Helvetica', 12))
    #     style.map('TCombobox', fieldbackground=[('readonly', '#3B4252')])
    #     style.configure('TRadiobutton', background='#2E3440', foreground='#D8DEE9', font=('Helvetica', 12))
    #     style.configure('TCheckbutton', background='#2E3440', foreground='#D8DEE9', font=('Helvetica', 12))
    #     style.configure('Horizontal.TProgressbar', background='#5E81AC', troughcolor='#3B4252', thickness=20)

    # def apply_light_theme(self, style):
    #     style.configure('TFrame', background='#FFFFFF')
    #     style.configure('TLabel', background='#FFFFFF', foreground='#000000', font=('Helvetica', 12))
    #     style.configure('TButton', background='#E0E0E0', foreground='#000000', font=('Helvetica', 12), borderwidth=1)
    #     style.map('TButton', background=[('active', '#0078D7')])
    #     style.configure('TEntry', fieldbackground='#F0F0F0', foreground='#000000', font=('Helvetica', 12))
    #     style.configure('TCombobox', fieldbackground='#F0F0F0', foreground='#000000', font=('Helvetica', 12))
    #     style.map('TCombobox', fieldbackground=[('readonly', '#F0F0F0')])
    #     style.configure('TRadiobutton', background='#FFFFFF', foreground='#000000', font=('Helvetica', 12))
    #     style.configure('TCheckbutton', background='#FFFFFF', foreground='#000000', font=('Helvetica', 12))
    #     style.configure('Horizontal.TProgressbar', background='#0078D7', troughcolor='#E0E0E0', thickness=20)
    def fetch_query(self,train_type):
        db = DatabaseConnection()
        try:
            db.connect()
            print("Database connection established successfully.")
            #print("traintype",train_type)
            if db.check_connection():
                print("Database connection is active before query execution.")
                
                fetch_query = """
                SELECT [id], [train_type], [coaches], [speed_km/h] FROM [dbo].[test_train] WHERE [train_type] = ?;
                """

                result=db.execute_query(fetch_query,(train_type,))
                db.connection.commit()
                #print("Records fetched successfully.",result)
                # Initialize a set to keep track of seen timestamps
                if not hasattr(self, 'seen_timestamps'):
                    self.seen_timestamps = set()
                
                # Print results and append only new entries
                for row in result:
                    new_coach_timestamp = row[3]
                    if new_coach_timestamp not in self.seen_timestamps:
                        #print(new_coach_timestamp)
                        
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
    def fetch_all_query(self):
        db = DatabaseConnection()
        try:
            db.connect()
            print("Database connection established successfully.")
            
            if db.check_connection():
                print("Database connection is active before query execution.")
                
                fetch_query = """
                SELECT [id], [train_type], [coaches], [speed_km/h] FROM [dbo].[test_train];
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
                    print("Database connection became inactive after query execution.")

            else:
                print("Database connection is not active before executing the query.")
            
            return 

        except Exception as e:
            print("Error:", str(e))

        finally:
            db.close()
            print("Database connection closed.")

    def insert_query(self,param):
                db = DatabaseConnection()
                try:
                    db.connect()
                    print("Database connection established successfully.")
                    
                    if db.check_connection():
                        print("Database connection is active before query execution.")
                        #print(param)
                        insert_query = """
                        INSERT INTO [dbo].[test_train_userinput] ([speed_km/h],[coachnos])
                        VALUES (?,?)
                        """

                        db.execute_query(insert_query, (param))
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
                    print("Error insert:", str(e))

                finally:
                    db.close()
                    print("Database connection closed.")

    def plc_program(self):
        opcua_client = OPCUAClient()
        opcua_client.connect()
        opcua_client.Test_Bit_C1_Sen()
        
    def plc_program_trainend(self):
        opcua_client = OPCUAClient()
        opcua_client.connect()
        TrainEnd = opcua_client.ExCounter_For_C1_Sen
        print("Initializing TrainEnd thread")
        train_end_thread = threading.Thread(target=TrainEnd, daemon=True)
        train_end_thread.start()
    # Button click event handler
    def on_button_click(self):
        # Show the progress bar and start animation
        self.progress.grid()
        self.progress["value"] = 0
        #self.progress.config(maximum=100)
        self.plc_program_trainend()
        # Disable the button to prevent multiple clicks
        self.button.config(state=tk.DISABLED)
        self.save_preferences()
        # self.plc_program()
        # Start a thread to simulate processing
        threading.Thread(target=self.process_data).start()
        # Get selected values
        user_input = self.entry.get()
        if not user_input:
            raise ValueError("Please enter a value in the text field.")
        threading.Thread(target=self.plc_program).start()
        
    # Simulate processing and update UI
    def process_data(self):
        try:
            logging.info("Processing started.")
            # for i in range(101):  # Simulate progress from 0% to 100%
            #     time.sleep(0.03)  # Simulate work being done
            #     self.progress["value"] = i
            #     self.root.update_idletasks()  # Update the UI
##############################################################################
            # total_values = 34#  # Total number of values
            # for i in range(1, total_values + 1):  # Loop from 1 to 34
            #     percentage = (i / total_values) * 100  # Convert value to percentage
            #     self.progress["value"] = percentage
            #     self.root.update_idletasks()  # Update UI
            #     time.sleep(0.1)  # Simulate processing time
                    #################################################################3
            # Get selected values
            user_input = self.entry.get()
            if not user_input:
                raise ValueError("Please enter a value in the text field.")

            coachtypevalue = self.entrycoach.get()
            tik_radio_value = self.tik_var.get()
            #tik_check_values = [f"Tik {i+1}" for i, var in enumerate(self.tik_check_vars) if var.get()]
            #######################################################################
            loadclass = LOADdata()
            json_file = "data/output_text/output_text.json"  # Replace with your JSON file path
            
            # data = loadclass.load_json(json_file)
            
            # if data:
            #     value = loadclass.get_value(data, "data")  # Replace with actual keys
            #     print("Value:", value)
            #######################################################################
            #value=1
            # previous_value = None
            # change_counter = -2
            while True:
                data = loadclass.load_json(json_file)
                
                if data:
                    value = loadclass.get_value(data, "data")  # Replace with actual keys
                    value_iteration = loadclass.get_value(data, "iteration")
                    #print("Value:", value)
                    #print("iterations",value_iteration)
                    ####################################################333
                    # if value != previous_value:  # Check if value has changed
                    #     change_counter += 1
                    #     print(f"Value changed to: {value}, Change Count: {change_counter}")
                    #     previous_value = value  # Update previous value
                    #self.progress["value"] = change_counter
                    self.progress["value"] = value_iteration
                    # if change_counter == 1 or change_counter == 2:
                    #     print("1")
                    # else:
                        
                    #     self.progress["value"] = change_counter
                    coachtypevalue
                    calc=calculator()
        
                    totalnoof_axles=calc.convert_coachto_axles(coachtypevalue)
                    self.progress.config(maximum=totalnoof_axles)
                    self.root.update_idletasks()
                    if value_iteration==0 and value=="TrainEnd.......Done":
                        self.button.config(state=tk.NORMAL)
                        totalnoof_axles=calc.convert_coachto_axles(coachtypevalue)
                        self.progress.config(maximum=totalnoof_axles)
                    #    change_counter=-2
                        #previous_value=None
                    # if change_counter==-2 and value=="TrainEnd.......Done":
                    #     self.button.config(state=tk.NORMAL)
                    #     totalnoof_axles=calc.convert_coachto_axles(coachtypevalue)
                    #     self.progress.config(maximum=totalnoof_axles)
                    #     change_counter=-2
                # total_values = 34  # Total number of values
                # for i in range(1, total_values + 1):  # Loop from 1 to 34
                #     percentage = (i / total_values) * 100  # Convert value to percentage
                #     self.progress["value"] = percentage
                #     self.root.update_idletasks()  # Update UI
                #     time.sleep(0.1)  # Simulate processing time
                    ######################################################
                #value +=1
                # Update the output label
                output_text = (
                    f"Wait for train to end if started {value_iteration}\n"
                    f"Train Pass Progress {value}\n"
                    f"speed of train is {user_input}\n"
                    
                    f"coachnos: {coachtypevalue}\n"
                    f"totalnoof_axles: {totalnoof_axles}\n"
                    f"train type is: {tik_radio_value}\n"
                    #f"Checkboxe is: {', '.join(tik_check_values)}"
                )
                #print(f"cls.itr",{value})
                self.output_label.config(text=output_text, foreground="#D8DEE9")

                logging.info("Processing completed successfully.")
                
        except Exception as e:
            self.output_label.config(text=f"Error: {str(e)}", foreground="#BF616A")
            logging.error(f"Error during processing: {str(e)}")
        finally:
            # Stop the progress bar and hide it
            self.progress.grid_remove()

            # Re-enable the button
            self.button.config(state=tk.NORMAL)

    # Save preferences to a file
    def save_preferences(self):
        
        preferences = {
            "speed_km/h": self.entry.get(),
            "train_type": self.entrycoach.get(),
            "tik_radio": self.tik_var.get(),
            #"tik_checks": [var.get() for var in self.tik_check_vars]
        }
        speed_km_h=self.entry.get()
        coachnos=self.entrycoach.get()
        param=(speed_km_h,coachnos)
        self.insert_query(param)
        with open("data/save_preferences/preferences.json", "w") as f:
            json.dump(preferences, f)
        logging.info("Preferences saved.")

    # Load preferences from a file
    def load_preferences(self):
        try:
            with open("preferences.json", "r") as f:
                preferences = json.load(f)
                self.entry.insert(0, preferences["user_input"])
                self.entrycoach.set(preferences["tik_dropdown"])
                self.tik_var.set(preferences["tik_radio"])
                # for i, var in enumerate(self.tik_check_vars):
                #     var.set(preferences["tik_checks"][i])
            logging.info("Preferences loaded.")
        except FileNotFoundError:
            logging.info("No preferences file found.")

    # Toggle between dark and light themes
    def toggle_theme(self):
        self.configure_styles()

    # Enable/disable button based on entry input
    def on_entry_change(self, event=None):
        if self.entry.get().strip():
            self.button.config(state=tk.NORMAL)
        else:
            self.button.config(state=tk.DISABLED)

# Run the application
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ModernUIApp(root)
#     root.mainloop()