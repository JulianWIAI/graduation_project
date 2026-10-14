# build_exe_windows.ps1 - Full pipeline: C++ compile -> locate DLLs -> PyInstaller .exe
#
# Usage (run from daw_light_version/ or anywhere):
#   powershell -ExecutionPolicy Bypass -File build_exe_windows.ps1
#
# What this script does:
#   1. Verifies Python and pip are available.
#   2. Installs pyinstaller if missing.
#   3. Compiles the C++ extension (daw_processors.pyd) via build_win.ps1.
#   4. Locates FluidSynth DLLs on the system and copies them into cpp_processors/
#      so the spec file can bundle them automatically.
#   5. Runs PyInstaller with daw_light.spec to produce dist/SBS-Synth-Master.exe.
#
# Requirements before running:
#   - Python 3.11+ in PATH (the one with your project's packages installed)
#   - Visual Studio Build Tools with C++ workload (for the C++ compilation step)
#   - CMake 3.18+ (used by build_win.ps1 via setup.py / the compiler chain)
#   - FluidSynth installed (choco install fluidsynth  OR  manual DLL on PATH)

$ScriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
Push-Location $ScriptDir

function Write-Step { param([string]$Msg) Write-Host "`n==> $Msg" -ForegroundColor Cyan }
function Write-OK   { param([string]$Msg) Write-Host "    OK: $Msg" -ForegroundColor Green }
function Write-Warn { param([string]$Msg) Write-Host "    WARN: $Msg" -ForegroundColor Yellow }
function Abort      { param([string]$Msg) Write-Host "`nABORTED: $Msg" -ForegroundColor Red; Pop-Location; exit 1 }

# ---------------------------------------------------------------------------
# Step 1 - Verify Python
# ---------------------------------------------------------------------------
Write-Step "Checking Python"
$pyExe = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyExe) {
    Abort "Python not found in PATH.  Install Python 3.11+ and add it to PATH."
}
$pyVersion = & python --version
Write-OK $pyVersion

# ---------------------------------------------------------------------------
# Step 2 - Install / verify PyInstaller
# ---------------------------------------------------------------------------
Write-Step "Checking PyInstaller"
$piCheck = & python -c "import PyInstaller; print(PyInstaller.__version__)"
if ($LASTEXITCODE -ne 0) {
    Write-Host "    PyInstaller not found - installing..." -ForegroundColor Yellow
    & pip install pyinstaller
    if ($LASTEXITCODE -ne 0) { Abort "pip install pyinstaller failed." }
    $piCheck = & python -c "import PyInstaller; print(PyInstaller.__version__)"
}
Write-OK "PyInstaller $piCheck"

# ---------------------------------------------------------------------------
# Step 3 - Compile C++ extension
# ---------------------------------------------------------------------------
Write-Step "Compiling C++ extension (daw_processors.pyd)"

$CppBuildScript = Join-Path $ScriptDir "cpp_processors\build_win.ps1"
if (-not (Test-Path $CppBuildScript)) {
    Abort "build_win.ps1 not found at $CppBuildScript"
}

powershell -ExecutionPolicy Bypass -File $CppBuildScript
if ($LASTEXITCODE -ne 0) {
    Abort "C++ build failed.  See output above.  Make sure Visual Studio C++ Build Tools and CMake are installed."
}

# Verify .pyd was produced
$pyd = Get-ChildItem "$ScriptDir\cpp_processors" -Filter "daw_processors*.pyd" -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $pyd) {
    Abort "daw_processors*.pyd not found after build.  Something went wrong in the C++ compilation step."
}
Write-OK "Found $($pyd.Name)"

# ---------------------------------------------------------------------------
# Step 4 - Locate FluidSynth DLLs and copy them next to the .pyd
#
# The DLL on this machine is libfluidsynth-3.dll (not fluidsynth.dll).
# pyfluidsynth tries several names; bundling the actual file is enough.
# We also bundle companion DLLs (SDL3.dll, sndfile.dll) from the same
# directory so the .exe is fully self-contained.
# ---------------------------------------------------------------------------
Write-Step "Locating FluidSynth DLLs"

