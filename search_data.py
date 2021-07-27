from os import read
import re
from math import log2
import matplotlib.pyplot as plt

with open("result.txt", 'r') as file:
    lines = file.readlines()
    parameters = re.compile("n:(\d{3,4}) w_c: (\d), w_r: (\d), p: (0.0?\d)")
    data = re.compile("There are (\d{2,3}) successes out of 100 tests")
    timing = re.compile("\AThe runtime for run took")
    def entropy(p): return - p*log2(p) - (1-p)*log2(1-p)
    parameterList = []
    timeList = []
    successList = []
    efficiency = []
    ending_point = [('2048', '3', '4', '0.1'), ('2000', '4','5', '0.1'), ('1920', '5', '6', '0.1')]
    for line in lines:
        set_para = parameters.search(line)
        if set_para != None:
            parameterList.append(set_para.groups())
        set_data = data.search(line)
        if set_data != None:
            successList.append(float(set_data.groups()[0]))
        set_timing = timing.search(line)
        if set_timing != None:
            index = line.find('k')
            timeRun = float(line[index+2:index+10])
            timeList.append(timeRun)
            efficiency.append(round(float(parameterList[-1][1])/(
                float(parameterList[-1][2])*(entropy(float(parameterList[-1][3])))), 3))
            if parameterList[-1] == ending_point[0]:
                length = [128, 256, 512, 1024, 2048]
