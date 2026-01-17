import sys

def parse_augmented_instance(file_path):
    """
    Parses the Augmented Cheng et al. format.
    Returns:
        metadata (dict): Global params (CustNum, DroneNum)
        nodes (list of dicts): The row-by-row data
    """
    metadata = {}
    nodes = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()

    header_map = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped: continue
        
        parts = stripped.split() # This handles mixed tabs/spaces automatically
        
        # 1. Parse Metadata (CustNum, DroneNum)
        if parts[0] == 'CustNum':
            metadata['CustNum'] = int(parts[1])
            continue
        if parts[0] == 'DroneNum':
            metadata['DroneNum'] = int(parts[1])
            continue
            
        # 2. Parse Header
        if parts[0] == '#Node':
            # Store column names for mapping
            header_map = parts 
            continue
            
        # 3. Parse Data Rows (if line starts with a digit)
        if parts[0].isdigit() and header_map:
            row_data = {}
            for i, value in enumerate(parts):
                col_name = header_map[i]
                # Convert to float, then int if it's a whole number
                try:
                    val_float = float(value)
                    row_data[col_name] = int(val_float) if val_float.is_integer() else val_float
                except ValueError:
                    row_data[col_name] = value # Keep as string if not number
            
            nodes.append(row_data)

    return metadata, nodes

# --- RUN THE TEST ---
# Change this path to one of your actual generated files
test_file = "AUGMENTED_BENCHMARK_DATASET/Type_1/Set_A1_Cust_10_1.txt" 

try:
    meta, data = parse_augmented_instance(test_file)
    print(f"✅ SUCCESS! parsed {test_file}")
    print("-" * 40)
    print(f"Metadata: {meta}")
    print("-" * 40)
    print(f"First Node (Depot): {data[0]}")
    print("-" * 40)
    print(f"Last Node (Customer): {data[-1]}")
    print("-" * 40)
    print(f"Total Rows Read: {len(data)}")
    
except Exception as e:
    print(f"❌ ERROR: Could not parse file. Reason: {e}")