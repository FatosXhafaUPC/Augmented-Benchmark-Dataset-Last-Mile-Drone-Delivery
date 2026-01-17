import math

class EnergyModel:
    def __init__(self, drone_weight_kg=2.0, battery_capacity_joules=500000):
        """
        Physics-based Energy Model for a Quadcopter.
        Default values based on standard delivery drones (e.g., DJI Matrice).
        """
        self.W = drone_weight_kg  # Empty drone weight (kg)
        self.Q_max = battery_capacity_joules # Total battery capacity (J)
        
        # Physics Constants (Standard Atmosphere & Drag)
        self.g = 9.81           # Gravity (m/s^2)
        self.rho = 1.225        # Air density (kg/m^3)
        self.area = 0.5         # Frontal area (m^2) - Approx
        
        # Aerodynamic Drag Coefficients (k1, k2 typical for quadrotors)
        self.k1 = 0.85 
        self.k2 = 0.30 

    def get_power_consumption(self, total_mass_kg, airspeed_ms):
        """
        Calculates Power (Watts) required to fly at a specific AIRSPEED.
        Formula approximates the non-linear power curve of a rotorcraft.
        """
        # 1. Induced Power (Lift) - Dominates at low speed
        # P_i = (Force^1.5) / sqrt(2 * rho * Area)
        force_N = total_mass_kg * self.g
        p_induced = (self.k1 * force_N**1.5) / math.sqrt(2 * self.rho * self.area)

        # 2. Parasitic Power (Drag) - Dominates at high speed
        # P_p = 0.5 * rho * v^3 * Area * Cd
        p_parasitic = self.k2 * 0.5 * self.rho * (airspeed_ms**3) * self.area

        return p_induced + p_parasitic

    def calculate_arc_energy(self, distance_m, ground_speed_ms, wind_speed_ms, payload_kg):
        """
        Calculates total Energy (Joules) to traverse an arc.
        Takes into account the wind vector acting on the drone.
        """
        # Effective Airspeed = Ground Speed - Wind Speed (Simplified head/tail wind model)
        # If wind is positive (tailwind), airspeed decreases (less energy).
        # If wind is negative (headwind), airspeed increases (more energy).
        # We assume worst-case (headwind) or average for conservative planning if direction unknown.
        
        # For the MILP robust model, we assume wind opposes motion (Headwind)
        # to ensure the drone has enough battery.
        effective_airspeed = ground_speed_ms + abs(wind_speed_ms) 
        
        # Total Mass
        total_mass = self.W + payload_kg
        
        # Power (Watts)
        power_watts = self.get_power_consumption(total_mass, effective_airspeed)
        
        # Time (seconds) = Distance / Ground Speed
        time_seconds = distance_m / ground_speed_ms
        
        # Energy (Joules) = Power * Time
        energy_joules = power_watts * time_seconds
        
        return energy_joules

# --- Quick Test ---
if __name__ == "__main__":
    model = EnergyModel()
    
    dist = 1000  # 1 km
    speed = 10   # 10 m/s
    wind = 5     # 5 m/s headwind
    payload = 2.0 # 2 kg package
    
    e_cost = model.calculate_arc_energy(dist, speed, wind, payload)
    
    print(f"--- Energy Calculation Test ---")
    print(f"Distance: {dist} m | Speed: {speed} m/s | Wind: {wind} m/s")
    print(f"Payload: {payload} kg")
    print(f"Energy Cost: {e_cost:.2f} Joules")
    print(f"Battery % Used: {(e_cost / model.Q_max)*100:.2f}%")