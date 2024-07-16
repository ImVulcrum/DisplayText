import display_text
from time import sleep

for i in range(5):
    print("-")
    display_text.clear_screen()
    display_text.display(str(i))
    sleep(1)