$CppDir = "$ScriptDir\cpp_processors"

# Possible DLL filenames (search order: modern naming first)
$FluidDllNames = @("libfluidsynth-3.dll", "libfluidsynth-2.dll", "fluidsynth.dll")

# Directories to search: PATH entries + known manual-install locations
$SearchDirs = ($env:PATH.Split(";") | ForEach-Object { $_.Trim() }) + @(
    "C:\fluidsynth\bin",
    "C:\Program Files\FluidSynth\bin",
    "C:\tools\fluidsynth\bin",
    "C:\ProgramData\chocolatey\lib\fluidsynth\tools"
)

$FluidFound  = $false
$FluidBinDir = $null

foreach ($dll in $FluidDllNames) {
    foreach ($dir in $SearchDirs) {
        $candidate = Join-Path $dir $dll
        if (Test-Path $candidate) {
            $FluidBinDir = $dir
            Write-OK "Found $dll in $dir"
            $FluidFound = $true
            break
        }
    }
    if ($FluidFound) { break }
}

if ($FluidFound) {
    # Copy all DLLs from the same directory (they are runtime dependencies of each other)
    $dlls = Get-ChildItem $FluidBinDir -Filter "*.dll"
    foreach ($dll in $dlls) {
        $dest = Join-Path $CppDir $dll.Name
        Copy-Item $dll.FullName $dest -Force
        Write-OK "Bundled: $($dll.Name)"
    }
} else {
    Write-Warn "FluidSynth DLL not found on this machine."
    Write-Warn "The .exe will launch but audio playback may fail unless the user has FluidSynth installed."
    Write-Warn "To fix: install FluidSynth and re-run this script, OR"
    Write-Warn "copy libfluidsynth-3.dll manually to cpp_processors\ before running PyInstaller."
}

# ---------------------------------------------------------------------------
# Step 5 - Run PyInstaller
# ---------------------------------------------------------------------------
Write-Step "Running PyInstaller (this can take several minutes)"

$SpecFile = Join-Path $ScriptDir "daw_light.spec"
if (-not (Test-Path $SpecFile)) {
    Abort "daw_light.spec not found.  Expected at $SpecFile"
}

# Clean previous build artifacts so we start fresh
if (Test-Path "$ScriptDir\build") { Remove-Item "$ScriptDir\build" -Recurse -Force }
if (Test-Path "$ScriptDir\dist")  { Remove-Item "$ScriptDir\dist"  -Recurse -Force }

& python -m PyInstaller $SpecFile
if ($LASTEXITCODE -ne 0) {
    Abort "PyInstaller failed.  Check the output above for missing modules or import errors."
}

# ---------------------------------------------------------------------------
# Step 6 - Report output
# ---------------------------------------------------------------------------
$ExePath = "$ScriptDir\dist\SBS-Synth-Master.exe"
if (Test-Path $ExePath) {
    $SizeMB = [math]::Round((Get-Item $ExePath).Length / 1MB, 1)
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "  BUILD SUCCESSFUL" -ForegroundColor Green
    Write-Host "  Output : $ExePath" -ForegroundColor Green
    Write-Host "  Size   : $SizeMB MB" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Notes:" -ForegroundColor Yellow
    Write-Host "  * First launch extracts to a temp folder - expect 5-15 s startup." -ForegroundColor Yellow
    Write-Host "  * Windows SmartScreen will warn users (Windows protected your PC)." -ForegroundColor Yellow
    Write-Host "    They click More info -> Run anyway.  Normal for unsigned apps." -ForegroundColor Yellow
    Write-Host "  * For a polished installer (.exe setup wizard), wrap with Inno Setup:" -ForegroundColor Yellow
    Write-Host "    https://jrsoftware.org/isinfo.php" -ForegroundColor Yellow
} else {
    Abort "PyInstaller reported success but SBS-Synth-Master.exe was not found at $ExePath"
}

Pop-Location
