from os import read
import re
from math import log2
import matplotlib.pyplot as plt

with open("result3.txt", 'r') as file:
    lines = file.readlines()
    parameters = re.compile("n:(\d{3,4}) w_c: (\d), w_r: (\d), p: (0.0?\d)")
    data = re.compile("There are (\d{1,2}) successes out of 20 tests")
#    test_phrase = re.compile("\AThere are")
    timing = re.compile("\AThe runtime")
    def entropy(p): return - p*log2(p) - (1-p)*log2(1-p)
    parameterList = []
    timeList = []
    successList = []
    efficiency = []
    ending_point = [('504', '4', '9', '0.08'), ('2016', '4','9', '0.08'), ('20160', '4', '9', '0.08')]
    for line in lines:
        set_para = parameters.search(line)
        if set_para != None:
            parameterList.append(set_para.groups())
        set_data = data.search(line)
        if set_data != None:
            successList.append(int(set_data.groups()[0]))
            print(f"The value of number of success: {int(set_data.groups()[0])}")
#        test_phr = test_phrase.search(line)
#        if test_phr != None:
#            print(line)
        set_timing = timing.search(line)
        if set_timing != None:
            index = line.find('k')
            timeRun = float(line[index+2:index+10])
            timeList.append(timeRun)
            efficiency.append(round(float(parameterList[-1][1])/(
                float(parameterList[-1][2])*(entropy(float(parameterList[-1][3])))), 3))
            if parameterList[-1] == ending_point[0]:
                length = [504, 2016, 20160]
                listPro1 = [timeList[i*3] for i in range(3)]
                listPro2 = [timeList[i*3+1] for i in range(3)]
                listPro3 = [timeList[i*3+2] for i in range(3)]
                plt.figure(1)
                plt.plot(length, listPro1, label="w_c/w_r = 1/2, p = 0.05")
                plt.plot(length, listPro2, label="w_c/w_r = 1/2, p = 0.07")
                plt.plot(length, listPro3, label="w_c/w_r = 1/2, p = 0.08")
                plt.ylabel("Time (s)")
                plt.xlabel("Block size")
                plt.legend()
#                listSuccess1 = [successList[i*3] for i in range(5)]
#                listSuccess2 = [successList[i*3+1] for i in range(5)]
#                listSuccess3 = [successList[i*3+2] for i in range(5)]
#                plt.plot(length, listSuccess1, label="w_c = 3, w_r = 4, p = 0.02")
#                plt.plot(length, listSuccess2, label="w_c = 3, w_r = 4, p = 0.05")
#                plt.plot(length, listSuccess3, label="w_c = 3, w_r = 4, p = 0.1")
#                plt.ylabel("Succesful decoding (%)")
#                plt.legend()
#                listEff1 = [efficiency[i*3] for i in range(5)]
#                listEff2 = [efficiency[i*3+1] for i in range(5)]
#                listEff3 = [efficiency[i*3+2] for i in range(5)]
#                plt.plot(length, listEff1, label="w_c = 3, w_r = 4, p = 0.02")
#                plt.plot(length, listEff2, label="w_c = 3, w_r = 4, p = 0.05")
#                plt.plot(length, listEff3, label="w_c = 3, w_r = 4, p = 0.1")
#                plt.ylabel("Efficiency ")
                plt.legend()
                parameterList = []
                timeList = []
                successList = []
                efficiency = []
                continue
            if parameterList[-1] == ending_point[1]:
                length = [504, 2016, 20160]
                timeThreePOne = []
                timeThreePTwo = []
                timeThreePThree = []
                timeFourPOne = []
                timeFourPTwo = []
                timeFourPThree = []
#                SuccessThreePOne = []
#                SuccessThreePTwo = []
#                SuccessThreePThree = []
#                SuccessFourPOne = []
#                SuccessFourPTwo = []
#                SuccessFourPThree = []
#                EffThreePOne = []
#                EffThreePTwo = []
#                EffThreePThree = []
#                EffFourPOne = []
#                EffFourPTwo = []
#                EffFourPThree = []
                for i in range(len(parameterList)):
                    if parameterList[i][1] == '3' and parameterList[i][3] == '0.05':
                        timeThreePOne.append(timeList[i])
