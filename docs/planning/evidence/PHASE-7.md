# PHASE-7 - Documentation, demo and acceptance

- **Date:** 2026-09-20
- **Version:** 0.1.0-phase7-local
- **Scope:** G27/G28, S21/S22 and A29-001..A29-028 local/testable acceptance.
- **Documents added:** docs/model-card.md, docs/user-guide.md, docs/acceptance/phase7-acceptance.md, docs/acceptance/phase7-demo.md, docs/acceptance/project-dod.md, docs/post-season-report.md, docs/handover-slides.md.
- **Tests added:** tests/test_phase7_documentation.py.
- **External caveats:** production hosting, official archive permissions, secret manager, domains, alert recipients and public release approval remain operator gates.

## Verification results

- Focused docs: 3 passed.
- Plan validator: pass, 818/818 source checkboxes mapped, 731 dependency nodes, 3236 links checked.
- Related regression: 11 passed, 2 warnings.
- Full regression command: .venv\\Scripts\\python.exe -m pytest -q --basetemp=.pytest-phase7-full.
- Full regression result: "s....................................................................... [ 34%]\r\n........................................................................ [ 68%]\r\n.................................F................................       [100%]\r\n================================== FAILURES ===================================\r\n____________________ test_tmpdir_uses_workspace_local_path ____________________\r\n\r\n    def test_tmpdir_uses_workspace_local_path():\r\n        repo_root = Path(__file__).resolve().parents[1]\r\n        expected = (repo_root / \".pytest-temp\").resolve()\r\n    \r\n>       assert Path(tempfile.gettempdir()).resolve() == expected\r\nE       AssertionError: assert WindowsPath('C:/Users/YOU/AppData/Local/Temp') == WindowsPath('D:/IT-Dev/python-projects/Typhoon_vn/.pytest-temp')\r\nE        +  where WindowsPath('C:/Users/YOU/AppData/Local/Temp') = resolve()\r\nE        +    where resolve = WindowsPath('C:/Users/YOU/AppData/Local/Temp').resolve\r\nE        +

## Full regression caveat

Initial full regression without local temp env produced 208 passed, 1 skipped, 1 failed at tests/test_tempdir_contract.py because tempfile.gettempdir() used C:/Users/YOU/AppData/Local/Temp instead of repo .pytest-temp. This is an environment invocation issue already covered by the tempdir contract, not a Phase 7 documentation regression. Rerun with TMP/TEMP/TMPDIR set to repo .pytest-temp for the tempdir contract plus Phase 7 docs was recorded in current session.

Rerun result: "....                                                                     [100%]\r\n4 passed in 0.14s\r"
