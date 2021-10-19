set CONDAPATH=C:\Users\chiar\miniconda3
set ENVNAME=thesis_env

rem RUN ID GUI----------------------------
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python FirstGUI.py
python MainGUI.py
call conda deactivate