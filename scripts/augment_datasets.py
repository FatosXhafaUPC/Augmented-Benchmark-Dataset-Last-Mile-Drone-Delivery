import os
import sys
import math
import random
import hashlib

def get_deterministic_seed(filename):
    """
    Creates a deterministic integer seed from the filename.
    Ensures reproducibility: Set_A1... always gets the same wind values.
    """
    filename_bytes = filename.encode('utf-8')
    hash_object = hashlib.md5(filename_bytes)
    return int(hash_object.hexdigest(), 16)

def generate_wind_rayleigh_barcelona(seed_val):
    random.seed(seed_val)
    sigma_bcn = 2.79
    u = random.random()
    if u <= 0: u = 1e-9
    return sigma_bcn * math.sqrt(-2 * math.log(u))

def generate_wind_uniform(seed_val):
    random.seed(seed_val)
    return random.uniform(3, 8)

def process_instance(file_path, output_path, filename):
    # 1. Generate Parameters (Same logic as before)
    base_seed = get_deterministic_seed(filename)
    
    v_min = 10.0
    v_max = 25.0
    h_dot = 0.5
    
    # Use offset seeds for independence
    wind_uniform = generate_wind_uniform(base_seed)
    wind_rayleigh = generate_wind_rayleigh_barcelona(base_seed + 1000)

    # Prepare the suffix string (the 5 new columns)
    # We use tabs (\t) to ensure clean separation
    params_suffix = f"\t{v_min}\t{v_max}\t{h_dot}\t{wind_uniform:.4f}\t{wind_rayleigh:.4f}"
    
    # Header suffix
    header_suffix = "\tMIN_CRUISE_SPEED_MS\tMAX_CRUISE_SPEED_MS\tVERTICAL_SPEED_MS\tWIND_SPEED_UNIFORM_MS\tWIND_SPEED_RAYLEIGH_MS"

    # 2. Read and Transform Lines
    new_lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    header_found = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines, just copy them
        if not stripped:
            new_lines.append(line)
            continue
            
        parts = stripped.split()
        
        # Detect the Table Header (starts with #Node)
        if parts[0] == "#Node":
            header_found = True
            # Strip the newline char, add suffix, then add newline back
            new_header = line.rstrip('\n') + header_suffix + "\n"
            new_lines.append(new_header)
            continue
        
        # Detect Data Rows (must be after header, and start with a number)
        if header_found and parts[0].isdigit():
            new_row = line.rstrip('\n') + params_suffix + "\n"
            new_lines.append(new_row)
        else:
            # Metadata lines (CustNum, DroneNum, source tags) - copy as is
            new_lines.append(line)

    # 3. Write to Output
    with open(output_path, 'w') as f:
        f.writelines(new_lines)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 augment_datasets.py <INPUT_FOLDER> <OUTPUT_FOLDER>")
        sys.exit(1)

    input_root = sys.argv[1]
    output_root = sys.argv[2]

    if not os.path.exists(input_root):
        print(f"Error: Input directory '{input_root}' does not exist.")
        sys.exit(1)

    print(f"Processing instances from {input_root}...")
    instance_count = 0
    
    for dirpath, dirnames, filenames in os.walk(input_root):
        rel_path = os.path.relpath(dirpath, input_root)
        target_dir = os.path.join(output_root, rel_path)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for filename in filenames:
            if filename.endswith(".txt"):
                input_file = os.path.join(dirpath, filename)
                output_file = os.path.join(target_dir, filename)
                process_instance(input_file, output_file, filename)
                instance_count += 1
                
    print(f"Successfully generated {instance_count} column-augmented instances in '{output_root}'.")

if __name__ == "__main__":
    main()
