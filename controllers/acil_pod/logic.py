"""State machine for the simulated ACIL-POD."""
from dataclasses import dataclass
from math import isfinite

DRIVE = {"W": (3.5, 3.5), "S": (-2.0, -2.0),
         "A": (-1.6, 1.6), "D": (1.6, -1.6)}
STOP_DISTANCE = 0.20
LEASE = 0.55
CLOSE_SETTLE = 0.8

@dataclass
class Pod:
    motion: str = ""
    until: float = 0.0
    lid_open: bool = False
    close_until: float = 0.0

    def step(self, now, distance, command=None):
        good = distance is not None and isfinite(distance) and 0.0 < distance <= 2.0
        safe = good and distance >= STOP_DISTANCE
        status = ""
        if self.motion and (not safe or now >= self.until):
            status = "ENGEL" if good and not safe else ("SENSOR" if not good else "KOMUT ZAMAN ASIMI")
            self.motion = ""
        if command == "X":
            self.motion = ""
            status = "DUR"
        elif command == "C":
            self.motion = ""
            self.lid_open = False
            self.close_until = now + CLOSE_SETTLE
            status = "KAPAK KAPANIYOR"
        elif command == "ENTER":
            if self.motion:
                self.motion = ""
                status = "ARAC DURDU; KODU YENIDEN GIRIN"
            elif now < self.close_until:
                status = "KAPAK HAREKET EDIYOR"
            else:
                self.lid_open = True
                status = "DOGRU DEMO KODU; KAPAK ACIK"
        elif command == "WRONG":
            self.motion = ""
            status = "YANLIS KOD; KAPAK KONUMU DEGISMEDI"
        elif command in DRIVE:
            if safe and not self.lid_open and now >= self.close_until:
                self.motion = command
                self.until = now + LEASE
            else:
                self.motion = ""
                status = "HAREKET ENGELLENDI"
        lock = not safe or self.lid_open or now < self.close_until
        rates = DRIVE.get(self.motion, (0.0, 0.0)) if not lock else (0.0, 0.0)
        return rates, (1.18 if self.lid_open else 0.0), status
