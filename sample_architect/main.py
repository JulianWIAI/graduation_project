import logging
import pathlib
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)-8s  %(name)s — %(message)s',
)

# Ensure src/ is importable when launched from the project root
_root = pathlib.Path(__file__).parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from src.data.database import Database
from src.gui.app import App


def main():
    db_dir = pathlib.Path.home() / '.sample_architect'
    db_dir.mkdir(parents=True, exist_ok=True)
    db = Database(db_dir / 'library.db')

    app = App(db)
    app.mainloop()


if __name__ == '__main__':
    main()
