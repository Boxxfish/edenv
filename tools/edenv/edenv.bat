::@echo off
cur_path = %cd%
cd %~dp0
python "edenv" %*
cd cur_path