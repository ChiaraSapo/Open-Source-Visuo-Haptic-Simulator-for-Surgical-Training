import numpy as np

def read():
    ConfigName=open('C:/sofa/src/Chiara/Config.txt')
    for line in ConfigName:
        pass
    user_name = line
    ConfigName.close()

    ConfigNumber=open('C:/sofa/src/Chiara/Repetitions.txt')
    lines = ConfigNumber.readlines()
    RepNumber=int(lines[-1])
    print("rep is",RepNumber)
    ConfigNumber.close()

    return [RepNumber,user_name]