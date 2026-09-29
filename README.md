# Graduation Project — AI Music Production Suite

A cohesive set of four music production tools built as a graduation project.
Each module is independent but shares data with the others through a defined workflow.

---

## Modules

| Module | Technology | Purpose |
|--------|-----------|---------|
| [Music Architect V7](music_architect_v7/) | Python · Tkinter | AI-driven MIDI composition engine (11 genres, evolutionary pipeline) |
| [DAW Light Version](daw_light_version/) | Python · PySide6 · C++ DSP | Full digital audio workstation — MIDI sequencing, mixing, mastering |
| [Music Catalogue Manager v.2](Music_catalogue_manager_v.2/) | Python · Flask | Web-based catalog, licensing, and economic reporting |
| [Sample Architect](sample_architect/) | Python · Tkinter | Intelligent sample library analyzer and setup generator |

Each module has its own `README.md` with detailed feature documentation.

---

## Data Flow

```
Music Architect V7
  └─ generates MIDI files + production reports
        │
        ├─▶  DAW Light Version
        │      └─ imports MIDI, adds audio FX, exports stems / masters
        │
        ├─▶  Music Catalogue Manager v.2
        │      └─ scans catalog, manages licenses, models revenue
        │
        └─▶  Sample Architect
               └─ finds compatible audio samples for new projects
```

---

## Prerequisites

The following system-level tools must be installed before the Python dependencies.

### macOS

```bash
brew install fluidsynth ffmpeg sdl2
```

