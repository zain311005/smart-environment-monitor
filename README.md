# Smart Environment Monitor (Sense HAT)

## Project Documentation

A Python-based IoT application developed for the Raspberry Pi that uses the **Sense HAT** to monitor **temperature** and **humidity**, classify indoor comfort levels, and provide real-time visual feedback using the 8×8 LED matrix.

**Control Loop:**  
**Sense → Classify → Display**

---

## 1. Project Overview

This project monitors indoor environmental conditions using a physical Raspberry Pi Sense HAT.

When the program runs, the user selects whether to monitor **temperature** or **humidity**. The system then:

- Collects **10 sensor readings** (to ensure data stability)
- Rounds and stores each reading
- Classifies the readings using predefined comfort thresholds
- Displays a **color-coded scrolling message** on the Sense HAT LED matrix
- Prints the full list of readings to the terminal

---

## 2. Features

### Temperature Comfort Classification
- **Cold:** `< 15°C` (Blue LED)
- **Comfortable:** `15–22°C` (Green LED)
- **Hot:** `> 22°C` (Red LED)

### Humidity Comfort Classification
- **Dry:** `< 55%`
- **Sticky:** `55–65%`
- **Oppressive:** `> 65%`

### User Feedback
- Interactive command-line menu
- LED matrix scrolling messages with color-coded feedback
- Console output showing all collected sensor readings

---

## 3. Tech Stack

- **Programming Language:** Python 3
- **Hardware Platform:** Raspberry Pi (3, 4, or Zero W)
- **Sensor Module:** Raspberry Pi Sense HAT
- **Library:** `sense_hat`

---

## 4. Project Structure

```
smart-environment-monitor/
├─ src/
│  ├─ smart_environment_monitor.py
│  └─ __init__.py
├─ docs/
│  └─ sense-hat-report.docx
├─ assets/
│  └─ images/
├─ README.md
├─ requirements.txt
└─ LICENSE
```

---

## 5. Installation & Setup

1. Update the system:
   ```bash
   sudo apt update
   ```

2. Install the Sense HAT library (via apt, not pip):
   ```bash
   sudo apt install -y sense-hat
   ```

3. Install project dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Run the program:
   ```bash
   python3 src/smart_environment_monitor.py
   ```

---

## 6. Usage Example

1. Run the script and choose a mode from the menu.
2. The terminal logs the data collection process.
3. The Sense HAT LED matrix scrolls the comfort status using the corresponding color.

---

## Sample Terminal Output

```
--------------------------------
 Smart Environment Monitor
--------------------------------
[1] Monitor Temperature
[2] Monitor Humidity
[Q] Quit

Select an option: 1
Collecting 10 readings...

Reading 1: 21.5 °C
Reading 2: 21.6 °C
...
Reading 10: 21.5 °C

Status: Comfortable (Scrolling Green on LED Matrix)
```