#                        SuccessThreePOne.append(successList[i])
#                        EffThreePOne.append(efficiency[i])
                    if parameterList[i][1] == '3' and parameterList[i][3] == '0.07':
                        timeThreePTwo.append(timeList[i])
#                        SuccessThreePTwo.append(successList[i])
#                        EffThreePTwo.append(efficiency[i])
                    if parameterList[i][1] == '3' and parameterList[i][3] == '0.08':
                        timeThreePThree.append(timeList[i])
#                        SuccessThreePThree.append(successList[i])
#                        EffThreePThree.append(efficiency[i])
                    if parameterList[i][1] == '4' and parameterList[i][3] == '0.02':
                        timeFourPOne.append(timeList[i])
#                        SuccessFourPOne.append(successList[i])
#                        EffFourPOne.append(efficiency[i])
                    if parameterList[i][1] == '4' and parameterList[i][3] == '0.05':
                        timeFourPTwo.append(timeList[i])
#                        SuccessFourPTwo.append(successList[i])
#                        EffFourPTwo.append(efficiency[i])
                    if parameterList[i][1] == '4' and parameterList[i][3] == '0.1':
                        timeFourPThree.append(timeList[i])
#                        SuccessFourPThree.append(successList[i])
#                        EffFourPThree.append(efficiency[i])
                plt.figure(2)
                plt.plot(length, timeThreePOne, label = "w_c/w_r = 3/5, p = 0.02")
                plt.plot(length, timeThreePTwo, label = "w_c/w_r = 3/5, p = 0.05")
                plt.plot(length, timeThreePThree, label = "w_c/w_r = 3/5, p = 0.1")
                plt.plot(length, timeFourPOne, label = "w_c/w_r = 4/5, p = 0.02")
                plt.plot(length, timeFourPTwo, label = "w_c/w_r = 4/5, p = 0.05")
                plt.plot(length, timeFourPThree, label = "w_c/w_r = 4/5, p = 0.1")                                                                
                plt.xlabel("Block size")
                plt.ylabel("Time(s)")
                plt.legend()
#                plt.figure(2)
#                plt.plot(length, SuccessThreePOne, label = "w_c/w_r = 3/5, p = 0.02")
#                plt.plot(length, SuccessThreePTwo, label = "w_c/w_r = 3/5, p = 0.05")
#                plt.plot(length, SuccessThreePThree, label = "w_c/w_r = 3/5, p = 0.1")
#                plt.plot(length, SuccessFourPOne, label = "w_c/w_r = 4/5, p = 0.02")
#                plt.plot(length, SuccessFourPTwo, label = "w_c/w_r = 4/5, p = 0.05")
#                plt.plot(length, SuccessFourPThree, label = "w_c/w_r = 4/5, p = 0.1")                                                                
#                plt.ylabel("Successful decoding (%)")
#                plt.legend()
#                plt.figure(3)
#                plt.plot(length, EffThreePOne, label = "w_c/w_r = 3/5, p = 0.02")
#                plt.plot(length, EffThreePTwo, label = "w_c/w_r = 3/5, p = 0.05")
#                plt.plot(length, EffThreePThree, label = "w_c/w_r = 3/5, p = 0.1")
#                plt.plot(length, EffFourPOne, label = "w_c/w_r = 4/5, p = 0.02")
#                plt.plot(length, EffFourPTwo, label = "w_c/w_r = 4/5, p = 0.05")
#                plt.plot(length, EffFourPThree, label = "w_c/w_r = 4/5, p = 0.1")                                                                
#                plt.ylabel("Efficiency")
#                plt.legend()                      
                parameterList = []
                timeList = []
                successList = []
                efficiency = []
                continue
            if parameterList[-1] == ending_point[2]:
                print("Length of parameterList" + str(len(parameterList)))
                print("Length of successList" + str(len(successList)))
                print("Length of timeList" + str(len(timeList)))
                length = [120, 240, 480, 960, 1920]
                timeThreePOne = []
                timeThreePTwo = []
                timeThreePThree = []
                timeFourPOne = []
                timeFourPTwo = []
                timeFourPThree = []
