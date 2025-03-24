import json
from datetime import datetime

class json_files_manager:
    def __init__(self):
        pass
    def file_paths(self):
        with open ("config/file_path.json","r") as file_p:
            file_paths=json.load(file_p)
            model_path=file_paths['model_path']
            video_path=file_paths['video_path']
            output_path=file_paths['output_path']
            bogieview_input_video_path=file_paths['bogieview_input_video_path']
            output_frames=file_paths['output_frames']
            return model_path,video_path,output_path,bogieview_input_video_path,output_frames
    
    def db_config(self):
        pass

    def get_trainid(self):
        with open("C://data_video_processingapp/TrainId.json", "r")as trainidfile:
            loadfile=json.load(trainidfile)
            _get_trainid=loadfile['TrainId']
            return _get_trainid
        
class JSONDumper:
    def __init__(self, filename="data.json"):
        self.filename = filename

    def dump_with_timestamp(self, **data):
        """Dumps JSON data with a timestamp and multiple keys."""
        timestamped_data = {
            "timestamp": datetime.now().isoformat(),
            **data  # Merging multiple key-value pairs
        }

        with open(self.filename, "w") as file:
            json.dump(timestamped_data, file, indent=4)

        #print(f"Data successfully written to {self.filename}")

class LOADdata:
    def __init__(self):
        pass
    def load_json(self, file_path):
        """
        Load JSON data from a file.
        :param file_path: Path to the JSON file.
        :return: Dictionary containing JSON data.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON: {e}")
            return None

    def get_value(self, json_data, *keys):
        """
        Retrieve a value from a nested JSON dictionary using keys.
        :param json_data: JSON dictionary.
        :param keys: Sequence of keys to traverse the JSON structure.
        :return: Value if found, else None.
        """
        try:
            for key in keys:
                json_data = json_data[key]
            return json_data
        except (KeyError, TypeError):
            return None

# Example usage
# if __name__ == "__main__":
#     loadclass = LOADdata()
#     json_file = "data/output_text/output_text.json"  # Replace with your JSON file path
#     data = loadclass.load_json(json_file)
    
#     if data:
#         value = loadclass.get_value(data, "data")  # Replace with actual keys
#         print("Value:", value)
