import pandas as pd
import random
import time
import json
from datetime import datetime

# =====================================================
# CONFIGURATION
# =====================================================

PULSES_PER_LITER = 450
PRESSURE_CONSTANT = 0.05
PAID_WATER_LITERS = 5          # User prepaid amount
MAX_RUNTIME_SECONDS = 60       # Maximum monitoring duration

# =====================================================
# SYSTEM STATE
# =====================================================

total_pulses = 0
total_liters_used = 0
remaining_credit = PAID_WATER_LITERS
valve_open = True
records = []

# =====================================================
# SENSOR SIMULATION
# =====================================================

def read_flow_sensor():
    """
    Simulate water flow sensor pulses.
    Replace this with real GPIO interrupt logic in hardware.
    """
    return random.randint(50, 200)

# =====================================================
# VALVE CONTROL
# =====================================================

def open_valve():
    global valve_open
    valve_open = True
    print("Valve opened.")

def close_valve():
    global valve_open
    valve_open = False
    print("Valve closed.")

# =====================================================
# USER NOTIFICATION
# =====================================================

def notify_user():
    print("ALERT: Paid water exhausted.")
    print("Please recharge to continue using water.")

# =====================================================
# MAIN MONITORING FUNCTION
# =====================================================

def monitor_water_system():
    global total_pulses, total_liters_used, remaining_credit

    open_valve()

    for _ in range(MAX_RUNTIME_SECONDS):

        if not valve_open:
            break

        pulses = read_flow_sensor()
        total_pulses += pulses

        liters_this_second = pulses / PULSES_PER_LITER
        total_liters_used += liters_this_second
        remaining_credit -= liters_this_second

        # Simulated pressure calculation
        flow_rate = liters_this_second
        pressure = flow_rate * PRESSURE_CONSTANT * 100

        timestamp = datetime.now()

        print(
            f"Total Used: {total_liters_used:.3f} L | "
            f"Remaining: {max(remaining_credit, 0):.3f} L | "
            f"Pressure: {pressure:.2f} kPa"
        )

        records.append({
            "timestamp": timestamp,
            "pulses": pulses,
            "liters_used_this_second": round(liters_this_second, 4),
            "total_liters_used": round(total_liters_used, 4),
            "remaining_credit": round(max(remaining_credit, 0), 4),
            "pressure_kPa": round(pressure, 2)
        })

        # Shutoff condition
        if remaining_credit <= 0:
            close_valve()
            notify_user()
            break

        time.sleep(1)

# =====================================================
# SUMMARY REPORT GENERATION
# =====================================================

def generate_summary_report():

    if not records:
        print("No data recorded.")
        return

    df = pd.DataFrame(records)

    total_consumed = df["liters_used_this_second"].sum()
    average_usage = df["liters_used_this_second"].mean()
    average_pressure = df["pressure_kPa"].mean()
    peak_usage = df["liters_used_this_second"].max()
    peak_pressure = df["pressure_kPa"].max()
    runtime_seconds = len(df)

    summary_report = {
        "initial_paid_water_liters": PAID_WATER_LITERS,
        "total_water_consumed_liters": round(total_consumed, 3),
        "remaining_credit_liters": round(max(remaining_credit, 0), 3),
        "runtime_seconds": runtime_seconds,
        "average_usage_liters_per_second": round(average_usage, 4),
        "average_pressure_kPa": round(average_pressure, 2),
        "peak_usage_liters_per_second": round(peak_usage, 3),
        "peak_pressure_kPa": round(peak_pressure, 2)
    }

    with open("water_summary_report.json", "w") as file:
        json.dump(summary_report, file, indent=4)

    print("\nSummary report saved as water_summary_report.json")

# =====================================================
# PROGRAM ENTRY POINT
# =====================================================

if __name__ == "__main__":
    monitor_water_system()
    generate_summary_report()
