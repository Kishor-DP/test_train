from utils.logging_utils import app_event
from datetime import datetime, timedelta
import pyodbc
from json.decoder import JSONDecodeError
import json
import logging
import time
import math
import re
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
        timestamp1="7   0  29  19  602330000"
        #modified_timestamp = re.sub(r'\s+', ' ', timestamp1).replace(" ,", ",").replace(", ", ",")

        #print(modified_timestamp)
        #timestamp2="30  22  18  0  907000000"

        ############################################################
        #speed_kmph = 240.028


        timestamp2 = '7   0  29  20  289635000'#self.calculate_timestamp2(speed_kmph)
        #print("Calculated timestamp2:", timestamp2)
        ############################################################
        
        timestamp_c1 = self.convert_to_datetime(timestamp1)
        #app_event.info("timestamp_c1111111111111111111111111")
        #app_event.info(timestamp_c1)
        #timestamp2='7   0  29  19  602330000'
        timestamp_c1_2 = self.convert_to_datetime(timestamp2)
        time_diff = abs((timestamp_c1_2 - timestamp_c1).total_seconds())
        print("C proxy time differece",time_diff)
        #app_event.info("time_diff")
        app_event.info(time_diff)
        if time_diff > 0:
            self.initial_distance=14.50
            speed_mps = self.initial_distance / time_diff
            speed_kmph = speed_mps * 3.6
            #print("c proxy speed: time_diff,speed_mps,speed_kmph",time_diff,speed_mps,speed_kmph)
            #self.speed_mps=speed_mps
        else:
            speed_kmph = 0
        c1_timestamp="7   0  29  19  384855000"
        s1_timestamp="7   0  29  23  384855000"
        speed=calculator.calculate_speed(c1_timestamp,s1_timestamp)
        print("S proxy time differece:",speed)
        speed_kmph1=speed#-220#240.028#speed_kmph#speed_mps
        # time_diff = abs((timestamp_s1 - timestamp_c1).total_seconds())
        # app_event.info("time_diff")
        # app_event.info(time_diff)
        #print("-speed",speed_kmph1)
        distance_m = speed_kmph1 / 3.6 * time_diff
        #distance_m=18.35977559577404
        distance_mm = distance_m * 1000  # Convert meters to millimeters
        app_event.info("distance_mm")
        app_event.info(distance_m)
        app_event.info(distance_mm)
        
        print(f"Distance between Axle C1 and Axle C1:{distance_m}mtr {distance_mm:.2f} millimeters")

    
    def convert_to_datetime(self, timestamp):
        try:
            # Clean the timestamp by removing commas and multiple spaces
            cleaned_timestamp = " ".join(timestamp.replace(",", "").split())
            #print(cleaned_timestamp)
            parts = cleaned_timestamp.split()
            if len(parts) < 5:
                print(f"Invalid timestamp format: {timestamp}")
                return None
            
            hours = int(parts[1])
            minutes = int(parts[2])
            seconds = int(parts[3])
            nanoseconds = int(parts[4]) 
            #nanoseconds = int(parts[6])
            #milisec= int(parts[6])
            #combined=int(nanoseconds + milisec)
            
            #print("h",hours,"m",minutes,"sec",seconds,"nanosec",nanoseconds)
            reference_date = datetime(2000, 1, 1)
            converted_date = reference_date + timedelta(
                hours=hours, minutes=minutes, seconds=seconds, microseconds=nanoseconds // 1000
            )

            return converted_date

        except (ValueError, IndexError) as e:
            print(f"Error converting timestamp: {timestamp}. Exception: {e}")
            return None
    def calculate_timestamp2(self,speed_kmph):
        distance_m = 15.60
        # Convert speed from km/h to m/s
        speed_mps = speed_kmph * (1000 / 3600)

        # Calculate time difference in seconds
        time_diff = distance_m / speed_mps

        # Assume a reference timestamp1
        timestamp1_str = "30  22  17  59  000000000"
        
        # Convert to datetime format
        timestamp1_parts = list(map(int, timestamp1_str.split()))
        reference_date = datetime(2000, 1, timestamp1_parts[0], 
                                timestamp1_parts[1], timestamp1_parts[2], 
                                timestamp1_parts[3], timestamp1_parts[4] // 1000)
        
        # Add time difference
        timestamp2 = reference_date + timedelta(seconds=time_diff)

        # Extract new timestamp values
        day = timestamp2.day
        hour = timestamp2.hour
        minute = timestamp2.minute
        second = timestamp2.second
        nanoseconds = timestamp2.microsecond * 1000  # Convert microseconds to nanoseconds

        # Format the final timestamp2
        timestamp2_str = f"{day}  {hour}  {minute}  {second}  {nanoseconds}"
        
        return timestamp2_str

    def calculate_speed(self,c1_timestamp,s1_timestamp):
        speeds = []
        previous_speed = None
        # c1_timestamp="7   0  29  19  384855000"
        # s1_timestamp="7   0  29  19  602330000"
        timestamp_c1 = self.convert_to_datetime(c1_timestamp)
        timestamp_s1 = self.convert_to_datetime(s1_timestamp)

        if timestamp_c1 is not None and timestamp_s1 is not None:
            time_diff = abs((timestamp_s1 - timestamp_c1).total_seconds())
            print(f"c and s time diff:{time_diff}")
            if time_diff > 0:
                speed_mps = self.initial_distance / time_diff
                speed_kmph = speed_mps * 3.6
            else:
                speed_kmph = 0

            # Check if the speed difference is within 30% compared to the previous speed
            if previous_speed is not None:
                diff_percentage = abs(speed_kmph - previous_speed) / previous_speed * 100

                if diff_percentage > 30:
                    corrected_axle_speed = previous_speed  # Use previous speed if difference is greater than 30%
                else:
                    corrected_axle_speed = speed_kmph  # Use current speed if within 30%
            else:
                corrected_axle_speed = speed_kmph  # For the first speed, use current speed as corrected

            # Update previous speed for next comparison
            previous_speed = corrected_axle_speed

            speeds.append((timestamp_c1, corrected_axle_speed))
            #print(f"Speed for Axle corrected_axle_speed: {corrected_axle_speed:.2f} km/h")
            speed_result = f"Speed for Axle : {speed_kmph:.2f} km/h"
            print(speed_result)
            return speed_kmph
# Example usage
calculator = calculator()
#result = calculator.get_time_for_coach_type(60, 12.60)  # Speed: 60 km/h, Distance: 2800 mm
#print(result)
# calculator = calculator()
# time_taken_us, time_taken_s = calculator.calculate_time_microseconds(70, 14.5)  # Speed in km/h, Distance in meters

# # Proper print formatting
# print(f"Time taken: ({time_taken_us:.2f}microsec) µs ({time_taken_s:.6f} s)")
calculator.xyz()

# Given speed of 50 km/h
# speed_kmph = 20


# timestamp2_result = calculator.calculate_timestamp2(speed_kmph)
# print("Calculated timestamp2:", timestamp2_result)
