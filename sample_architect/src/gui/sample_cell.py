import pathlib
import threading
import tkinter as tk
from typing import Any, Callable, Dict, List, Optional

from src.gui import styles


class SampleCell(tk.Frame):
    """One track row inside a setup card."""

    def __init__(
        self,
        parent,
        role: str,
        track: Dict[str, Any],
        alternatives: List[Dict[str, Any]],
        on_swap: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        **kwargs,
    ):
        super().__init__(parent, bg=styles.BG3, **kwargs)
        self._role = role
        self._track = track
        self._alternatives = alternatives
        self._on_swap = on_swap
        self._build()

    def _build(self):
        role_color = styles.ROLE_COLORS.get(self._role, styles.TXT_MED)
        score      = float(self._track.get('score', 0.0))
        fp         = self._track.get('file', '')
        fname      = pathlib.Path(fp).name if fp else '—'
        fname_disp = fname[:26] if len(fname) > 26 else fname

        bpm_val  = self._track.get('bpm')
        bpm_str  = f"{bpm_val:.0f}" if bpm_val else '—'
        key_str  = self._track.get('key') or '—'

        # Score colour + text
        if score >= 85:
            score_fg = styles.GREEN
        elif score >= 70:
            score_fg = styles.YELLOW
        else:
            score_fg = styles.TXT_MED

        # ── Role pill ────────────────────────────────────────────────────────
        pill = tk.Label(
            self,
            text=f' {self._role.upper()} ',
            fg=styles.BG1, bg=role_color,
            font=('Segoe UI', 8, 'bold'),
            width=8, anchor='center',
        )
        pill.pack(side='left', padx=(8, 6), pady=6)

        # ── Filename ─────────────────────────────────────────────────────────
        tk.Label(
            self, text=fname_disp,
            fg=styles.TXT_BRT, bg=styles.BG3,
            font=styles.FN_MONO_S, width=26, anchor='w',
        ).pack(side='left', padx=(0, 8))

        # ── BPM badge ────────────────────────────────────────────────────────
        self._badge(bpm_str, styles.YELLOW, width=4).pack(side='left', padx=2)

        # ── Key badge ────────────────────────────────────────────────────────
        self._badge(key_str, styles.CYAN, width=4).pack(side='left', padx=2)

        # ── Score badge ──────────────────────────────────────────────────────
        tk.Label(
            self, text=f'{score:.0f}',
            fg=score_fg, bg=styles.BG3,
            font=('Segoe UI', 9, 'bold'), width=3, anchor='center',
        ).pack(side='left', padx=(4, 2))

        # ── Play button ──────────────────────────────────────────────────────
        play_btn = tk.Button(
            self, text='▶',
            command=self._play,
            bg=styles.BG4, fg=styles.CYAN,
            relief='flat', font=('Segoe UI', 9),
            cursor='hand2', bd=0, padx=8, pady=2,
            activebackground=styles.BG5, activeforeground=styles.GREEN,
        )
        play_btn.pack(side='left', padx=(4, 2))

        # ── Swap button ──────────────────────────────────────────────────────
        swap_btn = tk.Button(
            self, text='Alt.',
            command=self._open_alternatives,
            bg=styles.BG4, fg=styles.TXT_MED,
            relief='flat', font=('Segoe UI', 8),
            cursor='hand2', bd=0, padx=8, pady=2,
            activebackground=styles.BG5, activeforeground=styles.TXT_BRT,
        )
        swap_btn.pack(side='left', padx=(0, 8))

    def _badge(self, text: str, color: str, width: int = 5) -> tk.Label:
        return tk.Label(
            self, text=text,
            fg=color, bg=styles.BG4,
            font=styles.FN_MONO_S, width=width, anchor='center',
            padx=4, pady=1,
        )

    # ── Playback ─────────────────────────────────────────────────────────────

    def _play(self):
        fp = self._track.get('file', '')
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
            self._play_fallback(fp)

    def _play_fallback(self, fp: str):
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

    # ── Alternatives popup ───────────────────────────────────────────────────

    def _open_alternatives(self):
        if not self._alternatives:
            return
        popup = tk.Toplevel(self)
        popup.title(f'Alternatives  —  {self._role.upper()}')
        popup.configure(bg=styles.BG2)
        popup.resizable(False, False)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        # Header
        hdr = tk.Frame(popup, bg=styles.BG3)
        hdr.pack(fill='x')
        tk.Label(hdr, text=f'  Pick a different  {self._role.upper()}  sample',
                 fg=styles.TXT_BRT, bg=styles.BG3,
                 font=styles.FN_HEAD).pack(side='left', pady=14, padx=16)
        tk.Button(hdr, text='✕', command=popup.destroy,
                  bg=styles.BG3, fg=styles.TXT_MED, relief='flat',
                  font=styles.FN_BODY, cursor='hand2', bd=0,
                  activebackground=styles.BG3, activeforeground=styles.RED,
                  padx=12, pady=8).pack(side='right')

        # Alt rows
        for alt in self._alternatives[:5]:
            self._alt_row(popup, alt)

        tk.Frame(popup, bg=styles.BG4, height=1).pack(fill='x', padx=0, pady=(8, 0))
        tk.Button(popup, text='Close  ✕', command=popup.destroy,
                  bg=styles.BG2, fg=styles.TXT_MED, relief='flat',
                  font=styles.FN_SMALL, cursor='hand2', bd=0, pady=10,
                  activebackground=styles.BG3).pack(fill='x')

    def _alt_row(self, parent, alt: Dict[str, Any]):
        row = tk.Frame(parent, bg=styles.BG3, cursor='hand2')
        row.pack(fill='x', padx=12, pady=3)

        fp    = alt.get('file_path', '')
        name  = pathlib.Path(fp).name if fp else '—'
        name_disp = name[:32] if len(name) > 32 else name
        bpm   = alt.get('bpm')
        key   = alt.get('key_root') or '—'
        score = float(alt.get('_score', 0.0))
        score_fg = styles.GREEN if score >= 85 else (styles.YELLOW if score >= 70 else styles.TXT_MED)

        tk.Label(row, text=name_disp, fg=styles.TXT_BRT, bg=styles.BG3,
                 font=styles.FN_MONO_S, anchor='w', width=34).pack(side='left', padx=10, pady=8)
        tk.Label(row, text=f"{bpm:.0f}" if bpm else '—',
                 fg=styles.YELLOW, bg=styles.BG3, font=styles.FN_MONO_S, width=5).pack(side='left')
        tk.Label(row, text=key, fg=styles.CYAN, bg=styles.BG3,
                 font=styles.FN_MONO_S, width=5).pack(side='left')
        tk.Label(row, text=f'{score:.0f}', fg=score_fg, bg=styles.BG3,
                 font=('Segoe UI', 9, 'bold'), width=4).pack(side='left')

        def use(a=alt):
            if self._on_swap:
                self._on_swap(self._role, a)
            parent.destroy()

        tk.Button(row, text='Use this  →', command=use,
                  bg=styles.CYAN, fg=styles.BG1, relief='flat',
                  font=('Segoe UI', 9, 'bold'), cursor='hand2', bd=0,
                  padx=12, pady=4,
                  activebackground=styles.GREEN, activeforeground=styles.BG1,
                  ).pack(side='right', padx=8, pady=4)

    def update_track(self, track: Dict[str, Any]):
        self._track = track
        for w in self.winfo_children():
            w.destroy()
        self._build()
