"""
Smart Environment Monitor (Sense HAT) - Raspberry Pi Version

Runs on a Raspberry Pi with a physical Sense HAT.
Collects 10 samples of temperature or humidity, classifies comfort,
and scrolls a color-coded message on the LED matrix.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, List, Tuple

from sense_hat import SenseHat  # Physical Sense HAT on Raspberry Pi


RGB = Tuple[int, int, int]


@dataclass(frozen=True)
class AppConfig:
    samples: int = 10
    delay_seconds: float = 5.0
    scroll_speed: float = 0.10


COLORS: dict[str, RGB] = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
}


def classify_temperature_c(temp_c: float) -> tuple[str, RGB]:
    """Cold <15°C, Comfortable 15–22°C, Hot >22°C"""
    if temp_c > 22:
        return "Hot", COLORS["red"]
    if 15 <= temp_c <= 22:
        return "Comfortable", COLORS["green"]
    return "Cold", COLORS["blue"]


def classify_humidity_pct(humidity: float) -> tuple[str, RGB]:
    """Dry <55%, Sticky 55–65%, Oppressive >65%"""
    if humidity > 65:
        return "Oppressive", COLORS["red"]
    if 55 <= humidity <= 65:
        return "Sticky", COLORS["yellow"]
    return "Dry", COLORS["blue"]


def read_temperature_c(sense: SenseHat) -> float:
    """
    On real Sense HAT, there are a few ways to estimate temperature.
    Pressure-derived temperature tends to be stable.
    We fallback to the generic temperature read if needed.
    """
    try:
        return float(sense.get_temperature_from_pressure())
    except Exception:
        return float(sense.get_temperature())


def take_samples(
    read_fn: Callable[[], float],
    label: str,
    classify_fn: Callable[[float], tuple[str, RGB]],
    sense: SenseHat,
    cfg: AppConfig,
) -> List[float]:
    readings: List[float] = []

    for i in range(cfg.samples):
        value = round(read_fn(), 2)
        readings.append(value)

        status, color = classify_fn(value)
        print(f"{label} [{i+1}/{cfg.samples}]: {value} -> {status}")

        sense.show_message(status, text_colour=color, scroll_speed=cfg.scroll_speed)
        time.sleep(cfg.delay_seconds)

    return readings


def prompt_mode() -> str:
    print("What do you want to collect?")
    print("1. Temperature")
    print("2. Humidity")
    return input("Enter 1 or 2: ").strip()


def run_interactive() -> None:
    sense = SenseHat()
    cfg = AppConfig()

    while True:
        choice = prompt_mode()

        if choice == "1":
            print("\nCollecting Temperature Data...\n")
            temps = take_samples(
                read_fn=lambda: read_temperature_c(sense),
                label="Temperature (°C)",
                classify_fn=classify_temperature_c,
                sense=sense,
                cfg=cfg,
            )
            print("\nTemperature Readings:")
            print(temps)
            break

        if choice == "2":
            print("\nCollecting Humidity Data...\n")
            hums = take_samples(
                read_fn=sense.get_humidity,
                label="Humidity (%)",
                classify_fn=classify_humidity_pct,
                sense=sense,
                cfg=cfg,
            )
            print("\nHumidity Readings:")
            print(hums)
            break

        print("\nInvalid choice! Please enter 1 or 2.\n")


def main() -> None:
    try:
        run_interactive()
    except KeyboardInterrupt:
        print("\nStopped by user (Ctrl+C).")


if __name__ == "__main__":
    main()
