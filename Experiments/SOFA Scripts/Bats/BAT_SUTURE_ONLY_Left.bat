
rem RUN ID GUI----------------------------
set CONDAPATH=C:\Users\chiar\miniconda3
set ENVNAME=thesis_env
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python C:\sofa\src\Chiara\Bats\ID_GUI.py

echo 12 >> C:/sofa/src/Chiara/Repetitions.txt
runSofa C:\sofa\src\Chiara\Suture_taskLeft.py -a
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