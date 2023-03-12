import numpy as np


class Metrics:
    def __init__(self):
        pass

    def TTR0(self, rate):
        weight = 1.5

        if (rate>=0 and rate<4):
            rate = 30
        rate = min(rate, 45)

        x0=[4,14]
        y0=[100,65]
        x1=[14,45]
        y1=[65,0]

        x = rate
        if x>=x0[0] and x<=x0[1]:
            y = np.interp(x, x0,y0)
            
        elif x>=x1[0] and x<=x1[1]:
            y = np.interp(x, x1,y1)
        
        probability = y * weight
        return probability
    
    def CR1(self, rating):
        weight = 1

        # 1-1 mapping
        probability = rating * weight
        return probability
    
    def TS2(self, size):  
        weight = 1

        size = min(size,30)

        x0=[1,3]
        y0=[0,20]
        x1=[4,10]
        y1=[60,100]
        x2=[10,16]
        y2=[100,70]
        x3=[17,30]
        y3=[60,20]

        x = size

        if x>=x0[0] and x<=x0[1]:
            y = np.interp(x, x0,y0)
            
        elif x>=x1[0] and x<=x1[1]:
            y = np.interp(x, x1,y1)

        elif x>=x2[0] and x<=x2[1]:
            y = np.interp(x, x2,y2)

        elif x>=x3[0] and x<=x3[1]:
            y = np.interp(x, x3,y3)

        probability = y * weight
        return probability
    
    
    def M3(self, morale):
        weight = 1
        # 1-1 mapping
        probability = morale * weight
        return probability
    
    def SPI4(self, index):
        weight = 2
        index = min(index, 1.8)

        x0=[0,1]
        y0=[0,95]
        x1=[1,1.8]
        y1=[95,100]

        x = index

        if x>=x0[0] and x<=x0[1]:
            y = np.interp(x, x0,y0)
            
        elif x>=x1[0] and x<=x1[1]:
            y = np.interp(x, x1,y1)
        
        probability = y * weight
        return probability
    
    def CPI5(self, index):
        weight = 2
        index = min(index, 1.8)

        x0=[0,1]
        y0=[0,95]
        x1=[1,1.8]
        y1=[95,100]

        x = index

        if x>=x0[0] and x<=x0[1]:
            y = np.interp(x, x0,y0)
            
        elif x>=x1[0] and x<=x1[1]:
            y = np.interp(x, x1,y1)
        
        probability = y * weight
        return probability
        
    def CQ6(self, quality):
        weight = 1.5

        # 1-1 mapping
        probability = quality * weight
        return probability
    
    #When changing CRF distribution, change evaluation graph direction
    def CRF7(self, freq):
        weight = 1
        freq = min(freq, 10)
        
        x0=[0,7,10]
        y0=[0,85,100]

        y = np.interp(freq, x0,y0)
        probability = y * weight
        return probability
    
    def DF8(self, freq):
        weight = 1
        freq = min(freq, 20)

        x0=[0,7]
        y0=[0,90]
        x1=[7,20]
        y1=[90,100]

        x=freq

        if x>=x0[0] and x<=x0[1]:
            y = np.interp(x, x0,y0)
            
        elif x>=x1[0] and x<=x1[1]:
            y = np.interp(x, x1,y1)
        
        probability = y * weight
        return probability
    

    def TSR9(self, rate):
        weight = 1.5

        # 1-1 mapping
        probability = rate * weight
        return probability
    
    def CC10(self, churn):
        weight = 1
        
        x0=[0,20]
        y0=[50,100]
        x1=[20,100]
        y1=[100,0]

        x = churn

        if x>=x0[0] and x<=x0[1]:
            y = np.interp(x, x0,y0)
            
        elif x>=x1[0] and x<=x1[1]:
            y = np.interp(x, x1,y1)
        
        probability = y * weight
        return probability
    
    def successProbability(self, arr):
        probability = (self.TTR0(arr[0]) + self.CR1(arr[1]) + self.TS2(arr[2]) + self.M3(arr[3]) + self.SPI4(arr[4]) + self.CPI5(arr[5]) + self.CQ6(arr[6]) + self.CRF7(arr[7]) + self.DF8(arr[8]) + self.TSR9(arr[9]) + self.CC10(arr[10])) / 14.5

        return probability
    
