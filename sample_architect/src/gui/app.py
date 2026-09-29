import tkinter as tk
from tkinter import ttk

from src.data.database import Database
from src.gui import styles
from src.gui.library_panel import LibraryPanel
from src.gui.setup_browser import SetupBrowser


class App(tk.Tk):
    def __init__(self, db: Database):
        super().__init__()
        self._db = db
        self.title('SampleArchitect')
        self.minsize(1080, 720)
        self.configure(bg=styles.BG0)
        self._apply_theme()
        self._build()

    def _apply_theme(self):
        style = ttk.Style(self)
        style.theme_use('default')
        style.configure('TCombobox',
                        fieldbackground=styles.BG4,
                        background=styles.BG4,
                        foreground=styles.TXT_BRT,
                        selectbackground=styles.BG5,
                        selectforeground=styles.CYAN,
                        arrowcolor=styles.CYAN,
                        borderwidth=0,
                        relief='flat')
        style.map('TCombobox',
                  fieldbackground=[('readonly', styles.BG4)],
                  foreground=[('readonly', styles.TXT_BRT)],
                  selectbackground=[('readonly', styles.BG5)])
        style.configure('TScrollbar',
                        background=styles.BG4,
                        troughcolor=styles.BG2,
                        arrowcolor=styles.TXT_DIM,
                        borderwidth=0,
                        relief='flat')
        style.configure('SA.Horizontal.TProgressbar',
                        background=styles.CYAN,
                        troughcolor=styles.BG4,
                        borderwidth=0,
                        relief='flat')

    def _build(self):
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        self.library_panel = LibraryPanel(self, self._db)
        self.library_panel.grid(row=0, column=0, sticky='ns')

        sep = tk.Frame(self, bg=styles.BG4, width=1)
        sep.grid(row=0, column=1, sticky='ns')

        self.setup_browser = SetupBrowser(self, self._db)
        self.setup_browser.grid(row=0, column=2, sticky='nsew')
