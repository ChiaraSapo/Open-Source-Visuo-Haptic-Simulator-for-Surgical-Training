
rem RUN ID GUI----------------------------
set CONDAPATH=C:\Users\chiar\miniconda3
set ENVNAME=thesis_env
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python C:\sofa\src\Chiara\Bats\ID_GUI.py
call conda deactivate

rem RUN SURGICAL TASKS----------------------
echo 1 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task2.py -a
echo 2 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task2.py -a
echo 3 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task3.py -a
echo 4 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task3.py -a
echo 5 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task4.py -a
echo 6 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task4.py -a
