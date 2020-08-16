import time
import win32api
import win32con
import win32gui


def find_window(title):
    print(title + "find...")
    title_hwnd = win32gui.FindWindow(None, title)
    return title_hwnd


def check_window(title, secs=5):
    global title_hwnd
    i = 0
    while i < secs:
        print(title + "checking..." + str(i) + "secs")
        time.sleep(1)
        title_hwnd = win32gui.FindWindow(None, title)
        if title_hwnd != 0:
            print(title + " is checked..." + str(i) + " secs")
            break
        i = i + 1

    return title_hwnd


def input_string(title, item_id, string, callback=None):
    print(title + "find...")
    title_hwnd = win32gui.FindWindow(None, title)
    print(title + " item find...")
    item_hwnd = win32gui.GetDlgItem(title_hwnd, item_id)
    for c in string:
        win32api.SendMessage(item_hwnd, win32con.WM_CHAR, ord(c), 0)
    if callback is not None and str(type(callback)) == "<class 'function'>":
        print("start " + callback)
        time.sleep(1)
        callback()

def click_item(title, item_id, callback=None):
    print(title + "find...")
    title_hwnd = win32gui.FindWindow(None, title)
    print(title + " item find...")
    item_hwnd = win32gui.GetDlgItem(title_hwnd, item_id)
    win32api.PostMessage(item_hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
    time.sleep(0.5)
    win32api.PostMessage(item_hwnd, win32con.WM_LBUTTONUP, 0, 0)
    time.sleep(2)
    if callback is not None and str(type(callback)) == "<class 'function'>":
        print("start " + callback)
        time.sleep(1)
        callback()

def close_win(title, secs=2):
    print(title + "find...")
    time.sleep(secs)
    title_hwnd = win32gui.FindWindow(None, title)
    win32gui.PostMessage(title_hwnd, win32con.WM_CLOSE, 0, 0)
    print(title + " is closed..")


