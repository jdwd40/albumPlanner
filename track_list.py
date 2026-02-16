import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from models import Track
from theme import COLORS


class TrackList(ttk.Frame):
    """Reorderable track list with drop zone, treeview, and remove button."""

    def __init__(self, parent, on_change=None):
        super().__init__(parent)
        self.tracks: list[Track] = []
        self.on_change = on_change  # callback when tracks change
        self._drag_source = None
        self._build_ui()

    def _build_ui(self):
        # Drop zone
        self.drop_frame = tk.Frame(self, bg=COLORS["bg_surface"], cursor="hand2",
                                    highlightbackground=COLORS["border"],
                                    highlightthickness=2, height=60)
        self.drop_frame.pack(fill="x", padx=5, pady=(5, 5))
        self.drop_frame.pack_propagate(False)
        self.drop_label = tk.Label(self.drop_frame, text="Drag MP3s here or click to add",
                                    bg=COLORS["bg_surface"], fg=COLORS["text_dim"],
                                    font=("Segoe UI", 10))
        self.drop_label.pack(expand=True)
        self.drop_frame.bind("<Button-1>", self._on_click_add)
        self.drop_label.bind("<Button-1>", self._on_click_add)

        # Treeview
        columns = ("num", "title", "duration", "filename", "remove")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="extended")
        self.tree.heading("num", text="#")
        self.tree.heading("title", text="Title")
        self.tree.heading("duration", text="Duration")
        self.tree.heading("filename", text="Original File")
        self.tree.heading("remove", text="")
        self.tree.column("num", width=40, minwidth=40, stretch=False)
        self.tree.column("title", width=200, minwidth=100)
        self.tree.column("duration", width=70, minwidth=60, stretch=False)
        self.tree.column("filename", width=150, minwidth=80)
        self.tree.column("remove", width=30, minwidth=30, stretch=False)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        scrollbar.pack(side="left", fill="y", pady=5)

        # Empty state
        self.empty_label = tk.Label(self, text="Drop MP3 files to begin",
                                     bg=COLORS["bg"], fg=COLORS["text_dim"],
                                     font=("Segoe UI", 11))

        # Drag reorder bindings
        self.tree.bind("<ButtonPress-1>", self._on_press)
        self.tree.bind("<B1-Motion>", self._on_drag)
        self.tree.bind("<ButtonRelease-1>", self._on_release)
        # Click-to-remove on last column
        self.tree.bind("<Button-1>", self._on_tree_click, add=True)

        self._update_empty_state()

    def _on_click_add(self, event=None):
        files = filedialog.askopenfilenames(
            title="Select MP3 files",
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        if files:
            self.add_files(files)

    def add_files(self, paths):
        """Add MP3 files from a list of paths."""
        for p in paths:
            p = p.strip().strip("{}")
            if not p.lower().endswith(".mp3"):
                messagebox.showwarning("Invalid file", f"Not an MP3:\n{Path(p).name}")
                continue
            if not Path(p).exists():
                messagebox.showwarning("Missing file", f"File not found:\n{p}")
                continue
            try:
                track = Track.from_file(p)
                self.tracks.append(track)
            except Exception as e:
                messagebox.showerror("Error", f"Could not read:\n{Path(p).name}\n{e}")
        self._refresh()

    def remove_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        indices = sorted([self.tree.index(s) for s in sel], reverse=True)
        for i in indices:
            self.tracks.pop(i)
        self._refresh()

    def _on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        col = self.tree.identify_column(event.x)
        if col == "#5" and region == "cell":  # remove column
            item = self.tree.identify_row(event.y)
            if item:
                idx = self.tree.index(item)
                self.tracks.pop(idx)
                self._refresh()

    # --- Drag reorder ---
    def _on_press(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self._drag_source = item

    def _on_drag(self, event):
        if not self._drag_source:
            return
        target = self.tree.identify_row(event.y)
        if target and target != self._drag_source:
            src_idx = self.tree.index(self._drag_source)
            dst_idx = self.tree.index(target)
            track = self.tracks.pop(src_idx)
            self.tracks.insert(dst_idx, track)
            self._refresh()
            # re-find the moved item
            children = self.tree.get_children()
            if dst_idx < len(children):
                self._drag_source = children[dst_idx]

    def _on_release(self, event):
        self._drag_source = None

    # --- Display ---
    def _refresh(self):
        self.tree.delete(*self.tree.get_children())
        for i, t in enumerate(self.tracks, 1):
            mins, secs = divmod(int(t.duration_secs), 60)
            self.tree.insert("", "end", values=(
                f"{i:02d}",
                t.title,
                f"{mins}:{secs:02d}",
                t.original_filename,
                "\u2715"
            ))
        self._update_empty_state()
        if self.on_change:
            self.on_change()

    def _update_empty_state(self):
        if not self.tracks:
            self.empty_label.place(relx=0.5, rely=0.6, anchor="center")
        else:
            self.empty_label.place_forget()

    def setup_dnd(self, widget):
        """Bind tkinterdnd2 drop to a widget."""
        try:
            widget.drop_target_register("DND_Files")
            widget.dnd_bind("<<Drop>>", self._on_dnd_drop)
            widget.dnd_bind("<<DragEnter>>", self._on_drag_enter)
            widget.dnd_bind("<<DragLeave>>", self._on_drag_leave)
        except Exception:
            pass  # tkinterdnd2 not available

    def _on_dnd_drop(self, event):
        self._on_drag_leave(event)
        data = event.data
        # tkinterdnd2 returns space-separated paths, braces around paths with spaces
        paths = self._parse_dnd_data(data)
        self.add_files(paths)

    def _on_drag_enter(self, event):
        self.drop_frame.configure(highlightbackground=COLORS["accent"])

    def _on_drag_leave(self, event):
        self.drop_frame.configure(highlightbackground=COLORS["border"])

    @staticmethod
    def _parse_dnd_data(data: str) -> list[str]:
        paths = []
        i = 0
        while i < len(data):
            if data[i] == "{":
                end = data.index("}", i)
                paths.append(data[i + 1:end])
                i = end + 2
            elif data[i] == " ":
                i += 1
            else:
                end = data.find(" ", i)
                if end == -1:
                    end = len(data)
                paths.append(data[i:end])
                i = end + 1
        return paths
