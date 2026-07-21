# reaction-timer #
Interrupt-driven GPIO reaction measurement system on a Raspberry Pi

# Cognitive Response Assessment Prototype #
An interrupt-driven GPIO reaction time measurement system built on Raspberry Pi 4, using Python and the `gpiozero` library. Measures stimulus-to-response latency with millisecond precision using hardware interrupts rather than polling.

## Medtech Relevance ##
Stimulus-response latency is a real, validated clinical measurement. Similar uses for reaction-time testing can be seen:
- **In concussion diagnostics** - protocols like Immediate Post-Concussion Assessment and Cognitive Testing (ImPACT) use reaction time in different methods as markers of neurological impairment after a head injury.
- Slowed movement due to **Parkinson's disease** can be partly assessed through reaction time changes over the course of disease progression.
- **Heavy machinery operator fitness testing** - reaction time benchmarks are used to assess alertness and fitness for safety-critical workplaces.

This project is a simplified hardware analog of that measurement principle:
- A randomized stimulus (the LED light)
- A physical response (button press)
- A precise latency calculation between the two ('elapsed_ms')

## Hardware ##

| Component | Quantity | Purpose |
|---|---|---|
| Raspberry Pi 4 | 1 | Compute + GPIO |
| LED (red) | 1 | Target stimulus |
| LED (green, yellow, blue) | 3 | Distractor sequence |
| 220Ω resistor | 4 | Current limiting for LEDs |
| Momentary push button | 1 | User response input |
| Breadboard + jumper wires | — | Circuit assembly |

## GPIO pin assignments (BCM numbering) ##

| Pin | Physical pin | Function |
|---|---|---|
| GPIO17 | 11 | Red LED (target) |
| GPIO27 | 13 | Green LED (distractor) |
| GPIO22 | 15 | Yellow LED (distractor) |
| GPIO23 | 16 | Blue LED (distractor) |
| GPIO24 | 18 | Push button (input, internal pull-up) |

## How it works ##

1. On round start, all LEDs turn off and any stale button state is cleared
2. Three distractor LEDs flash in sequence with randomized timing, to prevent the user from anticipating the target purely by rhythm
3. After a randomized pause, the red target LED turns on and a precision timer starts
4. A hardware interrupt — not a polling loop — detects the button press the instant it occurs, calculated via `perf_counter()` inside the interrupt callback itself to avoid OS thread-scheduling latency in the measurement
5. If no press occurs within 3 seconds, the round times out
6. Running statistics (last, best, average, round count) are recalculated and displayed after each round

## Engineering takeaways from this project ##
- **Interrupt-driven I/O**: `button.when_pressed` registers a callback that fires on a hardware-detected edge, rather than the CPU repeatedly checking pin state in a loop.
- **Hardware debouncing**: `bounce_time=0.05` filters out the mechanical bounce inherent to physical switch contacts, preventing a single press from being read as several.
- **Precision timing**: `time.perf_counter()` is used instead of `time.time()`, since it's a monotonic clock intended for measuring short, high-precision intervals.

## How to run

# Confirm the GPIO backend is available
python3 -c "from gpiozero import Device; from gpiozero.pins.lgpio import LGPIOFactory; Device.pin_factory = LGPIOFactory(); print('GPIO backend: ready')"

# Run the program
cd ~/projects/reaction-timer
python3 main.py

