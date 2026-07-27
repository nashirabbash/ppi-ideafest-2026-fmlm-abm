"""
Configuration Parameters for Paratransit Headway & Micro-Equity Simulation
Paper Target: PPI IDEAFEST 2026 National Paper Competition
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

# Random Seed for 100% Reproducibility
SEED = 42

# Corridor & Network Configuration
ROUTE_LENGTH_KM = 8.5
NUM_STOPS = 12
KRL_STATION_STOP_IDX = 0
SPEED_KMH_MEAN = 25.0  # Mean speed in km/h
SPEED_KMH_STD = 4.0

# Fleet & Capacity Parameters
NUM_DRIVERS = 40  # Fleet size per corridor loop
VEHICLE_CAPACITY = 12  # Standard Angkot capacity
BASE_HEADWAY_SCHEDULED_MIN = 6.0  # Scheduled headway in minutes

# Commuter Demand Parameters (Poisson Rates)
LAMBDA_PEAK_PAX_PER_HR = 120  # Peak hours (06:00-09:00, 16:00-19:00)
LAMBDA_OFFPEAK_PAX_PER_HR = 25  # Off-peak hours
MAX_WAIT_TIME_TOLERANCE_MIN = 15.0

# Economics & Financial Parameters (IDR)
FARE_IDR = 4000.0  # Standard flat fare per trip
BOK_PER_KM_IDR = 2500.0  # Operational cost per km (fuel, maintenance, driver)
DAILY_TARGET_REVENUE_IDR = 220000.0  # Historical daily gross target
NET_BOK_REVENUE_FLOOR_IDR = 180000.0  # Guaranteed net revenue floor (Arm B/D)
FLAT_BTS_WAGE_IDR = 150000.0  # Fixed gross BTS flat daily wage (Arm B)
EQUITY_POOL_SHARE = 0.15  # 15% cooperative dividend pool

# Driver Behavioral Utility Parameters (Random Utility Maximization)
# U_{i,t} = beta_0 + beta_1 * E[R_net] - beta_2 * Var(R) + beta_3 * S_{equity} - gamma * P_{gaming}
BETA_0 = 0.2
BETA_1 = 0.000015  # Scaled for IDR revenue expectation
BETA_2 = 0.00000005  # Scaled for IDR revenue variance penalty
BETA_3 = 1.2  # Equity ownership utility multiplier
GAMMA_GAMING = 2.5  # Anti-gaming penalty coefficient

BOYCOTT_UTILITY_THRESHOLD = -0.3  # Utility threshold below which driver boycotts/quits

# Telemetry Anti-Gaming Parameters
ALPHA_GAMING = 1.5  # Quadratic penalty scaling factor
TAU_MAX_BASE_MIN = 3.0  # Base maximum allowable dwell time (mins)

# Simulation Execution & Time Step
TICKS_PER_MINUTE = 2  # 30 seconds per tick
OPERATIONAL_HOURS_PER_DAY = 16  # 06:00 to 22:00
TICKS_PER_DAY = OPERATIONAL_HOURS_PER_DAY * 60 * TICKS_PER_MINUTE  # 1920 ticks/day

# Monte Carlo Settings
RUNS_PER_ARM = 125  # 125 runs x 4 arms = 500 total Monte Carlo runs
SIMULATION_DAYS_PER_RUN = 30  # Representative 30-day operational cycle

# Treatment Arms Matrix (2x2 Factorial Design)
TREATMENT_ARMS = {
    "Arm_A": {
        "name": "Arm A: Baseline Setoran Tradisi",
        "flexible_dispatch": False,
        "revenue_floor": False,
        "micro_equity": False,
        "anti_gaming": False
    },
    "Arm_B": {
        "name": "Arm B: Gross BTS Kaku (Flat Wage)",
        "flexible_dispatch": False,
        "revenue_floor": True,
        "flat_wage": True,
        "micro_equity": False,
        "anti_gaming": False
    },
    "Arm_C": {
        "name": "Arm C: Unprotected Flexible Dispatch",
        "flexible_dispatch": True,
        "revenue_floor": False,
        "micro_equity": False,
        "anti_gaming": False
    },
    "Arm_D": {
        "name": "Arm D: UNIFIED FRAMEWORK (Proposed)",
        "flexible_dispatch": True,
        "revenue_floor": True,
        "flat_wage": False,
        "micro_equity": True,
        "anti_gaming": True
    }
}
