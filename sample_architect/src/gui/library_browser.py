import pathlib
import threading
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List

from src.data.database import Database
from src.gui import styles

_COLUMNS = ('file_name', 'role', 'bpm', 'key', 'centroid')
_HEADERS = ('Filename', 'Role', 'BPM', 'Key', 'Centroid Hz')
_WIDTHS  = (220, 90, 65, 55, 100)


class LibraryBrowser(tk.Toplevel):
    """Sortable full-library table with role override and audio preview."""

    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.title('Library Browser  —  SampleArchitect')
        self.configure(bg=styles.BG2)
        self.minsize(740, 520)
        self._db      = db
        self._samples: List[Dict[str, Any]] = []
        self._sort_col = 'file_name'
        self._sort_rev = False
        self._build()
        self.after(60, self._load_samples)

    def _build(self):
        # ── Toolbar ───────────────────────────────────────────────────────────
        toolbar = tk.Frame(self, bg=styles.BG1)
        toolbar.pack(fill='x')

        tk.Label(toolbar, text='Library Browser', fg=styles.TXT_BRT, bg=styles.BG1,
                 font=('Segoe UI', 13, 'bold')).pack(side='left', padx=16, pady=12)

        tk.Button(toolbar, text='⟳  Refresh', command=self._load_samples,
                  bg=styles.BG3, fg=styles.CYAN, relief='flat',
                  font=('Segoe UI', 9, 'bold'), cursor='hand2', bd=0,
                  padx=12, pady=4,
                  activebackground=styles.BG4, activeforeground=styles.GREEN,
                  ).pack(side='right', padx=12, pady=8)

        tk.Frame(self, bg=styles.BG4, height=1).pack(fill='x')

        # ── Table ─────────────────────────────────────────────────────────────
        frame = tk.Frame(self, bg=styles.BG2)
        frame.pack(fill='both', expand=True, padx=0, pady=0)

        style = ttk.Style()
        style.configure('SA.Treeview',
                         background=styles.BG3,
                         foreground=styles.TXT_BRT,
                         fieldbackground=styles.BG3,
                         rowheight=26,
                         font=('Segoe UI', 9),
                         borderwidth=0, relief='flat')
        style.configure('SA.Treeview.Heading',
                         background=styles.BG4,
                         foreground=styles.CYAN,
                         font=('Segoe UI', 9, 'bold'),
                         relief='flat', borderwidth=0)
        style.map('SA.Treeview',
                  background=[('selected', styles.BG5)],
                  foreground=[('selected', styles.TXT_BRT)])

        self._tree = ttk.Treeview(frame, columns=_COLUMNS, show='headings',
                                   style='SA.Treeview', selectmode='browse')
        for col, hdr, w in zip(_COLUMNS, _HEADERS, _WIDTHS):
            self._tree.heading(col, text=hdr,
                               command=lambda c=col: self._sort_by(c))
            self._tree.column(col, width=w, minwidth=40, anchor='w')

        vsb = ttk.Scrollbar(frame, orient='vertical', command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        self._tree.bind('<Double-1>', lambda e: self._play_selected())

        tk.Frame(self, bg=styles.BG4, height=1).pack(fill='x')

        # ── Bottom bar ────────────────────────────────────────────────────────
        bottom = tk.Frame(self, bg=styles.BG1)
        bottom.pack(fill='x')

        tk.Label(bottom, text='Override role:', fg=styles.TXT_MED, bg=styles.BG1,
                 font=('Segoe UI', 9)).pack(side='left', padx=(16, 6), pady=10)

        self._role_var = tk.StringVar(value='')
        role_cb = ttk.Combobox(bottom, textvariable=self._role_var,
                                state='readonly', values=styles.ALL_ROLES,
                                width=12, font=('Segoe UI', 9))
        role_cb.pack(side='left', pady=10)

        tk.Button(bottom, text='Apply  ✓', command=self._apply_override,
                  bg=styles.ORANGE, fg=styles.BG0, relief='flat',
                  font=('Segoe UI', 9, 'bold'), cursor='hand2', bd=0,
                  padx=10, pady=4,
                  activebackground=styles.YELLOW, activeforeground=styles.BG0,
                  ).pack(side='left', padx=8, pady=10)

        tk.Button(bottom, text='▶  Preview', command=self._play_selected,
                  bg=styles.BG3, fg=styles.CYAN, relief='flat',
                  font=('Segoe UI', 9, 'bold'), cursor='hand2', bd=0,
                  padx=10, pady=4,
                  activebackground=styles.BG4, activeforeground=styles.GREEN,
                  ).pack(side='left', pady=10)

        self._status = tk.Label(bottom, text='', fg=styles.TXT_MED, bg=styles.BG1,
                                 font=('Segoe UI', 8))
        self._status.pack(side='right', padx=16)

    # ── Data ──────────────────────────────────────────────────────────────────

    def _load_samples(self):
        self._samples = self._db.get_all_samples()
        self._refresh_tree()

    def _refresh_tree(self):
        self._samples.sort(key=lambda s: (s.get(self._sort_col) or ''),
                           reverse=self._sort_rev)
        for item in self._tree.get_children():
            self._tree.delete(item)
        for s in self._samples:
            role    = s.get('user_role') or s.get('inferred_role') or '—'
            bpm_str = f"{s['bpm']:.1f}" if s.get('bpm') else '—'
            key_str = s.get('key_root') or '—'
            cen_str = f"{s['spectral_centroid']:.0f}" if s.get('spectral_centroid') else '—'
            self._tree.insert('', 'end', iid=s['file_path'],
                               values=(s.get('file_name', '—'), role,
                                       bpm_str, key_str, cen_str))
        self._status.config(text=f'{len(self._samples):,} samples')

    def _sort_by(self, col: str):
        self._sort_rev = (self._sort_col == col) and not self._sort_rev
        self._sort_col = col
        self._refresh_tree()

    def _selected_fp(self) -> str:
        sel = self._tree.selection()
        return sel[0] if sel else ''

    # ── Actions ───────────────────────────────────────────────────────────────

    def _play_selected(self):
        fp = self._selected_fp()
        if fp:
            threading.Thread(target=self._play_audio, args=(fp,), daemon=True).start()

    def _play_audio(self, fp: str):
        try:
            import pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
        except Exception:
            import subprocess, sys
            try:
                if sys.platform == 'win32':
                    subprocess.Popen(['cmd', '/c', 'start', '', fp], shell=False)
                elif sys.platform == 'darwin':
                    subprocess.Popen(['open', fp])
                else:
                    subprocess.Popen(['xdg-open', fp])
            except Exception:
                pass

    def _apply_override(self):
        fp   = self._selected_fp()
        role = self._role_var.get()
        if not fp or not role:
            self._status.config(text='Select a sample and a role first.')
            return
        self._db.update_role(fp, role)
        self._load_samples()
        self._status.config(text=f'Role set to  {role}  ✓')
