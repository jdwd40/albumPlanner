import tkinter as tk
from tkinter import ttk

COLORS = {
    "bg": "#1e1e2e",
    "bg_light": "#313244",
    "bg_surface": "#45475a",
    "text": "#cdd6f4",
    "text_dim": "#a6adc8",
    "accent": "#89b4fa",
    "green": "#a6e3a1",
    "yellow": "#f9e2af",
    "red": "#f38ba8",
    "border": "#585b70",
}


def apply_theme(root: tk.Tk):
    root.configure(bg=COLORS["bg"])
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(".", background=COLORS["bg"], foreground=COLORS["text"],
                     fieldbackground=COLORS["bg_light"], bordercolor=COLORS["border"],
                     insertcolor=COLORS["text"])

    style.configure("TFrame", background=COLORS["bg"])
    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"])
    style.configure("TButton", background=COLORS["bg_surface"], foreground=COLORS["text"],
                     padding=(10, 5))
    style.map("TButton",
              background=[("active", COLORS["accent"]), ("disabled", COLORS["bg_light"])],
              foreground=[("active", COLORS["bg"]), ("disabled", COLORS["text_dim"])])

    style.configure("Accent.TButton", background=COLORS["accent"], foreground=COLORS["bg"],
                     font=("Segoe UI", 11, "bold"), padding=(14, 8))
    style.map("Accent.TButton",
              background=[("active", "#b4d0fb"), ("disabled", COLORS["bg_surface"])],
              foreground=[("disabled", COLORS["text_dim"])])

    style.configure("TEntry", fieldbackground=COLORS["bg_light"], foreground=COLORS["text"],
                     insertcolor=COLORS["text"], padding=5)

    style.configure("Treeview", background=COLORS["bg_light"], foreground=COLORS["text"],
                     fieldbackground=COLORS["bg_light"], rowheight=28,
                     borderwidth=0)
    style.configure("Treeview.Heading", background=COLORS["bg_surface"],
                     foreground=COLORS["text"], font=("Segoe UI", 9, "bold"))
    style.map("Treeview",
              background=[("selected", COLORS["bg_surface"])],
              foreground=[("selected", COLORS["accent"])])

    style.configure("Surface.TFrame", background=COLORS["bg_light"])
    style.configure("Surface.TLabel", background=COLORS["bg_light"], foreground=COLORS["text"])
    style.configure("Dim.TLabel", background=COLORS["bg"], foreground=COLORS["text_dim"])
    style.configure("Header.TLabel", background=COLORS["bg"], foreground=COLORS["text"],
                     font=("Segoe UI", 18, "bold"))
    style.configure("Warning.TLabel", background=COLORS["bg"], foreground=COLORS["red"],
                     font=("Segoe UI", 10, "bold"))
