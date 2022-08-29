import pyWinhook
import pythoncom

num_click = 0

def onclick(event):
    print(event.Position)
    global num_click
    num_click = num_click + 1
    return True

hm = pyWinhook.HookManager()
hm.SubscribeMouseAllButtonsDown(onclick)
hm.HookMouse()

while num_click < 2:
    pythoncom.PumpWaitingMessages()

hm.UnhookMouse()