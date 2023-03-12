from metric_inverse import MetricInverse
from metric_distributions import Metrics
import random
import numpy as np

data = MetricInverse()
success = Metrics()


#Training-Testing split is 80/20

#Total =  150*9  +  300*2  +  450  = 2400
trainingDataCustom = 150
trainingDataUniform1 = 300
trainingDataUniform2 = 450

#Total =  40*9  +  75*2  +  90  = 600
testDataCustom = 40
testDataUniform1 = 75
testDataUniform2 = 90

def generate(IDstart, custom, uniform1, uniform2):
    projectID = IDstart
    count = 0
    for i in range(custom):
        arr = [[0]*11 for i in range(9)]
        metric = [[0]*12 for i in range(9)]


        for x in range(9):
            print("insert into project values('{}','P{}','now','now','1','a','2160810');".format(projectID, projectID))
            #Probability Range
            pr = [0 + (10*x),20 + (10*x)]
            for y in range(11):
                arr[x][y] = round(random.uniform(pr[0],pr[1]),3)

            
            metric[x][0] = data.TTR0_inverse(arr[x][0])
            metric[x][1] = data.CR1_inverse(arr[x][1])
            metric[x][2] = data.TS2_inverse(arr[x][2])
            metric[x][3] = data.M3_inverse(arr[x][3])
            metric[x][4] = data.SPI4_inverse(arr[x][4])
            metric[x][5] = data.CPI5_inverse(arr[x][5]) 
            metric[x][6] = data.CQ6_inverse(arr[x][6]) 
            metric[x][7] = data.CRF7_inverse(arr[x][7]) 
            metric[x][8] = data.DF8_inverse(arr[x][8]) 
            metric[x][9] = data.TSR9_inverse(arr[x][9]) 
            metric[x][10] = data.CC10_inverse(arr[x][10])
            
            metric[x][11] = success.successProbability(metric[x][0:11])
            count+=1

            print("insert into metric_assignment values(' 0','{}','{}'),(' 1','{}','{}'),(' 2','{}','{}'),(' 3','{}','{}'),(' 4','{}','{}'),(' 5','{}','{}'),(' 6','{}','{}'),(' 7','{}','{}'),(' 8','{}','{}'),(' 9','{}','{}'),('10','{}','{}'),('11','{}','{}');".format(projectID, metric[x][0], projectID, metric[x][1], projectID, metric[x][2], projectID, metric[x][3], projectID, metric[x][4], projectID, metric[x][5], projectID, metric[x][6], projectID, metric[x][7], projectID, metric[x][8], projectID, metric[x][9], projectID, metric[x][10], projectID, metric[x][11]))
            print()
            projectID+=1

    count = 0

    for i in range(uniform1):
        for m in range(2):
            print("insert into project values('{}','P{}','now','now','1','a','2160810');".format(projectID, projectID))
            pr = [0 + (50*m),50 + (50*m)]
            arr = [0] * 11
            metric = [0] * 12
            for i in range(11):
                arr[i] = round(random.uniform(pr[0],pr[1]),3)

            metric[0] = data.TTR0_inverse(arr[0])
            metric[1] = data.CR1_inverse(arr[1])
            metric[2] = data.TS2_inverse(arr[2])
            metric[3] = data.M3_inverse(arr[3])
            metric[4] = data.SPI4_inverse(arr[4])
            metric[5] = data.CPI5_inverse(arr[5]) 
            metric[6] = data.CQ6_inverse(arr[6]) 
            metric[7] = data.CRF7_inverse(arr[7]) 
            metric[8] = data.DF8_inverse(arr[8]) 
            metric[9] = data.TSR9_inverse(arr[9]) 
            metric[10] = data.CC10_inverse(arr[10])

            metric[11] = success.successProbability(metric[0:11])
            count +=1

            print("insert into metric_assignment values(' 0','{}','{}'),(' 1','{}','{}'),(' 2','{}','{}'),(' 3','{}','{}'),(' 4','{}','{}'),(' 5','{}','{}'),(' 6','{}','{}'),(' 7','{}','{}'),(' 8','{}','{}'),(' 9','{}','{}'),('10','{}','{}'),('11','{}','{}');".format(projectID, metric[0], projectID, metric[1], projectID, metric[2], projectID, metric[3], projectID, metric[4], projectID, metric[5], projectID, metric[6], projectID, metric[7], projectID, metric[8], projectID, metric[9], projectID, metric[10], projectID, metric[11]))
            print()
            projectID+= 1

    count = 0
    for i in range(uniform2):

        print("insert into project values('{}','P{}','now','now','1','a','2160810');".format(projectID, projectID))

        arr = [0] * 11
        metric = [0] * 12
        for i in range(11):
            arr[i] = round(random.uniform(0,100),3)

        metric[0] = data.TTR0_inverse(arr[0])
        metric[1] = data.CR1_inverse(arr[1])
        metric[2] = data.TS2_inverse(arr[2])
        metric[3] = data.M3_inverse(arr[3])
        metric[4] = data.SPI4_inverse(arr[4])
        metric[5] = data.CPI5_inverse(arr[5]) 
        metric[6] = data.CQ6_inverse(arr[6]) 
        metric[7] = data.CRF7_inverse(arr[7]) 
        metric[8] = data.DF8_inverse(arr[8]) 
        metric[9] = data.TSR9_inverse(arr[9]) 
        metric[10] = data.CC10_inverse(arr[10])

        metric[11] = success.successProbability(metric[0:11])
        count +=1

        print("insert into metric_assignment values(' 0','{}','{}'),(' 1','{}','{}'),(' 2','{}','{}'),(' 3','{}','{}'),(' 4','{}','{}'),(' 5','{}','{}'),(' 6','{}','{}'),(' 7','{}','{}'),(' 8','{}','{}'),(' 9','{}','{}'),('10','{}','{}'),('11','{}','{}');".format(projectID, metric[0], projectID, metric[1], projectID, metric[2], projectID, metric[3], projectID, metric[4], projectID, metric[5], projectID, metric[6], projectID, metric[7], projectID, metric[8], projectID, metric[9], projectID, metric[10], projectID, metric[11]))
        print()
        projectID+= 1


#generate(2001, trainingDataCustom, trainingDataUniform1, trainingDataUniform2)
#generate(5001, testDataCustom, testDataUniform1, testDataUniform2)

 







    

