import time
import random

# ==============================
# SYSTEM CONFIGURATION
# ==============================

PULSES_PER_LITER = 450      # Calibration value
paid_water_liters = 3      # User paid for 20 liters

# System state
total_pulses = 0
total_liters_used = 0
valve_open = True


# ==============================
# SENSOR SIMULATION
# ==============================

def read_flow_sensor():
    """
    Simulate reading pulses from water flow sensor.
    In real system, this comes from GPIO interrupt.
    """
    return random.randint(10, 50)  # random pulses per second


# ==============================
# VALVE CONTROL
# ==============================

def open_valve():
    global valve_open
    valve_open = True
    print("Valve opened.")


def close_valve():
    global valve_open
    valve_open = False
    print("Valve closed.")


# ==============================
# NOTIFICATION SYSTEM
# ==============================

def notify_user():
    print("ALERT: Paid water exhausted!")
    print("Please recharge to continue using water.")


# ==============================
# MAIN CONTROL LOOP
# ==============================

def monitor_water_usage():
    global total_pulses, total_liters_used

    open_valve()

    while valve_open:
        pulses = read_flow_sensor()
        total_pulses += pulses

        # Convert pulses to liters
        total_liters_used = total_pulses / PULSES_PER_LITER

        print(f"Water used: {total_liters_used:.2f} L / {paid_water_liters} L")

        # Check if credit exhausted
        if total_liters_used >= paid_water_liters:
            close_valve()
            notify_user()
            break

        time.sleep(1)


# ==============================
# RUN SYSTEM
# ==============================

if __name__ == "__main__":
    monitor_water_usage()
