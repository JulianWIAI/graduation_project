"""
rt_hook_cpp.py — PyInstaller runtime hook

When the app is frozen (onefile), sys._MEIPASS holds the temp directory where
PyInstaller extracts everything.  main.py adds <exe_dir>/cpp_processors to
sys.path, but in a frozen build the .pyd lives under _MEIPASS/cpp_processors,
not next to the .exe.  This hook runs before main.py and pre-inserts the
correct path so "import daw_processors" resolves correctly.
"""

import os
import sys

if getattr(sys, "frozen", False):
    _meipass = getattr(sys, "_MEIPASS", "")
    if _meipass:
        _cpp = os.path.join(_meipass, "cpp_processors")
        if _cpp not in sys.path:
            sys.path.insert(0, _cpp)
        # _MEIPASS itself (for any top-level .pyd/.dll siblings)
        if _meipass not in sys.path:
            sys.path.insert(0, _meipass)