#                listPro1 = [timeList[i*3]/100 for i in range(5)]
#                listPro2 = [timeList[i*3+1]/100 for i in range(5)]
#                listPro3 = [timeList[i*3+2]/100 for i in range(5)]
#                plt.plot(length, listPro1, label="w_c = 3, w_r = 4, p = 0.02")
#                plt.plot(length, listPro2, label="w_c = 3, w_r = 4, p = 0.05")
#                plt.plot(length, listPro3, label="w_c = 3, w_r = 4, p = 0.1")
#                plt.ylabel("Decoding time (s)")
#                plt.legend()
#                plt.show()
#                listSuccess1 = [successList[i*3] for i in range(5)]
#                listSuccess2 = [successList[i*3+1] for i in range(5)]
#                listSuccess3 = [successList[i*3+2] for i in range(5)]
#                plt.plot(length, listSuccess1, label="w_c = 3, w_r = 4, p = 0.02")
#                plt.plot(length, listSuccess2, label="w_c = 3, w_r = 4, p = 0.05")
#                plt.plot(length, listSuccess3, label="w_c = 3, w_r = 4, p = 0.1")
#                plt.ylabel("Succesful decoding (%)")
#                plt.legend()
#                plt.show()
#                listEff1 = [efficiency[i*3] for i in range(5)]
#                listEff2 = [efficiency[i*3+1] for i in range(5)]
#                listEff3 = [efficiency[i*3+2] for i in range(5)]
#                plt.plot(length, listEff1, label="w_c = 3, w_r = 4, p = 0.02")
#                plt.plot(length, listEff2, label="w_c = 3, w_r = 4, p = 0.05")
#                plt.plot(length, listEff3, label="w_c = 3, w_r = 4, p = 0.1")
#                plt.ylabel("Efficiency ")
#                plt.legend()
#                plt.show()
                parameterList = []
                timeList = []
                successList = []
                efficiency = []
                continue
            if parameterList[-1] == ending_point[1]:
                length = [125, 250, 500, 1000, 2000]
                timeThreePOne = []
                timeThreePTwo = []
                timeThreePThree = []
                timeFourPOne = []
                timeFourPTwo = []
                timeFourPThree = []
                SuccessThreePOne = []
                SuccessThreePTwo = []
                SuccessThreePThree = []
                SuccessFourPOne = []
                SuccessFourPTwo = []
                SuccessFourPThree = []
                EffThreePOne = []
                EffThreePTwo = []
                EffThreePThree = []
                EffFourPOne = []
                EffFourPTwo = []
                EffFourPThree = []
                for i in range(len(parameterList)):
                    if parameterList[i][1] == '3' and parameterList[i][3] == '0.02':
                        timeThreePOne.append(timeList[i])
                        SuccessThreePOne.append(successList[i])
                        EffThreePOne.append(efficiency[i])
                    if parameterList[i][1] == '3' and parameterList[i][3] == '0.05':
                        timeThreePTwo.append(timeList[i])
                        SuccessThreePTwo.append(successList[i])
                        EffThreePTwo.append(efficiency[i])
                    if parameterList[i][1] == '3' and parameterList[i][3] == '0.1':
                        timeThreePThree.append(timeList[i])
                        SuccessThreePThree.append(successList[i])
                        EffThreePThree.append(efficiency[i])
                    if parameterList[i][1] == '4' and parameterList[i][3] == '0.02':
                        timeFourPOne.append(timeList[i])
                        SuccessFourPOne.append(successList[i])
                        EffFourPOne.append(efficiency[i])
                    if parameterList[i][1] == '4' and parameterList[i][3] == '0.05':
                        timeFourPTwo.append(timeList[i])
                        SuccessFourPTwo.append(successList[i])
                        EffFourPTwo.append(efficiency[i])
                    if parameterList[i][1] == '4' and parameterList[i][3] == '0.1':
                        timeFourPThree.append(timeList[i])
                        SuccessFourPThree.append(successList[i])
                        EffFourPThree.append(efficiency[i])
                plt.figure(1)
                plt.plot(length, timeThreePOne, label = "w_c = 3, w_r = 5, p = 0.02")
                plt.plot(length, timeThreePTwo, label = "w_c = 3, w_r = 5, p = 0.05")
                plt.plot(length, timeThreePThree, label = "w_c = 3, w_r = 5, p = 0.1")
                plt.plot(length, timeFourPOne, label = "w_c = 4, w_r = 5, p = 0.02")
                plt.plot(length, timeFourPTwo, label = "w_c = 4, w_r = 5, p = 0.05")
                plt.plot(length, timeFourPThree, label = "w_c = 4, w_r = 5, p = 0.1")                                                                
                plt.ylabel("Time(s)")
                plt.legend()
                plt.figure(2)
                plt.plot(length, SuccessThreePOne, label = "w_c = 3, w_r = 5, p = 0.02")
                plt.plot(length, SuccessThreePTwo, label = "w_c = 3, w_r = 5, p = 0.05")
                plt.plot(length, SuccessThreePThree, label = "w_c = 3, w_r = 5, p = 0.1")
                plt.plot(length, SuccessFourPOne, label = "w_c = 4, w_r = 5, p = 0.02")
                plt.plot(length, SuccessFourPTwo, label = "w_c = 4, w_r = 5, p = 0.05")
                plt.plot(length, SuccessFourPThree, label = "w_c = 4, w_r = 5, p = 0.1")                                                                
                plt.ylabel("Successful decoding (%)")
                plt.legend()
                plt.figure(3)
                plt.plot(length, EffThreePOne, label = "w_c = 3, w_r = 5, p = 0.02")
                plt.plot(length, EffThreePTwo, label = "w_c = 3, w_r = 5, p = 0.05")
                plt.plot(length, EffThreePThree, label = "w_c = 3, w_r = 5, p = 0.1")
                plt.plot(length, EffFourPOne, label = "w_c = 4, w_r = 5, p = 0.02")
                plt.plot(length, EffFourPTwo, label = "w_c = 4, w_r = 5, p = 0.05")
                plt.plot(length, EffFourPThree, label = "w_c = 4, w_r = 5, p = 0.1")                                                                
                plt.ylabel("Efficiency")
                plt.legend()                      
                plt.show()
                        


                                 

#        time = re.compile("The runtime for run took 15.477386474609375 seconds to complete")
