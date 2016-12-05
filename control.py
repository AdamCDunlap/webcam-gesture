#!/usr/bin/env python2

import autopy
import platform

OS_MAC = 'Darwin' in platform.system()

def next_tab():
    if OS_MAC:
        autopy.key.tap(long(autopy.key.K_RIGHT),
                       long(autopy.key.MOD_ALT)|long(autopy.key.MOD_META))
    else:
        autopy.key.tap(autopy.key.K_PAGEUP,
                       autopy.key.MOD_CONTROL)

def prev_tab():
    if OS_MAC:
        autopy.key.tap(long(autopy.key.K_LEFT),
                       long(autopy.key.MOD_ALT)|long(autopy.key.MOD_META))
    else:
        autopy.key.tap(autopy.key.K_PAGEDOWN,
                       autopy.key.MOD_CONTROL)

def close_tab():
    if OS_MAC:
        autopy.key.tap(u'w', long(autopy.key.MOD_META))
    else:
        autopy.key.tap(autopy.key.K_F4, autopy.key.MOD_CONTROL)

def reopen_tab():
    if OS_MAC:
        autopy.key.tap(u't',
                       long(autopy.key.MOD_SHIFT)|long(autopy.key.MOD_META))

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
    time.sleep(1)
    reopen_tab()
    time.sleep(1)
    click_at_loc(50,50)

if __name__ == '__main__':
    test()
