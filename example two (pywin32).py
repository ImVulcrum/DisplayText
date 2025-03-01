import win32api, win32con, win32gui, win32ui, ctypes

counter = 3
TIMER_ID = 1  # Define the timer ID

def start_timer():
    hInstance = win32api.GetModuleHandle()
    className = 'MyWindowClassName'

    wndClass = win32gui.WNDCLASS()
    wndClass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wndClass.lpfnWndProc = wndProc
    wndClass.hInstance = hInstance
    wndClass.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
    wndClass.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
    wndClass.lpszClassName = className
    wndClassAtom = win32gui.RegisterClass(wndClass)

    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    style = win32con.WS_DISABLED | win32con.WS_POPUP | win32con.WS_VISIBLE

    hWindow = win32gui.CreateWindowEx(
        exStyle,
        wndClassAtom,
        None,
        style,
        0,
        0,
        win32api.GetSystemMetrics(win32con.SM_CXSCREEN),
        win32api.GetSystemMetrics(win32con.SM_CYSCREEN),
        None,
        None,
        hInstance,
        None
    )

    win32gui.SetLayeredWindowAttributes(hWindow, 0x00ffffff, 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
    win32gui.SetWindowPos(hWindow, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

    # Set a timer to trigger every 1000 milliseconds (1 second)
    ctypes.windll.user32.SetTimer(hWindow, TIMER_ID, 1000, None)

    win32gui.PumpMessages()

def wndProc(hWnd, message, wParam, lParam):
    global counter

    if message == win32con.WM_PAINT:
        hdc, paintStruct = win32gui.BeginPaint(hWnd)

        dpiScale = win32ui.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 60.0
        fontSize = 120

        lf = win32gui.LOGFONT()
        lf.lfFaceName = "Arial Black"
        lf.lfHeight = int(round(dpiScale * fontSize))
        hf = win32gui.CreateFontIndirect(lf)
        win32gui.SelectObject(hdc, hf)

        # Set text color to white (RGB: 255, 255, 254)
        win32gui.SetTextColor(hdc, win32api.RGB(255, 255, 254))

        rect = win32gui.GetClientRect(hWnd)
        screen_height = rect[3]
        lower_third_top = int(screen_height * 2 / 4)
        rect = (rect[0], lower_third_top, rect[2], screen_height)

        win32gui.DrawText(
            hdc,
            str(counter),
            -1,
            rect,
            win32con.DT_CENTER | win32con.DT_NOCLIP | win32con.DT_SINGLELINE | win32con.DT_VCENTER
        )
        win32gui.EndPaint(hWnd, paintStruct)
        return 0

    elif message == win32con.WM_TIMER:
        if wParam == TIMER_ID:  # Check if the timer ID matches
            counter -= 1
            if counter < 0:
                win32gui.PostQuitMessage(0)
            else:
                win32gui.InvalidateRect(hWnd, None, True)
        return 0

    elif message == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0

    else:
        return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

if __name__ == '__main__':
    main()
