# Volt Inverter Hub for HASS

**Custom Integration for Home Assistant – Modbus RTU gateway to Volt Sinus PRO ULTRA 6 kW 24 V inverters**

*Poll your inverter every 1–30 s, expose more than 150 metrics, write set-points and toggle features – all from the Home Assistant UI.*

---

## ✨ Key features
| Category | What you get |
|-----------|--------------|
| **Sensors** | Real-time DC/AC voltages, currents, power (P / S / Q), frequencies, temperatures, MPPT data, energy counters (Wh & kWh)… |
| **Numbers** | Output-voltage & frequency set-points, charger/ discharger limits, alarm thresholds, max PV/grid currents, etc. |
| **Switches** | Search/eco mode, off-grid enable – instant ON/OFF with state verification. |
| **Selects** | Energy-use mode, charger-source priority, solar-use aim, battery/MPPT types… |
| **Per-entity polling** | Each register honours its own `interval` (1-30 s) – no wasted Modbus traffic. |
| **Config-flow UI** | Choose serial port, baud-rate, slave ID & model; edit options later in “Devices & Services → Configure”. |
| **Single-source map** | All registers live in **`const.py → registers`** – add a line, restart HA, done. |
| **Multi-model ready** | Add more models by dropping a new dict into `MODEL_CONFIGS`. |

---

## 🔧 Requirements
* Home Assistant **2024.2** or newer  
* `pymodbus ≥ 3.7.0` (installed automatically)  
* RS-485/USB adapter wired to the inverter’s COM port

---

## 🛠 Installation

### HACS (recommended)
1. In **HACS → Integrations → “＋” → *Custom repository***  
   * URL  `https://github.com/<your-github>/volt_inverter_hub_for_hass`  
   * Category  **Integration**
2. Install → **Restart Home Assistant**

### Manual
```bash
custom_components/
└── volt_inverter_hub_for_hass/
    ├── __init__.py
    ├── const.py
    ├── config_flow.py
    ├── coordinator.py
    ├── entities.py
    ├── manifest.json
    ├── services.yaml
    └── translations/
        ├── en.json
        └── pl.json

Copy the folder, restart HA.

⸻

🚀 Configuration
	1.	Settings → Devices & Services → “＋ Add Integration”
search for Volt Inverter Hub.
	2.	Fill in:
	•	Serial port – e.g. /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0
	•	Baud-rate (19200 by default)
	•	Slave ID (4 by default for Volt Sinus PRO ULTRA)
	•	Model – currently Volt Sinus PRO ULTRA 6000
	3.	Finish → the integration creates ~150 entities grouped under one device.

Need faster refresh for a single value?
Edit its dict in const.py and add e.g. "interval": 1 – the sensor will update every second while the rest stays at 10 s.

⸻

🧩 Extending

Add a new register

"pv_power": {
    "addr": 3102,
    "scale": 1,
    "unit": "W",
    "device_class": "power",
    "display_name": "PV power",
    "interval": 1,
    "is_write_reg": False
},

Add a writable number / select / switch
	•	set "is_write_reg": True
	•	for Number add min, max, step
	•	for Select add "options": {raw: "Label", …}
	•	for Switch add "type": "switch" and optional "write_values": {0: "OFF", 1: "ON"}

Support another inverter model

MODEL_CONFIGS["my_new_model"] = {
    "name": "Awesome Inverter 3 kW",
    "default_slave": 2,
    "registers": { … }
}


⸻

🗒 Troubleshooting

logger:
  logs:
    custom_components.volt_inverter_hub_for_hass: debug
    pymodbus.client: debug

	•	Watch the log for CRC/time-out errors → check wiring & grounding.
	•	Wrong values? Verify address/scale against the manufacturer’s register list.

⸻

🤝 Contributing

Pull-requests with additional models, bug-fixes or translations are welcome!
Create an issue or fork the repo and submit a PR.

⸻

© License

Released under the MIT License.  See LICENSE for details.

⸻

Enjoy full insight and control over your Volt Sinus inverter – natively in Home Assistant!