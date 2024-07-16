import tkinter, win32api, win32con, pywintypes, time

label = tkinter.Label(text='3', font=('Arial Black','100'), fg='#ffffff', bg='#feffff', width=1)
label.master.overrideredirect(True)

#calculate the center of the screen
x = (label.winfo_screenwidth()/2) - (40)
x = round(x)
x_string = "+" + str(x)

label.master.geometry(x_string+"+100")
label.master.lift()
label.master.wm_attributes("-topmost", True)
label.master.wm_attributes("-disabled", True)
label.master.wm_attributes("-transparentcolor", "#feffff")

hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

label.pack()

timer = 4
while True:
    timer = timer -1
    if timer < 1:
        label.configure(text=str(timer))
        label.update()
        time.sleep(0.3)
        break

    label.configure(text=str(timer))
    label.update()
    label.update_idletasks()
    time.sleep(1)