#                SuccessThreePOne = []
#                SuccessThreePTwo = []
#                SuccessThreePThree = []
#                SuccessFourPOne = []
#                SuccessFourPTwo = []
#                SuccessFourPThree = []
#                EffThreePOne = []
#                EffThreePTwo = []
#                EffThreePThree = []
#                EffFourPOne = []
#                EffFourPTwo = []
#                EffFourPThree = []
                for i in range(len(parameterList)):
                    if parameterList[i][1] == '4' and parameterList[i][3] == '0.02' and parameterList[i][2] == '6':
                        timeThreePOne.append(timeList[i])
#                        SuccessThreePOne.append(successList[i])
#                        EffThreePOne.append(efficiency[i])
                    if parameterList[i][1] == '4' and parameterList[i][3] == '0.05' and parameterList[i][2] == '6':
                        timeThreePTwo.append(timeList[i])
#                        SuccessThreePTwo.append(successList[i])
#                        EffThreePTwo.append(efficiency[i])
                    if parameterList[i][1] == '4' and parameterList[i][3] == '0.1'and parameterList[i][2] == '6':
                        timeThreePThree.append(timeList[i])
#                        SuccessThreePThree.append(successList[i])
#                        EffThreePThree.append(efficiency[i])
                    if parameterList[i][1] == '5' and parameterList[i][3] == '0.02'and parameterList[i][2] == '6':
                        timeFourPOne.append(timeList[i])
#                        SuccessFourPOne.append(successList[i])
#                        EffFourPOne.append(efficiency[i])
                    if parameterList[i][1] == '5' and parameterList[i][3] == '0.05'and parameterList[i][2] == '6':
                        timeFourPTwo.append(timeList[i])
#                        SuccessFourPTwo.append(successList[i])
#                        EffFourPTwo.append(efficiency[i])
                    if parameterList[i][1] == '5' and parameterList[i][3] == '0.1' and parameterList[i][2] == '6':
                        timeFourPThree.append(timeList[i])
#                        SuccessFourPThree.append(successList[i])
#                        EffFourPThree.append(efficiency[i])
                plt.figure(3)
                plt.plot(length, timeThreePOne, label = "w_c/w_r = 2/3, p = 0.02")
                plt.plot(length, timeThreePTwo, label = "w_c/w_r = 2/3, p = 0.05")
                plt.plot(length, timeThreePThree, label = "w_c/w_r = 2/3, p = 0.1")
                plt.plot(length, timeFourPOne, label = "w_c/w_r = 5/6, p = 0.02")
                plt.plot(length, timeFourPTwo, label = "w_c/w_r = 5/6, p = 0.05")
                plt.plot(length, timeFourPThree, label = "w_c/w_r = 5/6, p = 0.1")                                                                
                plt.ylabel("Time(s)")
                plt.xlabel("Block size")
                plt.legend()
#                plt.figure(2)
#                plt.plot(length, SuccessThreePOne, label = "w_c = 4, w_r = 6, p = 0.02")
#                plt.plot(length, SuccessThreePTwo, label = "w_c = 4, w_r = 6, p = 0.05")
#                plt.plot(length, SuccessThreePThree, label = "w_c = 4, w_r = 6, p = 0.1")
#                plt.plot(length, SuccessFourPOne, label = "w_c = 5, w_r = 6, p = 0.02")
#                plt.plot(length, SuccessFourPTwo, label = "w_c = 5, w_r = 6, p = 0.05")
#                plt.plot(length, SuccessFourPThree, label = "w_c = 5, w_r = 6, p = 0.1")                                                                
#                plt.ylabel("Successful decoding (%)")
#                plt.legend()
#                plt.figure(3)
#                plt.plot(length, EffThreePOne, label = "w_c = 4, w_r = 6, p = 0.02")
#                plt.plot(length, EffThreePTwo, label = "w_c = 4, w_r = 6, p = 0.05")
#                plt.plot(length, EffThreePThree, label = "w_c = 4, w_r = 6, p = 0.1")
#                plt.plot(length, EffFourPOne, label = "w_c = 5, w_r = 6, p = 0.02")
#                plt.plot(length, EffFourPTwo, label = "w_c = 5, w_r = 6, p = 0.05")
#                plt.plot(length, EffFourPThree, label = "w_c = 5, w_r = 6, p = 0.1")                                                                
#                plt.ylabel("Efficiency")
#                plt.legend()
            
    plt.show()
    print(parameterList)
    print(successList)
    print(timeList)                        


                                 

#        time = re.compile("The runtime for run took 15.477386474609375 seconds to complete")
