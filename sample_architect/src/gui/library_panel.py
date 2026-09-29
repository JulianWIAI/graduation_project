import pathlib
import tkinter as tk
from tkinter import filedialog, ttk

from src.analysis.library_scanner import LibraryScanner
from src.data.database import Database
from src.gui import styles


class LibraryPanel(tk.Frame):
    """Left sidebar — folder picker, scan control, library stats."""

    WIDTH = 300

    def __init__(self, parent, db: Database):
        super().__init__(parent, bg=styles.BG1, width=self.WIDTH)
        self.pack_propagate(False)
        self._db      = db
        self._scanner = LibraryScanner(db)
        self._folder_var = tk.StringVar()
        self._build()
        self._update_stats()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build(self):
        # ── App title ─────────────────────────────────────────────────────────
        title_bar = tk.Frame(self, bg=styles.BG0)
        title_bar.pack(fill='x')
        tk.Label(title_bar, text='Sample', fg=styles.ORANGE, bg=styles.BG0,
                 font=('Segoe UI', 16, 'bold')).pack(side='left', padx=(16, 0), pady=14)
        tk.Label(title_bar, text='Architect', fg=styles.PINK, bg=styles.BG0,
                 font=('Segoe UI', 16, 'bold')).pack(side='left', pady=14)

        self._divider()

        # ── Library section ───────────────────────────────────────────────────
        self._section('YOUR LIBRARY', styles.TXT_MED)

        # Folder picker
        folder_lbl_row = tk.Frame(self, bg=styles.BG1)
        folder_lbl_row.pack(fill='x', padx=16)
        tk.Label(folder_lbl_row, text='Sample Folder', fg=styles.TXT_MED, bg=styles.BG1,
                 font=('Segoe UI', 9)).pack(side='left', pady=(0, 4))

        folder_row = tk.Frame(self, bg=styles.BG4)
        folder_row.pack(fill='x', padx=16)

        self._folder_entry = tk.Entry(
            folder_row, textvariable=self._folder_var,
            bg=styles.BG4, fg=styles.TXT_BRT,
            insertbackground=styles.CYAN, relief='flat',
            font=('Segoe UI', 9), bd=6,
        )
        self._folder_entry.pack(side='left', fill='x', expand=True)

        tk.Button(
            folder_row, text='Browse', command=self._browse,
            bg=styles.BG4, fg=styles.CYAN, relief='flat',
            font=('Segoe UI', 9, 'bold'), cursor='hand2', bd=0,
            padx=10, activebackground=styles.BG5, activeforeground=styles.GREEN,
        ).pack(side='right')

        # Scan button
        self._scan_btn = tk.Button(
            self, text='⟳  Scan / Update Library',
            command=self._scan,
            bg=styles.ORANGE, fg=styles.BG0, relief='flat',
            font=('Segoe UI', 10, 'bold'), cursor='hand2', bd=0,
            pady=10, activebackground=styles.YELLOW, activeforeground=styles.BG0,
        )
        self._scan_btn.pack(fill='x', padx=16, pady=(10, 6))

        # Progress bar
        self._progress = ttk.Progressbar(self, mode='determinate',
                                          style='SA.Horizontal.TProgressbar')
        self._progress.pack(fill='x', padx=16)

        self._progress_lbl = tk.Label(
            self, text='', fg=styles.TXT_MED, bg=styles.BG1,
            font=('Segoe UI', 8), anchor='w', wraplength=260, justify='left',
        )
        self._progress_lbl.pack(fill='x', padx=16, pady=(3, 0))

        # Hint shown when library is empty
        self._hint_lbl = tk.Label(
            self,
            text='Point to a folder of samples and click Scan.\nWAV · MP3 · FLAC · AIFF supported.',
            fg=styles.TXT_DIM, bg=styles.BG1,
            font=('Segoe UI', 8), justify='left', anchor='w',
        )
        self._hint_lbl.pack(fill='x', padx=16, pady=(6, 0))

        self._divider()

        # ── Stats ─────────────────────────────────────────────────────────────
        self._section('LIBRARY STATS', styles.TXT_MED)

        self._stats_lbl = tk.Label(
            self, text='No samples scanned yet',
            fg=styles.TXT_BRT, bg=styles.BG1,
            font=('Segoe UI', 10, 'bold'), anchor='w',
        )
        self._stats_lbl.pack(fill='x', padx=16, pady=(0, 8))

        self._role_frame = tk.Frame(self, bg=styles.BG1)
        self._role_frame.pack(fill='x', padx=16)

        self._divider()

        # ── Browse button ─────────────────────────────────────────────────────
        tk.Button(
            self, text='Browse All Samples  →',
            command=self._open_browser,
            bg=styles.BG3, fg=styles.CYAN, relief='flat',
            font=('Segoe UI', 10, 'bold'), cursor='hand2', bd=0,
            pady=10, activebackground=styles.BG4, activeforeground=styles.GREEN,
        ).pack(fill='x', padx=16, pady=(0, 16))

    def _section(self, text: str, color: str):
        tk.Label(self, text=text, fg=color, bg=styles.BG1,
                 font=('Segoe UI', 8, 'bold'), anchor='w'
                 ).pack(fill='x', padx=16, pady=(12, 6))

    def _divider(self):
        tk.Frame(self, bg=styles.BG4, height=1).pack(fill='x', padx=0, pady=4)

    # ── Actions ───────────────────────────────────────────────────────────────

    def _browse(self):
        folder = filedialog.askdirectory(title='Select your sample folder')
        if folder:
            self._folder_var.set(folder)

    def _scan(self):
        folder_str = self._folder_var.get().strip()
        if not folder_str:
            self._progress_lbl.config(text='Please choose a folder first.')
            return
        folder = pathlib.Path(folder_str)
        if not folder.is_dir():
            self._progress_lbl.config(text='Folder not found — check the path.')
            return

        self._scan_btn.config(state='disabled', text='Scanning…')
        self._progress['value'] = 0
        self._hint_lbl.config(text='')
        self._progress_lbl.config(text='Starting scan…')

        def progress_cb(current, total, filename):
            self.after(0, self._on_progress, current, total, filename)

        def done_cb(added, skipped, errors):
            self.after(0, self._on_done, added, skipped, errors)

        self._scanner.scan(folder, progress_cb=progress_cb, done_cb=done_cb)

    def _on_progress(self, current: int, total: int, filename: str):
        self._progress['value'] = (current / total * 100) if total else 0
        self._progress_lbl.config(text=f'{filename}  ({current} of {total})')

    def _on_done(self, added: int, skipped: int, errors: int):
        self._progress['value'] = 100
        self._progress_lbl.config(
            text=f'Done!  +{added} new  ·  {skipped} already known  ·  {errors} errors'
        )
        self._scan_btn.config(state='normal', text='⟳  Scan / Update Library')
        self._update_stats()

    # ── Stats rendering ───────────────────────────────────────────────────────

    def _update_stats(self):
        stats = self._db.get_stats()
        total  = sum(stats.values())
        n_roles = len([v for v in stats.values() if v > 0])

        if total == 0:
            self._stats_lbl.config(text='No samples scanned yet')
            self._hint_lbl.config(
                text='Point to a folder of samples and click Scan.\nWAV · MP3 · FLAC · AIFF supported.'
            )
        else:
            self._stats_lbl.config(text=f'{total:,} samples  ·  {n_roles} roles')
            self._hint_lbl.config(text='')

        for w in self._role_frame.winfo_children():
            w.destroy()

        if not stats:
            return

        max_count = max(stats.values())
        for role in styles.ALL_ROLES + ['drums', 'perc']:
            cnt = stats.get(role, 0)
            if cnt == 0:
                continue
            color = styles.ROLE_COLORS.get(role, styles.TXT_MED)
            row = tk.Frame(self._role_frame, bg=styles.BG1)
            row.pack(fill='x', pady=2)

            tk.Label(row, text=role.ljust(10), fg=color, bg=styles.BG1,
                     font=('Segoe UI', 9, 'bold'), width=10, anchor='w').pack(side='left')

            # Mini bar
            bar_outer = tk.Frame(row, bg=styles.BG4, height=6, width=120)
            bar_outer.pack(side='left', padx=(4, 6))
            bar_outer.pack_propagate(False)
            fill_w = max(4, int((cnt / max_count) * 120))
            tk.Frame(bar_outer, bg=color, height=6, width=fill_w).pack(side='left')

            tk.Label(row, text=str(cnt), fg=styles.TXT_MED, bg=styles.BG1,
                     font=('Segoe UI', 9), anchor='w').pack(side='left')

    def _open_browser(self):
        from src.gui.library_browser import LibraryBrowser
        LibraryBrowser(self, self._db)

    def refresh_stats(self):
        self._update_stats()
