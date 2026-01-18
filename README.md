[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18215032-blue)](https://doi.org/10.5281/zenodo.18215032)
# Augmented Benchmark Dataset for Single-Truck Multiple Drones Last-Mile Delivery

This repository contains an augmented version of the standard benchmark dataset (Cheng et al., 2018) for Drone Routing Problems (DRP) and Vehicle Routing Problems with Drones (VRPD).

The dataset has been enhanced with **operational physics parameters** to support energy-aware optimization and realistic weather scenarios using data from City of Barcelona.

## Dataset Structure

The repository is organized as follows:
- **`original_data/`**: The original instances from Cheng et al. (Type 1 and Type 2).
- **`augmented_data/`**: The processed instances containing 5 additional columns for operational limits.
- **`scripts/`**: Python scripts used to generate the data and parse it.

## Augmentation Details

For every instance, we have appended the following parameters as new columns (tab-separated):

| Parameter | Description | Value |
| :--- | :--- | :--- |
| `MIN_CRUISE_SPEED_MS` | Minimum safe flight speed | 10.0 m/s |
| `MAX_CRUISE_SPEED_MS` | Maximum safe flight speed | 25.0 m/s |
| `VERTICAL_SPEED_MS` | Speed for takeoff/landing | 0.5 m/s |
| `WIND_SPEED_UNIFORM_MS` | Wind speed sampled from Uniform[3, 8] | *Instance Specific* |
| `WIND_SPEED_RAYLEIGH_MS` | Wind speed sampled from Rayleigh (Barcelona) | *Instance Specific* |

**Reproducibility Note:** The wind values are generated using a deterministic seed based on the MD5 hash of the filename. This ensures that `Set_A1_Cust_10_1.txt` always contains the exact same wind values.

## Usage (Python)

```python
from scripts.data_utils import parse_augmented_instance

meta, nodes = parse_augmented_instance("augmented_data/Type_1/Set_A1_Cust_10_1.txt")
print(meta)
# {'CustNum': 10, 'DroneNum': 2}
```

## Citation

If you use this dataset or code, please cite:

**Augmented Dataset:**
Xhafa, F. (2026). Augmented Benchmark Dataset for Last-Mile Drone Delivery (v1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18215032

**Code Repository:**
Xhafa, F. (2026). Augmented Benchmark Dataset Source Code. GitHub. https://github.com/FatosXhafaUPC/Augmented-Benchmark-Dataset-Last-Mile-Drone-Delivery

**Original Data Source:**
Cheng, C., Adulyasak, Y., Rousseau, L.-M. (2020). Drone routing with energy function: Formulation and exact algorithm. *Transportation Research Part B: Methodological*, 139, 364–387. https://doi.org/10.1016/j.trb.2020.06.011
