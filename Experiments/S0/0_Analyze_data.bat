
rem RUN ID GUI----------------------------
set CONDAPATH=C:\Users\chiar\miniconda3
set ENVNAME=thesis_env
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python 0_Height.py
python 0_Scalpel_height.py
python 0_Time_Reps.py
python 0_Trajectories.py


call conda deactivate
