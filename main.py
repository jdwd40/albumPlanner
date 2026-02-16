#!/usr/bin/env python3
import tkinter as tk
import sys

def main():
    try:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    except ImportError:
        print("tkinterdnd2 not available, drag-and-drop from file manager disabled")
        root = tk.Tk()

    root.title("Album Planner")
    root.geometry("900x600")
    root.minsize(700, 450)

    from theme import apply_theme
    apply_theme(root)

    from app import App
    App(root)

    root.mainloop()


if __name__ == "__main__":
    main()
