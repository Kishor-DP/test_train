from utils.logging_utils import app_event
class calculator:
    def __init__(self):
        pass
    
    def convert_coachto_axles(self,elements):
        num_int = int(elements)
        axles=num_int*4
        #print("elements:",elements)
        #print(f"Axles: {axles}")
        return axles
    
    def calculate_time_microseconds(self, speed, initial_distance):
        #initial_distance=14.5
        if speed == 0:
            return "Speed cannot be zero"
        
        # Convert speed from km/h to m/s
        speed_mps = speed * (5 / 18)  # km/h to m/s

        # Calculate time in seconds
        time_seconds = initial_distance / speed_mps

        # Convert time to microseconds
        time_microseconds = time_seconds * 1_000_000  # Convert seconds to µs
        seconds=time_microseconds/1000000
       
        return time_microseconds,seconds  # Returns time in microseconds
    def get_time_for_coach_type(self, speed, distance_mm):
        # Determine coach type based on distance range
        if 2700 <= distance_mm <= 3300:
            self.coach_type = "ICF"
        
        elif 2350 <= distance_mm <= 2699:
            self.coach_type = "LHB"
        elif 1800 <= distance_mm <= 2349:
            self.coach_type = "WAGON"
        else:
            self.coach_type = "UNKNOWN"
        # Convert distance from millimeters to meters
        initial_distance = distance_mm / 1000  #  meters
        app_event.info("initial_distance")
        app_event.info(initial_distance)
        # Calculate time for the given distance
        time_microseconds, time_seconds = self.calculate_time_microseconds(speed, initial_distance)

        return {
            "coach_type": self.coach_type,
            "distance_mm": distance_mm,
            "speed_kmh": speed,
            "time_microseconds": time_microseconds,
            "time_seconds": time_seconds
        }
    
    def xyz(self):
        timestamp2=180397000
        timestamp1=822567000
        speed_kmph1=1
        time_diff = abs((timestamp2 - timestamp1).total_seconds())
        distance_m = speed_kmph1 / 3.6 * time_diff
        distance_mm = distance_m * 1000  # Convert meters to millimeters
        app_event.info("distance_mm")
        app_event.info(distance_m)
        app_event.info(distance_mm)
        
        print(f"Distance between Axle {distance_m} and Axle {distance_m}: {distance_mm:.2f} millimeters")
# Example usage
#calculator = calculator()
# result = calculator.get_time_for_coach_type(60, 2800)  # Speed: 60 km/h, Distance: 2800 mm
# print(result)
# calculator = calculator()
# time_taken_us, time_taken_s = calculator.calculate_time_microseconds(70, 14.5)  # Speed in km/h, Distance in meters

# # Proper print formatting
# print(f"Time taken: ({time_taken_us:.2f}microsec) µs ({time_taken_s:.6f} s)")
#calculator.xyz()