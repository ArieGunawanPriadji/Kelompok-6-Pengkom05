import time

class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, balance=0, has_pass=False):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.balance = balance
        self.has_pass = has_pass

    def deduct_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False

class TollGate:
    def __init__(self):
        # Define toll rates based on entry and exit points
        self.toll_routes = {
            ("B","A"): {"car": 3.0, "truck": 6.0, "motorcycle": 1.5, "bus": 5.0},
            ("A", "C"): {"car": 4.0, "truck": 8.0, "motorcycle": 2.0, "bus": 6.5},
            ("B", "C"): {"car": 2.5, "truck": 5.0, "motorcycle": 1.0, "bus": 4.0},
            ("A","A"): {"car": 8 }
        }

    def calculate_toll(self, entry, exit, vehicle_type):
        route = (entry, exit)
        if route in self.toll_routes:
            return self.toll_routes[route].get(vehicle_type, 5.0)  # Default toll rate if type unknown
        else :
            route= (exit, entry)
            return self.toll_routes[route].get(vehicle_type, 5.0)

    def process_vehicle(self, vehicle, entry, exit):
        if vehicle.has_pass:
            print(f"Vehicle {vehicle.vehicle_id} with a pass: Toll waived.")
            return True
        else:
            toll_amount = self.calculate_toll(entry, exit, vehicle.vehicle_type)
            if vehicle.deduct_balance(toll_amount):
                print(f"Vehicle {vehicle.vehicle_id} charged {toll_amount} for route {entry} to {exit}. Remaining balance: {vehicle.balance}")
                return True
            else:
                print(f"Vehicle {vehicle.vehicle_id} does not have enough balance for route {entry} to {exit}.")
                return False

def add_vehicle():
    vehicle_id = input("Enter vehicle ID: ")
    vehicle_type = input("Enter vehicle type (car, truck, motorcycle, bus): ").lower()
    balance = float(input("Enter vehicle balance: "))
    has_pass = input("Does the vehicle have a toll pass? (yes/no): ").strip().lower() == 'yes'
    return Vehicle(vehicle_id, vehicle_type, balance, has_pass)

def main():
    toll_gate = TollGate()
    vehicle_db = []

    # Add vehicles to the system
    while True:
        add_another = input("Do you want to add a new vehicle? (yes/no): ").strip().lower()
        if add_another == 'yes':
            vehicle = add_vehicle()
            vehicle_db.append(vehicle)
        else:
            break

    # Process each vehicle through the toll gate with entry and exit points
    for vehicle in vehicle_db:
        print(f"\nProcessing vehicle {vehicle.vehicle_id}...")
        entry = input(f"Enter entry gate for vehicle {vehicle.vehicle_id} (e.g., A, B, C): ").strip().upper()
        exit = input(f"Enter exit gate for vehicle {vehicle.vehicle_id} (e.g., A, B, C): ").strip().upper()
        toll_gate.process_vehicle(vehicle, entry, exit)
        time.sleep(1)  # Pause for readability

if __name__ == "__main__":
    main()
