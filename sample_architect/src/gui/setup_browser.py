import json
import pathlib
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Any, Dict, List, Optional

from src.data.database import Database
from src.export.assignment_map import AssignmentMap
from src.gui import styles
from src.gui.sample_cell import SampleCell
from src.matching.setup_generator import SetupGenerator

_GENRES = ['trap', 'hiphop', 'house', 'edm', 'techno', 'dnb',
           'phonk', 'pop', 'jpop', 'cinematic', 'classical']

_KEYS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

_GROOVE_DISPLAY = [
    'Default', 'Boom Bap', 'Lo-Fi Chill', 'Modern Rap',
    'Dark Memphis', 'Melodic Trap', 'Detroit', 'Tight Grid',
]
_GROOVE_MAP = {
    'Default':      'default',
    'Boom Bap':     'swing',
    'Lo-Fi Chill':  'lo_fi',
    'Modern Rap':   'tight',
    'Dark Memphis': 'swing',
    'Melodic Trap': 'tight',
    'Detroit':      'swing',
    'Tight Grid':   'tight',
}
_FX_VARIANTS = ['BRIGHT', 'NEUTRAL', 'DARK']


class SetupBrowser(tk.Frame):
    """Right panel: song parameters + scrollable setup cards."""

    def __init__(self, parent, db: Database):
        super().__init__(parent, bg=styles.BG2)
        self._db        = db
        self._generator = SetupGenerator(db)
        self._exporter  = AssignmentMap(db)
        self._setups:        List[Dict[str, Any]] = []
        self._all_candidates: Dict[str, List]     = {}
        self._fx_var = tk.StringVar(value='NEUTRAL')
        self._build()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build(self):
        self._build_params_bar()
        self._build_cards_area()

    def _build_params_bar(self):
        bar = tk.Frame(self, bg=styles.BG1)
        bar.pack(fill='x')

        # ── Section label ────────────────────────────────────────────────────
        top_row = tk.Frame(bar, bg=styles.BG1)
        top_row.pack(fill='x', padx=20, pady=(14, 8))
        tk.Label(top_row, text='YOUR SONG', fg=styles.TXT_MED, bg=styles.BG1,
                 font=('Segoe UI', 8, 'bold')).pack(side='left')
        tk.Button(top_row, text='Load from JSON  ↑',
                  command=self._load_json,
                  bg=styles.BG3, fg=styles.TXT_MED, relief='flat',
                  font=('Segoe UI', 8), cursor='hand2', bd=0,
                  padx=10, pady=3,
                  activebackground=styles.BG4, activeforeground=styles.TXT_BRT,
                  ).pack(side='right')

        # ── Param widgets row ─────────────────────────────────────────────────
        params_row = tk.Frame(bar, bg=styles.BG1)
        params_row.pack(fill='x', padx=20, pady=(0, 6))

        self._genre_var = tk.StringVar(value='trap')
        self._bpm_var   = tk.StringVar(value='140')
        self._key_var   = tk.StringVar(value='C')
        self._mode_var  = tk.StringVar(value='minor')

        self._combo(params_row, 'Genre',  self._genre_var, _GENRES,     10)
        self._entry(params_row, 'BPM',    self._bpm_var,   5)
        self._combo(params_row, 'Key',    self._key_var,   _KEYS,       5)
        self._combo(params_row, 'Mode',   self._mode_var,  ['major', 'minor'], 6)
        self._fx_chips(params_row)
        self._combo(params_row, 'Groove', self._groove_var if hasattr(self, '_groove_var')
                    else self._mk_groove(), _GROOVE_DISPLAY, 12)

        # ── Find button ───────────────────────────────────────────────────────
        self._find_btn = tk.Button(
            params_row, text='Find Matching Setups  →',
            command=self._find_setups,
            bg=styles.CYAN, fg=styles.BG0, relief='flat',
            font=('Segoe UI', 10, 'bold'), cursor='hand2', bd=0,
            padx=16, pady=6,
            activebackground=styles.GREEN, activeforeground=styles.BG0,
        )
        self._find_btn.pack(side='left', padx=(16, 0))

        # ── Status bar ────────────────────────────────────────────────────────
        self._status_lbl = tk.Label(
            bar, text='', fg=styles.TXT_MED, bg=styles.BG1,
            font=('Segoe UI', 8), anchor='w',
        )
        self._status_lbl.pack(fill='x', padx=20, pady=(0, 10))

        tk.Frame(self, bg=styles.BG4, height=1).pack(fill='x')

    def _mk_groove(self):
        self._groove_var = tk.StringVar(value='Default')
        return self._groove_var

    def _combo(self, parent, label: str, var: tk.StringVar, values: list, width: int):
        grp = tk.Frame(parent, bg=styles.BG1)
        grp.pack(side='left', padx=(0, 10))
        tk.Label(grp, text=label, fg=styles.TXT_MED, bg=styles.BG1,
                 font=('Segoe UI', 8)).pack(anchor='w')
        cb = ttk.Combobox(grp, textvariable=var, values=values,
                           state='readonly', width=width,
                           font=('Segoe UI', 9))
        cb.pack()
        return cb

    def _entry(self, parent, label: str, var: tk.StringVar, width: int):
        grp = tk.Frame(parent, bg=styles.BG1)
        grp.pack(side='left', padx=(0, 10))
        tk.Label(grp, text=label, fg=styles.TXT_MED, bg=styles.BG1,
                 font=('Segoe UI', 8)).pack(anchor='w')
        tk.Entry(grp, textvariable=var, width=width,
                 bg=styles.BG4, fg=styles.TXT_BRT,
                 insertbackground=styles.CYAN, relief='flat',
                 font=('Segoe UI', 9), bd=6).pack()

    def _fx_chips(self, parent):
        if not hasattr(self, '_groove_var'):
            self._groove_var = tk.StringVar(value='Default')
        grp = tk.Frame(parent, bg=styles.BG1)
        grp.pack(side='left', padx=(0, 10))
        tk.Label(grp, text='Vibe', fg=styles.TXT_MED, bg=styles.BG1,
                 font=('Segoe UI', 8)).pack(anchor='w')
        chip_row = tk.Frame(grp, bg=styles.BG1)
        chip_row.pack()
        self._fx_btns: Dict[str, tk.Button] = {}
        for fx in _FX_VARIANTS:
            btn = tk.Button(chip_row, text=fx,
                            command=lambda v=fx: self._select_fx(v),
                            font=('Segoe UI', 8, 'bold'), relief='flat',
                            cursor='hand2', bd=0, padx=8, pady=3)
            btn.pack(side='left', padx=1)
            self._fx_btns[fx] = btn
        self._select_fx('NEUTRAL')

    def _select_fx(self, variant: str):
        self._fx_var.set(variant)
        colors = {'BRIGHT': styles.YELLOW, 'NEUTRAL': styles.CYAN, 'DARK': styles.PURPLE}
        for v, btn in self._fx_btns.items():
            if v == variant:
                btn.config(bg=colors.get(v, styles.CYAN), fg=styles.BG0)
            else:
                btn.config(bg=styles.BG4, fg=styles.TXT_MED)

    def _build_cards_area(self):
        container = tk.Frame(self, bg=styles.BG2)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg=styles.BG2, highlightthickness=0)
        vsb    = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        self._cards_inner  = tk.Frame(canvas, bg=styles.BG2)
        self._canvas_win   = canvas.create_window((0, 0), window=self._cards_inner, anchor='nw')
        self._canvas       = canvas

        self._cards_inner.bind('<Configure>',
                                lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        def _resize(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.itemconfig(self._canvas_win, width=event.width)

        canvas.bind('<Configure>', _resize)
        canvas.bind_all('<MouseWheel>',
                        lambda e: canvas.yview_scroll(int(-1 * e.delta / 120), 'units'))

        self._show_empty_state()

    def _show_empty_state(self):
        f = tk.Frame(self._cards_inner, bg=styles.BG2)
        f.pack(expand=True, pady=60)
        tk.Label(f, text='No setups yet', fg=styles.TXT_MED, bg=styles.BG2,
                 font=('Segoe UI', 15, 'bold')).pack()
        tk.Label(f,
                 text='Set your song\'s Genre, BPM, Key and Vibe above,\nthen click  Find Matching Setups  to generate combinations.',
                 fg=styles.TXT_DIM, bg=styles.BG2,
                 font=('Segoe UI', 10), justify='center').pack(pady=(8, 0))

    # ── JSON load ─────────────────────────────────────────────────────────────

    def _load_json(self):
        path = filedialog.askopenfilename(
            title='Load Music Architect V7 composition',
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')],
        )
        if not path:
            return
        try:
            data   = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
            config = data.get('config', {})
            if config.get('genre'):   self._genre_var.set(config['genre'])
            if config.get('bpm'):     self._bpm_var.set(str(config['bpm']))
            if config.get('key_root'): self._key_var.set(config['key_root'])
            if config.get('key_mode'): self._mode_var.set(config['key_mode'])
            self._status_lbl.config(
                text='Loaded from JSON  ✓  —  set Vibe and Groove manually.'
            )
        except Exception as exc:
            messagebox.showerror('Load Error', str(exc))

    # ── Setup generation ──────────────────────────────────────────────────────

    def _song_params(self) -> Dict[str, Any]:
        try:
            bpm = float(self._bpm_var.get())
        except ValueError:
            bpm = 140.0
        return {
            'genre':       self._genre_var.get(),
            'bpm':         bpm,
            'key':         self._key_var.get(),
            'key_mode':    self._mode_var.get(),
            'fx_variant':  self._fx_var.get(),
            'groove_feel': _GROOVE_MAP.get(self._groove_var.get(), 'default'),
        }

    def _find_setups(self):
        self._find_btn.config(state='disabled', text='Generating…')
        self._status_lbl.config(text='Scoring your library…')
        self._clear_cards()
        self._setups = []
        params = self._song_params()

        def run():
            result = self._generator.generate(params, n_setups=5)
            self.after(0, self._on_setups_ready, result, params)

        threading.Thread(target=run, daemon=True).start()

    def _on_setups_ready(self, result: Dict, song_params: Dict):
        self._setups          = result['setups']
        self._all_candidates  = result['all_candidates']
        warnings              = result.get('warnings', [])
        self._find_btn.config(state='normal', text='Find Matching Setups  →')
        if warnings:
            roles = ', '.join(w['role'] for w in warnings)
            self._status_lbl.config(text=f'⚠  Low sample count for: {roles}')
        else:
            self._status_lbl.config(
                text=f'{len(self._setups)} setups ready  —  click Use This Setup to export.'
            )
        self._render_setups(self._setups, song_params)

    def _render_setups(self, setups: List[Dict], song_params: Dict):
        self._clear_cards()
        for setup in setups:
            self._add_setup_card(setup, song_params)
        self._add_more_button(song_params)

    def _clear_cards(self):
        for w in self._cards_inner.winfo_children():
            w.destroy()

    # ── Setup card ────────────────────────────────────────────────────────────

    def _add_setup_card(self, setup: Dict, song_params: Dict):
        outer = tk.Frame(self._cards_inner, bg=styles.BG2)
        outer.pack(fill='x', padx=20, pady=(12, 0))

        card = tk.Frame(outer, bg=styles.BG3)
        card.pack(fill='x')

        self._card_header(card, setup, song_params)
        tk.Frame(card, bg=styles.BG4, height=1).pack(fill='x')
        self._card_body(card, setup, song_params)
        self._card_footer(card, setup)

    def _card_header(self, card, setup: Dict, song_params: Dict):
        hdr = tk.Frame(card, bg=styles.BG4)
        hdr.pack(fill='x')

        score = setup['score']
        if score >= 80:
            score_fg = styles.GREEN
        elif score >= 65:
            score_fg = styles.YELLOW
        else:
            score_fg = styles.TXT_MED

        # Rank
        tk.Label(hdr, text=f'  #{setup["rank"]}', fg=styles.TXT_MED, bg=styles.BG4,
                 font=('Segoe UI', 9, 'bold'), width=4, anchor='w').pack(side='left', pady=10)

        # Score
        tk.Label(hdr, text=f'{score:.0f}', fg=score_fg, bg=styles.BG4,
                 font=('Segoe UI', 18, 'bold')).pack(side='left', padx=(4, 2), pady=6)
        tk.Label(hdr, text='/ 100', fg=styles.TXT_DIM, bg=styles.BG4,
                 font=('Segoe UI', 9)).pack(side='left', pady=10)

        # Score bar
        bar_frame = tk.Frame(hdr, bg=styles.BG5, height=4, width=80)
        bar_frame.pack(side='left', padx=12)
        bar_frame.pack_propagate(False)
        fill_w = max(2, int((score / 100) * 80))
        tk.Frame(bar_frame, bg=score_fg, height=4, width=fill_w).place(x=0, y=0)

        # Use button
        tk.Button(
            hdr, text='Use This Setup  →',
            command=lambda s=setup, sp=song_params: self._use_setup(s, sp),
            bg=styles.ORANGE, fg=styles.BG0, relief='flat',
            font=('Segoe UI', 9, 'bold'), cursor='hand2', bd=0,
            padx=14, pady=6,
            activebackground=styles.YELLOW, activeforeground=styles.BG0,
        ).pack(side='right', padx=12, pady=8)

    def _card_body(self, card, setup: Dict, song_params: Dict):
        body = tk.Frame(card, bg=styles.BG3)
        body.pack(fill='x')
        for i, role in enumerate(styles.SETUP_ROLES):
            row_bg = styles.BG3 if i % 2 == 0 else styles.BG2
            track  = setup['tracks'].get(role)
            if not track:
                self._empty_slot_row(body, role, row_bg)
            else:
                alts       = self._all_candidates.get(role, [])
                current_fp = track.get('file', '')
                other_alts = [c for c in alts if c['file_path'] != current_fp]
                cell = SampleCell(body, role=role, track=track,
                                   alternatives=other_alts,
                                   on_swap=lambda r=role, s=setup, sp=song_params:
                                       self._swap_track(r, s, sp))
                cell.configure(bg=row_bg)
                cell.pack(fill='x')
                tk.Frame(body, bg=styles.BG4, height=1).pack(fill='x')

    def _empty_slot_row(self, parent, role: str, bg: str):
        row = tk.Frame(parent, bg=bg)
        row.pack(fill='x')
        color = styles.ROLE_COLORS.get(role, styles.TXT_MED)
        tk.Label(row, text=f' {role.upper()} ',
                 fg=styles.BG4, bg=color,
                 font=('Segoe UI', 8, 'bold'), width=8, anchor='center',
                 ).pack(side='left', padx=(8, 6), pady=5)
        tk.Label(row, text='No samples in library for this role',
                 fg=styles.TXT_DIM, bg=bg,
                 font=('Segoe UI', 8)).pack(side='left')
        tk.Frame(parent, bg=styles.BG4, height=1).pack(fill='x')

    def _card_footer(self, card, setup: Dict):
        texts = []
        for w in setup.get('warnings', []):
            texts.append(f'⚠  Low candidates for {w["role"]} ({w["candidates"]} found)')
        for rank in setup.get('overlap_with', []):
            texts.append(f'↕  Shares samples with setup #{rank}')
        if texts:
            footer = tk.Frame(card, bg=styles.BG2)
            footer.pack(fill='x')
            for t in texts:
                tk.Label(footer, text=f'  {t}',
                         fg=styles.YELLOW, bg=styles.BG2,
                         font=('Segoe UI', 8), anchor='w').pack(fill='x', pady=2)

    # ── Generate More button ──────────────────────────────────────────────────

    def _add_more_button(self, song_params: Dict):
        f = tk.Frame(self._cards_inner, bg=styles.BG2)
        f.pack(fill='x', padx=20, pady=16)
        tk.Button(
            f, text='Generate 5 More Setups',
            command=lambda: self._generate_more(song_params),
            bg=styles.BG3, fg=styles.CYAN, relief='flat',
            font=('Segoe UI', 10, 'bold'), cursor='hand2', bd=0,
            pady=10, activebackground=styles.BG4, activeforeground=styles.GREEN,
        ).pack(fill='x')

    def _generate_more(self, song_params: Dict):
        used_fps: set = set()
        for s in self._setups:
            for t in s['tracks'].values():
                fp = t.get('file')
                if fp:
                    used_fps.add(fp)
        self._status_lbl.config(text='Generating 5 more setups…')

        def run():
            result = self._generator.generate(song_params, n_setups=5,
                                               exclude_fps=used_fps)
            self.after(0, self._on_more_ready, result, song_params)

        threading.Thread(target=run, daemon=True).start()

    def _on_more_ready(self, result: Dict, song_params: Dict):
        offset = len(self._setups)
        for s in result['setups']:
            s['rank'] += offset
        self._setups.extend(result['setups'])
        for key, cands in result['all_candidates'].items():
            existing = {c['file_path'] for c in self._all_candidates.get(key, [])}
            for c in cands:
                if c['file_path'] not in existing:
                    self._all_candidates.setdefault(key, []).append(c)
        self._status_lbl.config(text=f'{len(self._setups)} total setups shown.')
        self._render_setups(self._setups, song_params)

    # ── Swap / export ─────────────────────────────────────────────────────────

    def _swap_track(self, role: str, setup: Dict, song_params: Dict):
        pass  # handled inside SampleCell popup → on_swap callback

    def _use_setup(self, setup: Dict, song_params: Dict):
        path = filedialog.asksaveasfilename(
            title='Save setup',
            defaultextension='.json',
            filetypes=[('JSON files', '*.json')],
            initialfile='setup_export.json',
        )
        if not path:
            return
        try:
            self._exporter.export_setup(setup, song_params, pathlib.Path(path))
            self._status_lbl.config(
                text=f'Exported  ✓  →  {pathlib.Path(path).name}'
            )
        except Exception as exc:
            messagebox.showerror('Export Error', str(exc))
