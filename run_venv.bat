@echo off
set VENV=%USERPROFILE%\.lmstudio\scratchpads\ih\typhoon_vn_venv
%VENV%\Scripts\python.exe --version > _venv_test.log 2>&1
type _venv_test.log
