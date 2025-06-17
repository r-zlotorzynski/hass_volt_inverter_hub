#!/usr/bin/env python

"""
CONST – Volt Inverter Hub for HASS
"""
from __future__ import annotations

DOMAIN           = "hass_volt_inverter_hub"
DEFAULT_PORT     = "/dev/ttyUSB0"
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
        "is_write_reg": False,
        "input_type": "holding"
    },

    # ---------- BATTERY & DC -------------------------------------------
    "volt_battery_voltage": {
        "addr": 25205,
        "scale": 0.1,
        "precision": 2,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "volt_battery_voltage",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_battery_power": {
        "addr": 25273,
        "scale": 1,
        "unit": "W",
        "device_class": "power",
        "display_name": "volt_battery_power",
        "is_write_reg": False,
        "input_type": "holding",
        "interval": 5
    },
    "volt_battery_current": {
        "addr": 25274,
        "scale": 1,
        "unit": "A",
        "device_class": "current",
        "display_name": "volt_battery_current",
        "is_write_reg": False,
        "input_type": "holding"
    },

    # ---------- INVERTER / GRID / BUS / LOAD ---------------------------
    "volt_inverter_voltage": {
        "addr": 25206,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Inverter Voltage",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_grid_voltage": {
        "addr": 25207,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Grid Voltage",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_bus_voltage": {
        "addr": 25208,
        "scale": 0.1,
        "precision": 1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT BUS Voltage",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_control_current": {
        "addr": 25209,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Control Current",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_inverter_current": {
        "addr": 25210,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Inverter Current",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_grid_current": {
        "addr": 25211,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Grid Current",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_load_current": {
        "addr": 25212,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Load Current",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_power_inverter": {
        "addr": 25213,
        "scale": 1,
        "unit": "W",
        "device_class": "power",
        "display_name": "VOLT Power Inverter",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_power_grid": {
        "addr": 25214,
        "scale": 1,
        "unit": "W",
        "device_class": "power",
        "display_name": "VOLT Power Grid",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_power_load": {
        "addr": 25215,
        "scale": 1,
        "unit": "W",
        "device_class": "power",
        "display_name": "VOLT Power Load",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_load_percent": {
        "addr": 25216,
        "scale": 1,
        "unit": "%",
        "device_class": "power_factor",
        "display_name": "VOLT Load Percent",
        "is_write_reg": False,
        "input_type": "holding"
    },

    # ---------- APPARENT / REACTIVE POWER ------------------------------
    "volt_s_inverter": {
        "addr": 25217,
        "scale": 1,
        "unit": "VA",
        "device_class": "apparent_power",
        "display_name": "VOLT S Inverter",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_s_grid": {
        "addr": 25218,
        "scale": 1,
        "unit": "VA",
        "device_class": "apparent_power",
        "display_name": "VOLT S Grid",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_s_load": {
        "addr": 25219,
        "scale": 1,
        "unit": "VA",
        "device_class": "apparent_power",
        "display_name": "VOLT S Load",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_q_inverter": {
        "addr": 25221,
        "scale": 1,
        "unit": "var",
        "device_class": "reactive_power",
        "display_name": "VOLT Q Inverter",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_q_grid": {
        "addr": 25222,
        "scale": 1,
        "unit": "var",
        "device_class": "reactive_power",
        "display_name": "VOLT Q Grid",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_q_load": {
        "addr": 25223,
        "scale": 1,
        "unit": "var",
        "device_class": "reactive_power",
        "display_name": "VOLT Q Load",
        "is_write_reg": False,
        "input_type": "holding"
    },

    # ---------- FREQUENCY ----------------------------------------------
    "volt_frequency_inverter": {
        "addr": 25225,
        "scale": 0.01,
        "unit": "Hz",
        "device_class": "frequency",
        "display_name": "VOLT Frequency Inverter",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_frequency_grid": {
        "addr": 25226,
        "scale": 0.01,
        "unit": "Hz",
        "device_class": "frequency",
        "display_name": "VOLT Frequency Grid",
        "is_write_reg": False,
        "input_type": "holding"
    },

    # ---------- TEMPERATURE --------------------------------------------
    "volt_dc_radiator_temperature": {
        "addr": 25233,
        "scale": 1,
        "unit": "°C",
        "device_class": "temperature",
        "display_name": "VOLT DC Radiator Temperature",
        "is_write_reg": False,
        "input_type": "holding"
    },
    # ---------- RELAY STATES -------------------------------------------
    "volt_inverter_relay_state": {
        "addr": 25237,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT Inverter Relay State",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_grid_relay_state": {
        "addr": 25238,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT Grid Relay State",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_load_relay_state": {
        "addr": 25239,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT Load Relay State",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_n_line_relay_state": {
        "addr": 25240,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT N Line Relay State",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_dc_relay_state": {
        "addr": 25241,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT DC Relay State",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_earth_relay_state": {
        "addr": 25242,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT Earth Relay State",
        "is_write_reg": False,
        "input_type": "holding"
    },

    # ---------- ENERGY – CHARGER / DISCHARGER / BUY / SELL -------------
    # ——— CHARGER -------------------------------------------------------
    "_volt_accumulated_charger_power_h": {
        "addr": 25245, "scale": 1000, "input_type": "holding", "expose": False
    },
    "_volt_accumulated_charger_power_l": {
        "addr": 25246, "scale": 100,  "input_type": "holding", "expose": False
    },
    "volt_accumulated_charger_power": {
        "display_name": "Charger energy",
        "unit": "kWh", "device_class": "energy",
        "state_class": "total_increasing",
        "precision": 3,
        "composite": {
            "sources": [
                {"key": "_volt_accumulated_charger_power_h", "factor": 1},
                {"key": "_volt_accumulated_charger_power_l", "factor": 0.001}
            ]
        }
    },
    # ——— DISCHARGER ----------------------------------------------------
    "_volt_accumulated_discharger_power_h": {
        "addr": 25247, "scale": 1000, "input_type": "holding", "expose": False
    },
    "_volt_accumulated_discharger_power_l": {
        "addr": 25248, "scale": 100,  "input_type": "holding", "expose": False
    },
    "volt_accumulated_discharger_power": {
        "display_name": "Discharger energy",
        "unit": "kWh", "device_class": "energy",
        "state_class": "total_increasing",
        "precision": 3,
        "composite": {
            "sources": [
                {"key": "_volt_accumulated_discharger_power_h", "factor": 1},
                {"key": "_volt_accumulated_discharger_power_l", "factor": 0.001}
            ]
        }
    },
    # ——— GRID BUY ------------------------------------------------------
    "_volt_accumulated_buy_power_h": {
        "addr": 25249, "scale": 1000, "input_type": "holding", "expose": False
    },
    "_volt_accumulated_buy_power_l": {
        "addr": 25250, "scale": 100,  "input_type": "holding", "expose": False
    },
    "volt_accumulated_buy_power": {
        "display_name": "Grid-buy energy",
        "unit": "kWh", "device_class": "energy",
        "state_class": "total_increasing",
        "precision": 3,
        "composite": {
            "sources": [
                {"key": "_volt_accumulated_buy_power_h", "factor": 1},
                {"key": "_volt_accumulated_buy_power_l", "factor": 0.001}
            ]
        }
    },
    # ——— GRID SELL -----------------------------------------------------
    "_volt_accumulated_sell_power_h": {
        "addr": 25251, "scale": 1000, "input_type": "holding", "expose": False
    },
    "_volt_accumulated_sell_power_l": {
        "addr": 25252, "scale": 100,  "input_type": "holding", "expose": False
    },
    "volt_accumulated_sell_power": {
        "display_name": "Grid-sell energy",
        "unit": "kWh", "device_class": "energy",
        "state_class": "total_increasing",
        "precision": 3,
        "composite": {
            "sources": [
                {"key": "_volt_accumulated_sell_power_h", "factor": 1},
                {"key": "_volt_accumulated_sell_power_l", "factor": 0.001}
            ]
        }
    },
    # ——— LOAD ----------------------------------------------------------
    "_volt_accumulated_load_power_h": {
        "addr": 25253, "scale": 1000, "input_type": "holding", "expose": False
    },
    "_volt_accumulated_load_power_l": {
        "addr": 25254, "scale": 100,  "input_type": "holding", "expose": False
    },
    "volt_accumulated_load_power": {
        "display_name": "Load energy",
        "unit": "kWh", "device_class": "energy",
        "state_class": "total_increasing",
        "precision": 3,
        "composite": {
            "sources": [
                {"key": "_volt_accumulated_load_power_h", "factor": 1},
                {"key": "_volt_accumulated_load_power_l", "factor": 0.001}
            ]
        }
    },
    # ——— SELF-USE ------------------------------------------------------
    "_volt_accumulated_self_use_power_h": {
        "addr": 25255, "scale": 1000, "input_type": "holding", "expose": False
    },
    "_volt_accumulated_self_use_power_l": {
        "addr": 25256, "scale": 100,  "input_type": "holding", "expose": False
    },
    "volt_accumulated_self_use_power": {
        "display_name": "Self-use energy",
        "unit": "kWh", "device_class": "energy",
        "state_class": "total_increasing",
        "precision": 3,
        "composite": {
            "sources": [
                {"key": "_volt_accumulated_self_use_power_h", "factor": 1},
                {"key": "_volt_accumulated_self_use_power_l", "factor": 0.001}
            ]
        }
    },
    # ——— PV SELL -------------------------------------------------------
    "_volt_accumulated_pv_sell_power_h": {
        "addr": 25257, "scale": 1000, "input_type": "holding", "expose": False
    },
    "_volt_accumulated_pv_sell_power_l": {
        "addr": 25258, "scale": 100,  "input_type": "holding", "expose": False
    },
    "volt_accumulated_pv_sell_power": {
        "display_name": "PV-sell energy",
        "unit": "kWh", "device_class": "energy",
        "state_class": "total_increasing",
        "precision": 3,
        "composite": {
            "sources": [
                {"key": "_volt_accumulated_pv_sell_power_h", "factor": 1},
                {"key": "_volt_accumulated_pv_sell_power_l", "factor": 0.001}
            ]
        }
    },

    # ---------- BATTERY ENERGY FROM GRID -------------------------------
    "_volt_battery_energy_grid_h": {
        "addr": 25259, "scale": 1000, "input_type": "holding", "expose": False
    },
    "_volt_battery_energy_grid_l": {
        "addr": 25260, "scale": 100,  "input_type": "holding", "expose": False
    },
    "volt_battery_energy_accumulated_from_grid": {
        "display_name": "Battery-grid energy",
        "unit": "kWh", "device_class": "energy",
        "state_class": "total_increasing",
        "precision": 3,
        "composite": {
            "sources": [
                {"key": "_volt_battery_energy_grid_h", "factor": 1},
                {"key": "_volt_battery_energy_grid_l", "factor": 0.001}
            ]
        }
    },

    # ---------- BATTERY POWER / CURRENT (25273-25274) już w części 1 ----

    # ---------- MPPT – WORK STATES & BASIC -----------------------------
    "volt_mppt_charger_work_state": {
        "addr": 15201,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT charger workstate",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_mppt_work_state": {
        "addr": 15202,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT workstate",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_mppt_charging_work_state": {
        "addr": 15203,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT charging workstate",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_mppt_charger_voltage": {
        "addr": 15205,
        "scale": 0.1,
        "precision": 2,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "volt_mppt_charger_voltage",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_mppt_charger_battery_voltage": {
        "addr": 15206,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "volt_mppt_charger_battery_voltage",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_mppt_charger_current": {
        "addr": 15207,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "volt_mppt_charger_current",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_mppt_charger_power": {
        "addr": 15208,
        "scale": 1,
        "unit": "W",
        "device_class": "power",
        "display_name": "volt_mppt_charger_power",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_mppt_radiator_temperature": {
        "addr": 15209,
        "scale": 1,
        "unit": "°C",
        "device_class": "temperature",
        "display_name": "volt_mppt_radiator_temperature",
        "is_write_reg": False,
        "input_type": "holding"
    },

    # ---------- MPPT RELAY STATES --------------------------------------
    "volt_mppt_battery_relay_state": {
        "addr": 15211,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT battery relay State",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_mppt_pv_relay_state": {
        "addr": 15212,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT PV relay State",
        "is_write_reg": False,
        "input_type": "holding"
    },

    # ---------- MPPT – LICZNIKI ENERGII --------------------------------
    "_volt_mppt_accumulated_pv_energy_h": {
        "addr": 15217,
        "scale": 1000,
        "input_type": "holding",
        "expose": False
    },
    "_volt_mppt_accumulated_pv_energy_l": {
        "addr": 15218,
        "scale": 100,
        "input_type": "holding",
        "expose": False
    },
    "volt_mppt_accumulated_pv_energy": {
        "display_name": "PV energy",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
        "precision": 3,
        "composite": {
            "sources": [
                {"key": "_volt_mppt_accumulated_pv_energy_h", "factor": 1},
                {"key": "_volt_mppt_accumulated_pv_energy_l",   "factor": 0.001}
            ]
        }
    },
    "volt_mppt_accumulated_day": {
        "addr": 15219,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT Accumulated day",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_mppt_accumulated_hour": {
        "addr": 15220,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT Accumulated hour",
        "is_write_reg": False,
        "input_type": "holding"
    },
    "volt_mppt_accumulated_minute": {
        "addr": 15221,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT MPPT Accumulated minute",
        "is_write_reg": False,
        "input_type": "holding"
    },

    # ---------- SYSTEM FLAGI / STRZAŁKI --------------------------------
    "volt_arrow_flag": {
        "addr": 25279,
        "scale": 1,
        "unit": None,
        "device_class": None,
        "display_name": "VOLT Arrow Flag",
        "is_write_reg": False,
        "input_type": "holding"
    },

    # ===================  HOLDING REGISTERS (201xx)  ===================
    # -- tryb off-grid enable (0/1) -------------------------------------
    "volt_offgrid_work_enable": {
        "addr": 20101,
        "scale": 1,
        "unit": None,
        "display_name": "Volt offgrid work enable",
        "is_write_reg": True,
        "type": "switch",
        "write_values": {0: "OFF", 1: "ON"},
        "input_type": "holding"
    },

    # -- setpointy napięcia / częstotliwości wyjściowej inwertera -------
    "volt_inverter_output_voltage_set": {
        "addr": 20102,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Inverter output voltage Set",
        "is_write_reg": True,
        "min": 200.0,
        "max": 240.0,
        "step": 0.1,
        "input_type": "holding"
    },
    "volt_inverter_output_frequency_set": {
        "addr": 20103,
        "scale": 0.01,
        "unit": "Hz",
        "device_class": "frequency",
        "display_name": "VOLT Inverter output frequency Set",
        "is_write_reg": True,
        "min": 49.0,
        "max": 60.0,
        "step": 0.01,
        "input_type": "holding"
    },

    # -- SEARCH MODE – przełącznik -------------------------------------
    "volt_inverter_search_mode_switch": {
        "addr": 20104,
        "scale": 1,
        "unit": None,
        "display_name": "volt_inverter_search_mode_enable",
        "is_write_reg": True,
        "type": "switch",
        "write_values": {0: "OFF", 1: "ON"},
        "input_type": "holding"
    },

    # -- ENERGY USE MODE  (select) --------------------------------------
    "volt_energy_use_mode": {
        "addr": 20109,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT Energy use mode",
        "is_write_reg": True,
        "type": "select",
        "options": {
            0: "Solar",
            1: "Solar Battery Grid",
            2: "Solar Grid Battery",
            3: "Grid"
        },
        "input_type": "holding"
    },

    # -- GRID PROTECT STANDARD -----------------------------------------
    "volt_grid_protect_standard": {
        "addr": 20111,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT Grid protect standard",
        "is_write_reg": True,
        "input_type": "holding"
    },

    # -- SOLAR USE AIM (select 0/1) -------------------------------------
    "volt_solar_use_aim": {
        "addr": 20112,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT SolarUse Aim",
        "is_write_reg": True,
        "type": "select",
        "options": {
            0: "Load then Battery",
            1: "Battery then Load"
        },
        "input_type": "holding"
    },

    # -- prąd maks. rozładowania ---------------------------------------
    "volt_inverter_max_discharger_current": {
        "addr": 20113,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Inverter max discharger current",
        "is_write_reg": True,
        "min": 0.0,
        "max": 100.0,
        "step": 0.1,
        "input_type": "holding"
    },

    # -- progi napięć ---------------------------------------------------
    "volt_battery_stop_discharging_voltage": {
        "addr": 20118,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Battery stop discharging voltage",
        "is_write_reg": True,
        "input_type": "holding"
    },
    "volt_battery_stop_charging_voltage": {
        "addr": 20119,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Battery stop charging voltage",
        "is_write_reg": True,
        "input_type": "holding"
    },

    # -- max prąd ładowarki sieciowej -----------------------------------
    "volt_grid_max_charger_current_set": {
        "addr": 20125,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Grid max charger current set",
        "is_write_reg": True,
        "input_type": "holding"
    },

    # -- alarm low / high ----------------------------------------------
    "volt_battery_low_voltage": {
        "addr": 20127,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Battery low voltage",
        "is_write_reg": True,
        "input_type": "holding"
    },
    "volt_battery_high_voltage": {
        "addr": 20128,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT Battery high voltage",
        "is_write_reg": True,
        "input_type": "holding"
    },

    # -- max combined charger current -----------------------------------
    "volt_max_combine_charger_current": {
        "addr": 20132,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT Max combine charger current",
        "is_write_reg": True,
        "input_type": "holding"
    },

    # -- CHARGER SOURCE PRIORITY (select) -------------------------------
    "volt_charger_source_priority": {
        "addr": 20143,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT Charger source priority",
        "is_write_reg": True,
        "type": "select",
        "options": {
            0: "Solar first",
            2: "Solar + Grid",
            3: "Only Solar"
        },
        "input_type": "holding"
    },

    # -- SOLAR POWER BALANCE -------------------------------------------
    "volt_solar_power_balance": {
        "addr": 20144,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT Solar power balance",
        "is_write_reg": True,
        "input_type": "holding"
    },

    # =================  MPPT SETTINGS (101xx)  =========================
    "volt_mppt_float_voltage": {
        "addr": 10103,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT MPPT Float voltage",
        "is_write_reg": True,
        "input_type": "holding"
    },
    "volt_mppt_absorption_voltage": {
        "addr": 10104,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT MPPT Absorption voltage",
        "is_write_reg": True,
        "input_type": "holding"
    },
    "volt_mppt_battery_low_voltage": {
        "addr": 10105,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT MPPT battery low voltage",
        "is_write_reg": True,
        "input_type": "holding"
    },
    "volt_mppt_battery_high_voltage": {
        "addr": 10107,
        "scale": 0.1,
        "unit": "V",
        "device_class": "voltage",
        "display_name": "VOLT MPPT battery high voltage",
        "is_write_reg": True,
        "input_type": "holding"
    },
    "volt_mppt_pv_max_charger_current": {
        "addr": 10108,
        "scale": 0.1,
        "unit": "A",
        "device_class": "current",
        "display_name": "VOLT MPPT PV Max charger current",
        "is_write_reg": True,
        "input_type": "holding"
    },
    "volt_mppt_battery_type": {
        "addr": 10110,
        "scale": 1,
        "unit": None,
        "display_name": "VOLT MPPT Battery type",
        "is_write_reg": True,
        "input_type": "holding"
    }
}  # ←–––– KONIEC słownika `registers`

# ------------------------------------------------------------------
#  Definicja obsługiwanego modelu + skróty
# ------------------------------------------------------------------
MODEL_CONFIGS = {
    "volt_sinus_pro_ultra_6000": {
        "name": "Volt Sinus PRO ULTRA 6000 (24V, 60A MPPT)",
        "default_slave": 4,
        "registers": registers
    }
}

SUPPORTED_MODELS = {k: v["name"] for k, v in MODEL_CONFIGS.items()}