> **Homebrew** itself: see [brew.sh](https://brew.sh) if it is not already installed.

### Windows

Install the following manually or via **winget** / **Chocolatey**:

| Tool | winget command |
|------|----------------|
| Python 3.11 | `winget install Python.Python.3.11` |
| FluidSynth | download from [fluidsynth.org](https://www.fluidsynth.org) and add to `PATH` |
| FFmpeg | `winget install Gyan.FFmpeg` |
| CMake (for DAW C++ DSP) | `winget install Kitware.CMake` |
| Visual Studio Build Tools | `winget install Microsoft.VisualStudio.2022.BuildTools` |

> FluidSynth on Windows: copy `fluidsynth.dll` to the `daw_light_version/` directory **or** add its `bin/` folder to your system `PATH`.

---

## Environment Setup

### 1. Clone the repository

```bash
git clone <repo-url> graduation_project
cd graduation_project
```

### 2. Run the master setup script

**macOS / Linux**

```bash
chmod +x setup.sh
./setup.sh
```

**Windows (PowerShell, run as Administrator)**

```powershell
# Run each module setup individually — the master setup.sh is bash-only
cd music_architect_v7
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
deactivate

cd ..\daw_light_version
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
deactivate

cd ..\Music_catalogue_manager_v.2
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
deactivate

cd ..\sample_architect
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
deactivate
```

Each module uses its own isolated virtual environment (`.venv/`).
Do **not** mix them or install packages globally.

### 3. Download large assets (not in the repository)

These files are too large for Git and must be downloaded separately.

#### SoundFonts (`.sf2`)

See [`daw_light_version/soundfonts/README.txt`](daw_light_version/soundfonts/README.txt) for download links.
Place downloaded `.sf2` files in `daw_light_version/soundfonts/`.

#### Master Seed Corpus

`music_architect_v7/seeds/master_seeds.json` (~961 MB) is excluded from the repository.
Obtain it from your team's shared drive and place it at that path.
The smaller per-genre matrices in `seeds/matrices/` **are** included and sufficient for development.

### 4. Build the C++ DSP processors (DAW only)

**macOS**

```bash
cd daw_light_version/cpp_processors
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(sysctl -n hw.logicalcpu)
```

**Windows (PowerShell)**

```powershell
cd daw_light_version\cpp_processors
.\build_win.ps1
```

The compiled extension is placed automatically where PySide6 can load it.
The DAW runs without this step but falls back to pure-Python processing.

---

## Running the Applications

### Interactive launcher (macOS)

```bash
./start.sh
```

### Individual launchers (macOS)

```bash
./launch_architect.sh       # Music Architect V7
./launch_daw.sh             # DAW Light Version
./launch_catalogue.sh       # Music Catalogue Manager  →  http://localhost:5000
./launch_sample_architect.sh # Sample Architect
```

### Manual launch (macOS / Windows)

Activate the relevant virtual environment first, then run the entry point.

**macOS**

```bash
source music_architect_v7/.venv/bin/activate
cd music_architect_v7 && python main.py
```

**Windows**

```powershell
music_architect_v7\.venv\Scripts\activate
cd music_architect_v7
python main.py
```

---

## Repository Structure

```
graduation_project/
├── music_architect_v7/         # AI composition engine
│   ├── src/                    # Source — engine, GUI, tools
│   ├── seeds/                  # Genre matrices (master_seeds.json excluded)
│   ├── config/                 # harmonic_governor.json
│   ├── tests/
│   └── main.py
│
├── daw_light_version/          # Digital audio workstation
│   ├── core/                   # Python application layer
│   ├── cpp_processors/         # C++ DSP extension (pybind11)
│   ├── soundfonts/             # Place .sf2 files here (excluded from Git)
│   ├── benchmarks/             # Per-genre mastering targets
│   └── main.py
│
├── Music_catalogue_manager_v.2/ # Flask web catalog & licensing
│   ├── auth/ beatgen/ catalog/ commerce/ groove/
│   ├── db/                     # Schema and migrations
│   ├── templates/ static/
│   └── app.py
│
├── sample_architect/           # Sample library manager
│   ├── src/
│   └── main.py
│
├── setup.sh                    # Master setup (macOS)
├── start.sh                    # Interactive launcher (macOS)
├── launch_*.sh                 # Individual launchers (macOS)
├── .gitignore
└── README.md
```

---

## Git Workflow for the Team

### Initial setup (one-time, per contributor)

If the sub-project folders still contain their own `.git` directories, remove them so everything is tracked by the single root repository:

```bash
# Run from the graduation_project root
rm -rf music_architect_v7/.git
rm -rf daw_light_version/.git
rm -rf Music_catalogue_manager_v.2/.git
rm -rf sample_architect/.git

git init
git add .
git commit -m "chore: initial commit"
git remote add origin <repo-url>
git push -u origin main
```

### Daily workflow

```bash
# Start of day — pull latest changes
git pull origin main

# Create a branch for your work
git checkout -b feature/<short-description>

# ... make changes ...

git add <files>
git commit -m "type: short description"
git push origin feature/<short-description>
# Then open a Pull Request on GitHub
```

### Commit message convention

```
feat:     a new feature
fix:      a bug fix
refactor: code change with no functional difference
docs:     documentation only
chore:    build, config, or tooling changes
```

### Branch naming

```
feature/<what-you-are-adding>
fix/<what-you-are-fixing>
```

---

## Notes on Cross-Platform Development

| Topic | macOS | Windows |
|-------|-------|---------|
| Shell scripts | `./start.sh`, `./launch_*.sh` | Run Python entry points directly |
| FluidSynth | `brew install fluidsynth` | Manual install + `PATH` or DLL next to `main.py` |
| C++ build | `make` via CMake | `build_win.ps1` (MSVC required) |
| File paths | Forward slashes | Both slashes work in Python; avoid hardcoded backslashes in code |
| Line endings | LF | Set `git config core.autocrlf input` on Windows to avoid CRLF diffs |

> **Windows tip:** run `git config --global core.autocrlf input` once after installing Git to prevent line-ending noise in pull requests.

---

## Python Version

All modules require **Python 3.10 or higher**. Python 3.11 is recommended and tested.

```bash
python --version   # must be 3.10+
```