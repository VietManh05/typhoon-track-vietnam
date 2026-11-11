from pathlib import Path

p = Path("docs/planning/evidence/PHASE-7.md")
p.write_text(
    p.read_text(encoding="utf-8")
    + "\n## Verification results\n\n- Focused docs: 3 passed.\n- Plan validator: pass, 818/818 source checkboxes mapped, 731 dependency nodes, 3236 links checked.\n- Related regression: 11 passed, 2 warnings.\n- Full regression command: .venv\\\\Scripts\\\\python.exe -m pytest -q --basetemp=.pytest-phase7-full.\n- Full regression result: \"s....................................................................... [ 34%]\\r\\n........................................................................ [ 68%]\\r\\n.................................F................................       [100%]\\r\\n================================== FAILURES ===================================\\r\\n____________________ test_tmpdir_uses_workspace_local_path ____________________\\r\\n\\r\\n    def test_tmpdir_uses_workspace_local_path():\\r\\n        repo_root = Path(__file__).resolve().parents[1]\\r\\n        expected = (repo_root / \\\".pytest-temp\\\").resolve()\\r\\n    \\r\\n>       assert Path(tempfile.gettempdir()).resolve() == expected\\r\\nE       AssertionError: assert WindowsPath('C:/Users/YOU/AppData/Local/Temp') == WindowsPath('D:/IT-Dev/python-projects/Typhoon_vn/.pytest-temp')\\r\\nE        +  where WindowsPath('C:/Users/YOU/AppData/Local/Temp') = resolve()\\r\\nE        +    where resolve = WindowsPath('C:/Users/YOU/AppData/Local/Temp').resolve\\r\\nE        +   \n",
    encoding="utf-8",
)
