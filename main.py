# main.py - Cognitive Response Assessment Prototype
# Interrupt-driven GPIO reaction measurement system

#[Pulling specific tools into the program]
from gpiozero import LED, Button
from threading import Event
from time import perf_counter, sleep
from random import uniform

# ----Hardware Setup (BCM pin numbers) [Represent physical hardware, connection between code and physical (Embedded!!!!)]----
led_red = LED(17)
led_green = LED(27)
led_yellow = LED(22)
led_blue = LED(23)
button = Button(24, pull_up=True, bounce_time=0.05)

#----State variables [Everything that changes as program runs]----
scores = []
round_active = False
start_time = 0.0
response_flag = Event()

#----interrupt callback----
def on_button_press(): #[defines function]
	if not round_active:
		return
	elapsed_ms = (perf_counter() - start_time) * 1000
	scores.append(elapsed_ms)
	led_red.off()
	response_flag.set()

button.when_pressed = on_button_press #[when gpiozero detects GPIO24 drop from hi to low(button touch), it autop calls on_buton_press() in background thread. Hardware event trigger, aka interrupt-driven]

#----Helpers----
def all_off():
	for led in (led_red, led_green, led_yellow, led_blue):
		led.off()

def show_stats():
	if not scores:
		return
	print(f"\n Last: {scores{-1}:6.1f} ms"
 	print(f"  Best:    {min(scores):6.1f} ms")
 	print(f"  Average: {sum(scores)/len(scores):6.1f} ms")
	 print(f"  Rounds:  {len(scores)}\n")
