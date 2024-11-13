import time

def create_vehicle(vehicle_id, vehicle_type, balance=0):
    return {
        "vehicle_id": vehicle_id,
        "vehicle_type": vehicle_type,
        "balance": balance,
    }

def deduct_balance(vehicle, amount):
    if vehicle["balance"] >= amount:
        vehicle["balance"] -= amount
        return True
    else:
        return False

def calculate_toll(entry, exit, vehicle_type): #6 rute dan 4 rute putar balik
    toll_routes = {
        ("Kopo", "Toha"): {"car": 3.0, "truck": 6.0, "bus": 5.0},
        ("Kopo", "Buahbatu"): {"car": 4.0, "truck": 8.0, "bus": 6.5},
        ("Kopo", "Cileunyi"): {"car": 2.5, "truck": 5.0, "bus": 4.0},
        ("Toha", "Buahbatu"): {"car": 2.5, "truck": 5.0, "bus": 4.0},
        ("Toha", "Cileunyi"): {"car": 2.5, "truck": 5.0, "bus": 4.0},
        ("Buahbatu", "Cileunyi"): {"car": 2.5, "truck": 5.0, "bus": 4.0},
        
        ("Kopo", "Kopo"): {"car": 8, "truck":  , "bus":    },
        ("Toha", "Toha"): {"car": 8, "truck":  , "bus":    },
        ("Buahbatu", "Buahbatu"): {"car": 8, "truck":  , "bus":    },
        ("Cileunyi", "Cileunyi"): {"car": 8, "truck":  , "bus":    },
    }
    route = (entry, exit)
    if route in toll_routes:
        return toll_routes[route].get(vehicle_type,)
    else:
        route = (exit, entry)
        return toll_routes.get(route, {}).get(vehicle_type,)

def process_vehicle(vehicle, entry, exit):
    if vehicle["has_pass"]:
        print(f"Vehicle {vehicle['vehicle_id']} with a pass: Toll waived.")
        return True
    else:
        toll_amount = calculate_toll(entry, exit, vehicle["vehicle_type"])
        if deduct_balance(vehicle, toll_amount):
            print(f"Vehicle {vehicle['vehicle_id']} charged {toll_amount} for route {entry} to {exit}. Remaining balance: {vehicle['balance']}")
            return True
        else:
            print(f"Vehicle {vehicle['vehicle_id']} does not have enough balance for route {entry} to {exit}.")
            return False

def add_vehicle():
    vehicle_id = input("Enter vehicle ID: ")
    vehicle_type = input("Enter vehicle type (car, truck, motorcycle, bus): ").lower()
    balance = float(input("Enter vehicle balance: "))
    has_pass = input("Does the vehicle have a toll pass? (yes/no): ").strip().lower() == 'yes'
    return create_vehicle(vehicle_id, vehicle_type, balance, has_pass)

def main():
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
        print(f"\nProcessing vehicle {vehicle['vehicle_id']}...")
        entry = input(f"Enter entry gate for vehicle {vehicle['vehicle_id']} (e.g., A, B, C): ").strip().upper()
        exit = input(f"Enter exit gate for vehicle {vehicle['vehicle_id']} (e.g., A, B, C): ").strip().upper()
        process_vehicle(vehicle, entry, exit)
        time.sleep(1)  # Pause for readability

if __name__ == "__main__":
    main()
