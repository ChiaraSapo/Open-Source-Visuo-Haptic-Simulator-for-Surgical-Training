set CONDAPATH=C:\Users\chiar\miniconda3
set ENVNAME=thesis_env
set SIMULPATH=C:/sofa/src/Chiara

rem RUN ID GUI----------------------------
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python %SIMULPATH%\Bats\ID_GUI.py
call conda deactivate

rem RUN FAMILIARIZING GUI-----------------
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python %SIMULPATH%\Bats\Familiarizing_GUI.py
call conda deactivate

rem RUN FAMILIARIZING TASKS---------------
cd C:\sofa\build\v20.12.02\bin\Release
runSofa %SIMULPATH%\Trial_Line1_Left.py -a
runSofa %SIMULPATH%\Trial_Line2_Left.py -a
runSofa %SIMULPATH%\Trial_Line3_Left.py -a
runSofa %SIMULPATH%\Trial_Cube_Left.py -a
runSofa %SIMULPATH%\Trial_Sphere_Left.py -a


rem RUN TASK GUI--------------------------
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python %SIMULPATH%\Bats\Task_GUI.py
python %SIMULPATH%\Bats\Change_ee.py
call conda deactivate


rem RUN SURGICAL TASKS----------------------
echo 1 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Incision_task1_Left.py -a
echo 2 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Incision_task1_Left.py -a
echo 3 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Incision_task2_Left.py -a
echo 4 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Incision_task2_Left.py -a
echo 5 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Incision_task3_Left.py -a
echo 6 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Incision_task3_Left.py -a


rem RUN TASK GUI--------------------------
set CONDAPATH=C:\Users\chiar\miniconda3
set ENVNAME=thesis_env
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python %SIMULPATH%\Bats\Change_ee.py
call conda deactivate

rem trial
runSofa %SIMULPATH%\Rings_task_Left.py -a
echo 7 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Rings_task_Left.py -a
echo 8 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Rings_task_Left.py -a
echo 9 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Rings_task_Left.py -a
echo 10 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Rings_task_Left.py -a
echo 11 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Rings_task_Left.py -a
echo 12 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Rings_task_Left.py -a


rem RUN TASK GUI--------------------------
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python %SIMULPATH%\Bats\Change_ee.py
call conda deactivate

rem trial
runSofa %SIMULPATH%\Suture_task_Left.py -a
echo 13 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Suture_task_Left.py -a
echo 14 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Suture_task_Left.py -a
echo 15 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Suture_task_Left.py -a
echo 16 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Suture_task_Left.py -a
echo 17 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Suture_task_Left.py -a
echo 18 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Suture_task_Left.py -a
echo 19 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Suture_task_Left.py -a
echo 20 >> %SIMULPATH%/Repetitions.txt
runSofa %SIMULPATH%\Suture_task_Left.py -a