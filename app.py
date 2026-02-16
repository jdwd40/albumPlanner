import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from theme import COLORS
from models import AlbumProject
from track_list import TrackList
from album_service import export_album
from project_io import save_project, load_project


class App(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.project = AlbumProject()
        self.output_dir: str = ""
        self.pack(fill="both", expand=True)
        self._build_ui()
        self._update_duration()

    def _build_ui(self):
        # Header
        header = ttk.Label(self, text="Album Planner", style="Header.TLabel")
        header.pack(fill="x", padx=15, pady=(12, 4))

        # Main container
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=10, pady=5)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=0)
        main.rowconfigure(0, weight=1)

        # Left panel
        left = ttk.Frame(main)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left.rowconfigure(0, weight=1)
        left.columnconfigure(0, weight=1)

        self.track_list = TrackList(left, on_change=self._on_tracks_changed)
        self.track_list.grid(row=0, column=0, sticky="nsew")

        btn_frame = ttk.Frame(left)
        btn_frame.grid(row=1, column=0, sticky="ew", pady=(2, 5))
        ttk.Button(btn_frame, text="Remove Selected",
                   command=self.track_list.remove_selected).pack(side="left")

        # Right panel
        right = ttk.Frame(main, width=250)
        right.grid(row=0, column=1, sticky="ns", padx=(5, 0))
        right.grid_propagate(False)
        right.configure(width=250)

        # Album details
        ttk.Label(right, text="Album Details", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=10, pady=(10, 5))

        ttk.Label(right, text="Band Name:", style="Dim.TLabel").pack(anchor="w", padx=10)
        self.band_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.band_var).pack(fill="x", padx=10, pady=(0, 5))

        ttk.Label(right, text="Album Name:", style="Dim.TLabel").pack(anchor="w", padx=10)
        self.album_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.album_var).pack(fill="x", padx=10, pady=(0, 10))

        # Duration section
        sep = ttk.Separator(right, orient="horizontal")
        sep.pack(fill="x", padx=10, pady=5)
        ttk.Label(right, text="Duration", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=10, pady=(5, 5))

        dur_frame = ttk.Frame(right)
        dur_frame.pack(fill="x", padx=10)
        self.total_label = ttk.Label(dur_frame, text="Total:     0:00")
        self.total_label.pack(anchor="w")
        self.remaining_label = ttk.Label(dur_frame, text="Remaining: 80:00")
        self.remaining_label.pack(anchor="w")
        self.limit_label = ttk.Label(dur_frame, text="Limit:     80:00", style="Dim.TLabel")
        self.limit_label.pack(anchor="w")

        # Progress bar canvas
        self.bar_canvas = tk.Canvas(right, height=20, bg=COLORS["bg_light"],
                                     highlightthickness=0)
        self.bar_canvas.pack(fill="x", padx=10, pady=(8, 2))

        self.warning_label = ttk.Label(right, text="", style="Warning.TLabel")
        self.warning_label.pack(anchor="w", padx=10)

        # Output folder
        ttk.Separator(right, orient="horizontal").pack(fill="x", padx=10, pady=10)

        ttk.Button(right, text="Select Output Folder",
                   command=self._select_output).pack(fill="x", padx=10)
        self.folder_label = ttk.Label(right, text="No folder selected", style="Dim.TLabel",
                                       wraplength=220)
        self.folder_label.pack(anchor="w", padx=10, pady=(2, 8))

        # Create album button
        self.create_btn = ttk.Button(right, text="CREATE ALBUM", style="Accent.TButton",
                                      command=self._create_album)
        self.create_btn.pack(fill="x", padx=10, pady=(0, 10))

        # Save / Load
        ttk.Separator(right, orient="horizontal").pack(fill="x", padx=10, pady=5)
        sl_frame = ttk.Frame(right)
        sl_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(sl_frame, text="Save", command=self._save).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ttk.Button(sl_frame, text="Load", command=self._load).pack(side="left", expand=True, fill="x", padx=(3, 0))

        # Try DnD setup
        try:
            self.track_list.setup_dnd(self.track_list)
            self.track_list.setup_dnd(self.track_list.drop_frame)
        except Exception:
            pass

    def _on_tracks_changed(self):
        self.project.tracks = self.track_list.tracks
        self._update_duration()

    def _update_duration(self):
        total = self.project.total_duration
        rem = self.project.remaining
        t_min, t_sec = divmod(int(total), 60)
        r_min, r_sec = divmod(int(rem), 60)
        self.total_label.configure(text=f"Total:     {t_min}:{t_sec:02d}")
        self.remaining_label.configure(text=f"Remaining: {r_min}:{r_sec:02d}")

        # Progress bar
        self.bar_canvas.delete("all")
        w = self.bar_canvas.winfo_width() or 220
        ratio = min(total / 4800.0, 1.0)
        fill_w = int(w * ratio)

        if total > 4800:
            color = COLORS["red"]
        elif total > 3600:
            color = COLORS["yellow"]
        else:
            color = COLORS["green"]

        self.bar_canvas.create_rectangle(0, 0, fill_w, 20, fill=color, outline="")

        # Warning
        if self.project.over_limit:
            over = total - 4800
            o_min, o_sec = divmod(int(over), 60)
            self.warning_label.configure(text=f"Over limit by {o_min}:{o_sec:02d}")
        else:
            self.warning_label.configure(text="")

        # Create button state
        has_tracks = len(self.project.tracks) > 0
        self.create_btn.state(["!disabled"] if has_tracks else ["disabled"])

    def _select_output(self):
        d = filedialog.askdirectory(title="Select Output Folder")
        if d:
            self.output_dir = d
            self.folder_label.configure(text=d)

    def _create_album(self):
        self.project.band_name = self.band_var.get()
        self.project.album_name = self.album_var.get()

        if not self.project.album_name.strip():
            messagebox.showwarning("Missing info", "Enter an album name.", parent=self.root)
            return
        if not self.output_dir:
            self._select_output()
            if not self.output_dir:
                return

        try:
            created = export_album(self.project, Path(self.output_dir))
            messagebox.showinfo(
                "Done",
                f"Album created with {len(created)} tracks:\n{Path(self.output_dir) / self.project.album_name}",
                parent=self.root,
            )
        except ValueError as e:
            messagebox.showerror("Export error", str(e), parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    def _save(self):
        self.project.band_name = self.band_var.get()
        self.project.album_name = self.album_var.get()
        result = save_project(self.project, parent=self.root)
        if result:
            messagebox.showinfo("Saved", f"Project saved to:\n{result}", parent=self.root)

    def _load(self):
        proj = load_project(parent=self.root)
        if proj is None:
            return
        self.project = proj
        self.band_var.set(proj.band_name)
        self.album_var.set(proj.album_name)
        self.track_list.tracks = list(proj.tracks)
        self.track_list._refresh()
