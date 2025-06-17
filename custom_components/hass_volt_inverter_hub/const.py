#!/usr/bin/env python

"""
CONST – Volt Inverter Hub for HASS
"""
from __future__ import annotations

DOMAIN           = "volt_inverter_hub_for_hass"
DEFAULT_PORT     = "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0"
DEFAULT_BAUDRATE = 19200
UPDATE_INTERVAL  = 10          # encje bez własnego „interval” przyjmą 10 s

# ------------------------------------------------------------------
#  ↓↓↓ MAPA REJESTRÓW – kontynuacja w kolejnych wiadomościach ↓↓↓
# ------------------------------------------------------------------
registers = {
    # ---------- GENERAL -------------------------------------------------
    "volt_general_work_state": {
        "addr": 25201,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "volt_general_work_state",
        "interval": 2,
        "is_write_reg": False
    },

    # ---------- BATTERY & DC -------------------------------------------
    "volt_battery_voltage": {
        "addr": 25205,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "volt_battery_voltage",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_battery_power": {
        "addr": 25273,
        "scale": 1,
        "unit": "W",
        "device_class": "power",
        "display_name": "volt_battery_power",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_battery_current": {
        "addr": 25274,
        "scale": 1,
        "unit": "A",
        "device_class": "current",
        "display_name": "volt_battery_current",
        "interval": 2,
        "is_write_reg": False
    },

    # ---------- INVERTER / GRID / BUS / LOAD ---------------------------
    "volt_inverter_voltage": {
        "addr": 25206,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Inverter Voltage",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_grid_voltage": {
        "addr": 25207,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Grid Voltage",
        "interval": 10,
        "is_write_reg": False
    },
    "volt_bus_voltage": {
        "addr": 25208,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT BUS Voltage",
        "interval": 15,
        "is_write_reg": False
    },
    "volt_control_current": {
        "addr": 25209,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Control Current",
        "interval": 15,
        "is_write_reg": False
    },
    "volt_inverter_current": {
        "addr": 25210,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Inverter Current",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_grid_current": {
        "addr": 25211,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Grid Current",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_load_current": {
        "addr": 25212,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Load Current",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_power_inverter": {
        "addr": 25213,
        "scale": 1,
        "unit": "W",
        "device_class": "power",
        "display_name": "VOLT Power Inverter",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_power_grid": {
        "addr": 25214,
        "scale": 1,
        "unit": "W",
        "device_class": "power",
        "display_name": "VOLT Power Grid",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_power_load": {
        "addr": 25215,
        "scale": 1,
        "unit": "W",
        "device_class": "power",
        "display_name": "VOLT Power Load",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_load_percent": {
        "addr": 25216,
        "scale": 1,
        "unit": "%",
        "device_class": "power_factor",
        "display_name": "VOLT Load Percent",
        "interval": 2,
        "is_write_reg": False
    },

    # ---------- APPARENT / REACTIVE POWER ------------------------------
    "volt_s_inverter": {
        "addr": 25217,
        "scale": 1,
        "unit": "VA",
        "device_class": "apparent_power",
        "display_name": "VOLT S Inverter",
        "interval": 15,
        "is_write_reg": False
    },
    "volt_s_grid": {
        "addr": 25218,
        "scale": 1,
        "unit": "VA",
        "device_class": "apparent_power",
        "display_name": "VOLT S Grid",
        "interval": 15,
        "is_write_reg": False
    },
    "volt_s_load": {
        "addr": 25219,
        "scale": 1,
        "unit": "VA",
        "device_class": "apparent_power",
        "display_name": "VOLT S Load",
        "interval": 15,
        "is_write_reg": False
    },
    "volt_q_inverter": {
        "addr": 25221,
        "scale": 1,
        "unit": "var",
        "device_class": "reactive_power",
        "display_name": "VOLT Q Inverter",
        "interval": 15,
        "is_write_reg": False
    },
    "volt_q_grid": {
        "addr": 25222,
        "scale": 1,
        "unit": "var",
        "device_class": "reactive_power",
        "display_name": "VOLT Q Grid",
        "interval": 15,
        "is_write_reg": False
    },
    "volt_q_load": {
        "addr": 25223,
        "scale": 1,
        "unit": "var",
        "device_class": "reactive_power",
        "display_name": "VOLT Q Load",
        "interval": 15,
        "is_write_reg": False
    },

    # ---------- FREQUENCY ----------------------------------------------
    "volt_frequency_inverter": {
        "addr": 25225,
        "scale": 0.01,
        "unit": "Hz",
        "device_class": "frequency",
        "display_name": "VOLT Frequency Inverter",
        "interval": 15,
        "is_write_reg": False
    },
    "volt_frequency_grid": {
        "addr": 25226,
        "scale": 0.01,
        "unit": "Hz",
        "device_class": "frequency",
        "display_name": "VOLT Frequency Grid",
        "interval": 2,
        "is_write_reg": False
    },

    # ---------- TEMPERATURE --------------------------------------------
    "volt_dc_radiator_temperature": {
        "addr": 25233,
        "scale": 1,
        "unit": "°C",
        "device_class": "temperature",
        "display_name": "VOLT DC Radiator Temperature",
        "interval": 10,
        "is_write_reg": False
    },
    # ---------- RELAY STATES -------------------------------------------
    "volt_inverter_relay_state": {
        "addr": 25237,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT Inverter Relay State",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_grid_relay_state": {
        "addr": 25238,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT Grid Relay State",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_load_relay_state": {
        "addr": 25239,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT Load Relay State",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_n_line_relay_state": {
        "addr": 25240,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT N Line Relay State",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_dc_relay_state": {
        "addr": 25241,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT DC Relay State",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_earth_relay_state": {
        "addr": 25242,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT Earth Relay State",
        "interval": 2,
        "is_write_reg": False
    },

    # ---------- ENERGY – CHARGER / DISCHARGER / BUY / SELL -------------
    "volt_accumulated_charger_power_h": {
        "addr": 25245,
        "scale": 1000,
        "unit": "kWh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated charger power H",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_charger_power": {
        "addr": 25246,
        "scale": 100,
        "unit": "Wh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated charger power",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_discharger_power_h": {
        "addr": 25247,
        "scale": 1000,
        "unit": "kWh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated discharger power H",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_discharger_power": {
        "addr": 25248,
        "scale": 100,
        "unit": "Wh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated discharger power",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_buy_power_h": {
        "addr": 25249,
        "scale": 1000,
        "unit": "kWh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated buy power H",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_buy_power": {
        "addr": 25250,
        "scale": 100,
        "unit": "Wh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated buy power",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_sell_power_h": {
        "addr": 25251,
        "scale": 1000,
        "unit": "kWh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated sell power H",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_sell_power": {
        "addr": 25252,
        "scale": 100,
        "unit": "Wh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated sell power",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_load_power_h": {
        "addr": 25253,
        "scale": 1000,
        "unit": "kWh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated load power H",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_load_power": {
        "addr": 25254,
        "scale": 100,
        "unit": "Wh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated load power",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_self_use_power_h": {
        "addr": 25255,
        "scale": 1000,
        "unit": "kWh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated self_use power H",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_self_use_power": {
        "addr": 25256,
        "scale": 100,
        "unit": "Wh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated self_use power",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_pv_sell_power_h": {
        "addr": 25257,
        "scale": 1000,
        "unit": "kWh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated PV_sell power H",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_accumulated_pv_sell_power": {
        "addr": 25258,
        "scale": 100,
        "unit": "Wh",
        "device_class": "energy",
        "display_name": "VOLT Accumulated PV_sell power",
        "interval": 30,
        "is_write_reg": False
    },

    # ---------- BATTERY ENERGY FROM GRID -------------------------------
    "volt_battery_energy_accumulated_from_grid_h": {
        "addr": 25259,
        "scale": 1000,
        "unit": "kWh",
        "device_class": "energy",
        "display_name": "volt_battery_energy_accumulated_from_grid_high",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_battery_energy_accumulated_from_grid": {
        "addr": 25260,
        "scale": 100,
        "unit": "Wh",
        "device_class": "energy",
        "display_name": "volt_battery_energy_accumulated_from_grid",
        "interval": 30,
        "is_write_reg": False
    },

    # ---------- BATTERY POWER / CURRENT (25273-25274) już w części 1 ----

    # ---------- MPPT – WORK STATES & BASIC -----------------------------
    "volt_mppt_charger_work_state": {
        "addr": 15201,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT charger workstate",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_mppt_work_state": {
        "addr": 15202,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT workstate",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_mppt_charging_work_state": {
        "addr": 15203,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT charging workstate",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_mppt_charger_voltage": {
        "addr": 15205,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "volt_mppt_charger_voltage",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_mppt_charger_battery_voltage": {
        "addr": 15206,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "volt_mppt_charger_battery_voltage",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_mppt_charger_current": {
        "addr": 15207,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "volt_mppt_charger_current",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_mppt_charger_power": {
        "addr": 15208,
        "scale": 1,
        "unit": "W",
        "device_class": "power",
        "display_name": "volt_mppt_charger_power",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_mppt_radiator_temperature": {
        "addr": 15209,
        "scale": 1,
        "unit": "°C",
        "device_class": "temperature",
        "display_name": "volt_mppt_radiator_temperature",
        "interval": 15,
        "is_write_reg": False
    },

    # ---------- MPPT RELAY STATES --------------------------------------
    "volt_mppt_battery_relay_state": {
        "addr": 15211,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT battery relay State",
        "interval": 2,
        "is_write_reg": False
    },
    "volt_mppt_pv_relay_state": {
        "addr": 15212,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT PV relay State",
        "interval": 2,
        "is_write_reg": False
    },
    # ---------- MPPT – LICZNIKI ENERGII --------------------------------
    "volt_mppt_accumulated_pv_energy_h": {
        "addr": 15217,
        "scale": 1000,
        "unit": "kWh",
        "device_class": "energy",
        "display_name": "volt_mppt_accumulated_pv_energy_h",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_mppt_accumulated_pv_energy": {
        "addr": 15218,
        "scale": 100,
        "unit": "Wh",
        "device_class": "energy",
        "display_name": "volt_mppt_accumulated_pv_energy",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_mppt_accumulated_day": {
        "addr": 15219,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT Accumulated day",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_mppt_accumulated_hour": {
        "addr": 15220,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT Accumulated hour",
        "interval": 30,
        "is_write_reg": False
    },
    "volt_mppt_accumulated_minute": {
        "addr": 15221,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT Accumulated minute",
        "interval": 30,
        "is_write_reg": False
    },

    # ---------- SYSTEM FLAGI / STRZAŁKI --------------------------------
    "volt_arrow_flag": {
        "addr": 25279,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT Arrow Flag",
        "interval": 2,
        "is_write_reg": False
    },

    # ===================  HOLDING REGISTERS (201xx)  ===================
    # -- tryb off-grid enable (0/1) -------------------------------------
    "volt_offgrid_work_enable": {
        "addr": 20101,
        "scale": 1,
        "unit": None,
        "display_name": "Volt offgrid work enable",
        "interval": 30,
        "is_write_reg": True,
        "type": "switch",
        "write_values": {0: "OFF", 1: "ON"}
    },

    # -- setpointy napięcia / częstotliwości wyjściowej inwertera -------
    "volt_inverter_output_voltage_set": {
        "addr": 20102,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Inverter output voltage Set",
        "interval": 30,
        "is_write_reg": True,
        "min": 200.0,
        "max": 240.0,
        "step": 0.1
    },
    "volt_inverter_output_frequency_set": {
        "addr": 20103,
        "scale": 0.01,
        "unit": "Hz",
        "device_class": "frequency",
        "display_name": "VOLT Inverter output frequency Set",
        "interval": 30,
        "is_write_reg": True,
        "min": 49.0,
        "max": 60.0,
        "step": 0.01
    },

    # -- SEARCH MODE – przełącznik (już był, zostawiamy identyczny klucz)
    "volt_inverter_search_mode_switch": {
        "addr": 20104,
        "scale": 1,
        "unit": None,
        "display_name": "volt_inverter_search_mode_enable",
        "interval": 30,
        "is_write_reg": True,
        "type": "switch",
        "write_values": {0: "OFF", 1: "ON"}
    },

    # -- ENERGY USE MODE  (select) --------------------------------------
    "volt_energy_use_mode": {
        "addr": 20109,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT Energy use mode",
        "interval": 30,
        "is_write_reg": True,
        "type": "select",
        "options": {
            0: "Solar",
            1: "Solar Battery Grid",
            2: "Solar Grid Battery",
            3: "Grid"
        }
    },

    # -- GRID PROTECT STANDARD (surowy rejestr) -------------------------
    "volt_grid_protect_standard": {
        "addr": 20111,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT Grid protect standard",
        "interval": 30,
        "is_write_reg": True
    },

    # -- SOLAR USE AIM (select 0/1) -------------------------------------
    "volt_solar_use_aim": {
        "addr": 20112,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT SolarUse Aim",
        "interval": 30,
        "is_write_reg": True,
        "type": "select",
        "options": {
            0: "Load then Battery",
            1: "Battery then Load"
        }
    },

    # -- prąd maks. rozładowania inwertera ------------------------------
    "volt_inverter_max_discharger_current": {
        "addr": 20113,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Inverter max discharger current",
        "interval": 30,
        "is_write_reg": True,
        "min": 0.0,
        "max": 100.0,
        "step": 0.1
    },

    # -- progi napięć akumulatora ---------------------------------------
    "volt_battery_stop_discharging_voltage": {
        "addr": 20118,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Battery stop discharging voltage",
        "interval": 30,
        "is_write_reg": True
    },
    "volt_battery_stop_charging_voltage": {
        "addr": 20119,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Battery stop charging voltage",
        "interval": 30,
        "is_write_reg": True
    },

    # -- max prąd ładowarki sieciowej -----------------------------------
    "volt_grid_max_charger_current_set": {
        "addr": 20125,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Grid max charger current set",
        "interval": 30,
        "is_write_reg": True
    },

    # -- low / high voltage alarm setpoints -----------------------------
    "volt_battery_low_voltage": {
        "addr": 20127,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Battery low voltage",
        "interval": 30,
        "is_write_reg": True
    },
    "volt_battery_high_voltage": {
        "addr": 20128,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Battery high voltage",
        "interval": 30,
        "is_write_reg": True
    },

    # -- max combined charger current -----------------------------------
    "volt_max_combine_charger_current": {
        "addr": 20132,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Max combine charger current",
        "interval": 30,
        "is_write_reg": True
    },

    # -- CHARGER SOURCE PRIORITY (select) -------------------------------
    "volt_charger_source_priority": {
        "addr": 20143,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT Charger source priority",
        "interval": 30,
        "is_write_reg": True,
        "type": "select",
        "options": {
            0: "Solar first",
            2: "Solar + Grid",
            3: "Only Solar"
        }
    },

    # -- SOLAR POWER BALANCE (raw) --------------------------------------
    "volt_solar_power_balance": {
        "addr": 20144,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT Solar power balance",
        "interval": 30,
        "is_write_reg": True
    },

    # =================  MPPT SETTINGS (101xx)  ==========================
    "volt_mppt_float_voltage": {
        "addr": 10103,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT MPPT Float voltage",
        "interval": 30,
        "is_write_reg": True
    },
    "volt_mppt_absorption_voltage": {
        "addr": 10104,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT MPPT Absorption voltage",
        "interval": 30,
        "is_write_reg": True
    },
    "volt_mppt_battery_low_voltage": {
        "addr": 10105,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT MPPT battery low voltage",
        "interval": 30,
        "is_write_reg": True
    },
    "volt_mppt_battery_high_voltage": {
        "addr": 10107,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT MPPT battery high voltage",
        "interval": 30,
        "is_write_reg": True
    },
    "volt_mppt_pv_max_charger_current": {
        "addr": 10108,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT MPPT PV Max charger current",
        "interval": 30,
        "is_write_reg": True
    },
    "volt_mppt_battery_type": {
        "addr": 10110,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT MPPT Battery type",
        "interval": 30,
        "is_write_reg": True
    },
    "volt_mppt_battery_type": {
        "addr": 10110,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT MPPT Battery type",
        "interval": 30,
        "is_write_reg": True
    }
}  # ←–––––––––––––––––– koniec słownika `registers`

# ------------------------------------------------------------------
#  Definicja obsługiwanego modelu + skróty
# ------------------------------------------------------------------
MODEL_CONFIGS = {
    "volt_sinus_pro_ultra_6000": {
        "name": "Volt Sinus PRO ULTRA 6 kW 24 V",
        "default_slave": 4,
        "registers": registers
    }
}

SUPPORTED_MODELS = {k: v["name"] for k, v in MODEL_CONFIGS.items()}