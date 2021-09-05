
rem RUN ID GUI----------------------------
set CONDAPATH=C:\Users\chiar\miniconda3
set ENVNAME=thesis_env
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python C:\sofa\src\Chiara\Bats\ID_GUI.py
call conda deactivate

rem RUN FAMILIARIZING GUI-----------------
set CONDAPATH=C:\Users\chiar\miniconda3
set ENVNAME=thesis_env
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python C:\sofa\src\Chiara\Bats\Familiarizing_GUI.py
call conda deactivate

rem RUN FAMILIARIZING TASKS---------------
cd C:\sofa\build\v20.12.02\bin\Release
runSofa C:\sofa\src\Chiara\Trial_Line1Left.py -a
runSofa C:\sofa\src\Chiara\Trial_Line2Left.py -a
runSofa C:\sofa\src\Chiara\Trial_Line3Left.py -a
runSofa C:\sofa\src\Chiara\Trial_CubeLeft.py -a
runSofa C:\sofa\src\Chiara\Trial_SphereLeft.py -a


rem RUN TASK GUI--------------------------
set CONDAPATH=C:\Users\chiar\miniconda3
set ENVNAME=thesis_env
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python C:\sofa\src\Chiara\Bats\Task_GUI.py
python C:\sofa\src\Chiara\Bats\Change_ee.py
call conda deactivate


rem RUN SURGICAL TASKS----------------------
echo 1 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task2Left.py -a
echo 2 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task2Left.py -a
echo 3 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task3Left.py -a
echo 4 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task3Left.py -a
echo 5 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task4Left.py -a
echo 6 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Incision_task4Left.py -a


rem RUN TASK GUI--------------------------
set CONDAPATH=C:\Users\chiar\miniconda3
set ENVNAME=thesis_env
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python C:\sofa\src\Chiara\Bats\Change_ee.py
call conda deactivate

echo 7 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Rings_task_DoubleLeft.py -a
echo 8 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Rings_task_DoubleLeft.py -a
echo 9 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Rings_task_DoubleLeft.py -a
echo 10 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Rings_task_DoubleLeft.py -a
echo 11 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Rings_task_DoubleLeft.py -a
echo 12 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Rings_task_DoubleLeft.py -a


rem RUN TASK GUI--------------------------
set CONDAPATH=C:\Users\chiar\miniconda3
set ENVNAME=thesis_env
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python C:\sofa\src\Chiara\Bats\Change_ee.py
call conda deactivate

echo 13 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Suture_taskLeft.py -a
echo 14 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Suture_taskLeft.py -a
echo 15 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Suture_taskLeft.py -a
echo 16 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Suture_taskLeft.py -a
echo 17 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Suture_taskLeft.py -a
echo 18 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Suture_taskLeft.py -a
echo 19 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Suture_taskLeft.py -a
echo 20 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Suture_taskLeft.py -a