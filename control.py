#!/usr/bin/env python2

import autopy

def next_tab():
    autopy.key.tap(autopy.key.K_PAGEUP, autopy.key.MOD_CONTROL)

def prev_tab():
    autopy.key.tap(autopy.key.K_PAGEDOWN, autopy.key.MOD_CONTROL)

def close_tab():
    autopy.key.tap(autopy.key.K_F4, autopy.key.MOD_CONTROL)

def click_at_loc(x,y):
    autopy.mouse.move(x, y)
    autopy.mouse.click()

def test():
    import time

    time.sleep(2)
    next_tab()
    time.sleep(1)
    prev_tab()
    time.sleep(1)
    close_tab()

if __name__ == '__main__':
    test()
