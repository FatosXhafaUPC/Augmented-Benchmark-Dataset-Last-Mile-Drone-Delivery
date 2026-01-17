import math
import sys
import os

# Import your parser from the scripts folder
from scripts.data_utils import parse_augmented_instance

class MILPInstance:
    def __init__(self, file_path, wind_scenario='RAYLEIGH'):
        """
        Reads the augmented data and builds the Mathematical Sets & Parameters.
        wind_scenario: 'RAYLEIGH' or 'UNIFORM' (Selects which wind column to use)
        """
        # Ensure file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Instance file not found: {file_path}")

        self.meta, self.raw_nodes = parse_augmented_instance(file_path)
        self.wind_scenario = wind_scenario
        
        # Initialize Data Structures
        self.Sets = {}
        self.Params = {}
        
        self._build_sets()
        self._build_parameters()

    def _build_sets(self):
        """
        Defines sets: N (Nodes), C (Customers), K (Drones), A (Arcs)
        """
        # 1. Nodes (N): Index 0 is Depot Start, Index 11 is Depot End.
        self.Sets['N'] = [n['#Node'] for n in self.raw_nodes]
        
        # 2. Customers (C): Exclude first (start) and last (end) node
        self.Sets['C'] = self.Sets['N'][1:-1]
        
        # 3. Drones (K)
        num_drones = self.meta.get('DroneNum', 1)
        self.Sets['K'] = list(range(1, num_drones + 1))

        # 4. Arcs (A): Fully connected graph (excluding self-loops and invalid depot returns)
        start_depot = self.Sets['N'][0]
        end_depot = self.Sets['N'][-1]
        
        self.Sets['A'] = []
        for i in self.Sets['N']:
            for j in self.Sets['N']:
                if i == j: continue
                if i == end_depot: continue # Cannot leave end depot
                if j == start_depot: continue # Cannot enter start depot
                self.Sets['A'].append((i, j))

    def _build_parameters(self):
        """
        Calculates Euclidean Distances and extracts Physics/Demand parameters.
        """
        dist_dict = {}
        time_windows = {}
        demands = {}
        
        # Access the first node to get global physics (repeated in every row)
        global_params = self.raw_nodes[0]
        
        # 1. Distances (Euclidean)
        coords = {n['#Node']: (n['X_coor'], n['Y_coor']) for n in self.raw_nodes}
        
        for (i, j) in self.Sets['A']:
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            d_ij = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            dist_dict[(i, j)] = d_ij

        # 2. Node Parameters
        for n in self.raw_nodes:
            nid = n['#Node']
            demands[nid] = n['Demand']
            time_windows[nid] = (n['ReadyTime'], n['DueTime'])

        # 3. Physics & Operational Bounds
        if self.wind_scenario.upper() == 'UNIFORM':
            wind_speed = global_params['WIND_SPEED_UNIFORM_MS']
        else:
            wind_speed = global_params['WIND_SPEED_RAYLEIGH_MS']

        physics = {
            'v_min': global_params['MIN_CRUISE_SPEED_MS'],
            'v_max': global_params['MAX_CRUISE_SPEED_MS'],
            'v_vert': global_params['VERTICAL_SPEED_MS'],
            'v_wind': wind_speed
        }

        self.Params = {
            'dist': dist_dict,      # d_ij
            'demand': demands,      # q_i
            'tw': time_windows,     # [e_i, l_i]
            'physics': physics      # v_min, v_wind, etc.
        }

# --- Quick Test ---
if __name__ == "__main__":
    # Point to one of your actual files in the new folder structure
    test_file = "augmented_data/Type_1/Set_A1_Cust_10_1.txt"
    
    try:
        model = MILPInstance(test_file, wind_scenario='RAYLEIGH')
        print(f"✅ Loaded: {test_file}")
        print(f"   Nodes: {len(model.Sets['N'])} | Arcs: {len(model.Sets['A'])}")
        print(f"   Wind ({model.wind_scenario}): {model.Params['physics']['v_wind']:.4f} m/s")
    except Exception as e:
        print(f"❌ Error: {e}")