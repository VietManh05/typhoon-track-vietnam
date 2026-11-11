from pathlib import Path

p = Path("docs/planning/evidence/PHASE-7.md")
p.write_text(
    p.read_text(encoding="utf-8")
    + '\n## Full regression caveat\n\nInitial full regression without local temp env produced 208 passed, 1 skipped, 1 failed at tests/test_tempdir_contract.py because tempfile.gettempdir() used C:/Users/YOU/AppData/Local/Temp instead of repo .pytest-temp. This is an environment invocation issue already covered by the tempdir contract, not a Phase 7 documentation regression. Rerun with TMP/TEMP/TMPDIR set to repo .pytest-temp for the tempdir contract plus Phase 7 docs was recorded in current session.\n\nRerun result: "....                                                                     [100%]\\r\\n4 passed in 0.14s\\r"\n',
    encoding="utf-8",
)
