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
	print(f"\n Last: {scores[-1]:6.1f} ms")
	print(f"  Best:  {min(scores):6.1f} ms")
	print(f"  Average: {sum(scores)/len(scores):6.1f} ms")
	print(f"  Rounds:  {len(scores)}\n")
#----Round Logic----
def play_round(): #[Creates the play round action, turns lights off, grabs global, clears any presses from last round, game not active yet]
	global round_active, start_time

	all_off()
	response_flag.clear()
	round_active = False

	for distractor in (led_green, led_yellow, led_blue):
		distractor.on() #["Turn current light on"]
		sleep(uniform(0.2, 0.7)) #["Do nothing for a random decimal of seconds"]
		distractor.off() #["Turn current light off"]
		sleep(uniform(0.1, 0.4))

	sleep(uniform(0.6, 2.2)) #[Suspense]

	round_active = True #[Game ON]
	start_time = perf_counter() #[Start stopwatch]
	led_red.on()

	pressed = response_flag.wait(timeout=3.0)
	round_active  = False

	if pressed:
		show_stats()
	else:
		led_red.off()
		print("\n No response within 3 seconds. \n")

#----Entry Point----
def main():
	print("-" * 40)
	print(" Cognitive Response Timer")
	print(" Press button when the RED LED lights up.")
	print(" Ctrl+C to end session.")
	print("-" * 40 + "\n")

	try:
		while True:
			input(" Press Enter to start a round ")
			play_round()
	except KeyboardInterrupt:
		all_off()
		print("\n Session complete.")
		show_stats()

if __name__ == "__main__": #[This if check ensures main() only runs when you execute this file directly with python3 main.py — not if some other program ever imports it. ]
	main()
