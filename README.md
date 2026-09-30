# reaction-timer #
Interrupt-driven GPIO reaction measurement system on a Raspberry Pi

# Cognitive Response Assessment Prototype #
Measures stimulus-to-response latency using edge-triggered GPIO callbacks (interrupt-driven) rather than a polling loop. Timing resolution has not been characterized.

<img width="400" height="400" alt="Reaction-game" src="https://github.com/user-attachments/assets/e5a4e2bd-7987-4ab9-9993-50b15930764b" />


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

1. On round start, all LEDs turn off and any stale button state is cleared.
2. Three distractor LEDs flash in sequence with randomized timing, to prevent the user from anticipating the target purely by rhythm.
3. After a randomized pause, the red target LED turns on and a precision timer starts.
4. The GPIO library detects the button press as a falling edge and runs a callback on a background thread, so the program never polls the pin. The callback reads perf_counter() right away. That keeps the delay of waking the main loop out of the measurement, but OS scheduling latency is still included.
5. If no press occurs within 3 seconds, the round times out.
6. Running statistics (last, best, average, round count) are recalculated and displayed after each round.

## Engineering takeaways from this project ##
- **Interrupt-driven I/O**: `button.when_pressed` registers a callback that fires on a hardware-detected edge, rather than the CPU repeatedly checking pin state in a loop.
- **Software debouncing**: `bounce_time=0.05` tells the GPIO library to ignore a press until the pin has been stable for 50 ms. This filters out the mechanical bounce of the switch contacts, so one press isn't read as several.
- **Precision timing**: `time.perf_counter()` is used instead of `time.time()`, since it's a monotonic clock intended for measuring short, high-precision intervals.

## How to run

# Confirm the GPIO backend is available
python3 -c "from gpiozero import Device; from gpiozero.pins.lgpio import LGPIOFactory; Device.pin_factory = LGPIOFactory(); print('GPIO backend: ready')"

# Run the program
cd ~/projects/reaction-timer
python3 main.py

