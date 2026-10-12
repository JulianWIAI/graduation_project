"""
synth_core_fix.py — Sichert den Python-Fallback wenn synth_core.SynthCore fehlt.

Im Music-Architect-Motor liegt unter src/synth_core nur der C++-Quelltext.
Solange daraus keine Extension (.so / .pyd) gebaut wurde, findet Python den
Ordner trotzdem als leeres Namespace-Package: 'import synth_core' gelingt,
builtin_synthesizer.py setzt _CPP_AVAILABLE=True und stuerzt dann mit
"module 'synth_core' has no attribute 'SynthCore'" ab.

Loesung: Fehlt die kompilierte Klasse, wird sys.modules["synth_core"] = None
gesetzt. Das ist Standard-Python: jeder weitere 'import synth_core' wirft dann
ImportError, builtin_synthesizer setzt _CPP_AVAILABLE=False und nutzt den
reinen Python-Renderer. Der Motor selbst bleibt unveraendert.
"""
import sys


def ensure_python_fallback() -> None:
    """
    Idempotent. Muss VOR dem ersten Import von rendering.* aufgerufen werden
    (geschieht in beatgen.generate._ensure_ma_path).
    """
    try:
        import synth_core  # type: ignore
        if hasattr(synth_core, "SynthCore"):
            return                          # kompilierte Extension vorhanden
    except ImportError:
        pass
    sys.modules["synth_core"] = None        # ab jetzt: ImportError -> Python-Renderer
