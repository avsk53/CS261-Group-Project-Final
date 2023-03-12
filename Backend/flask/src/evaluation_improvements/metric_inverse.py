import numpy as np


class MetricInverse:
    def __init__(self):
        pass
    
    def TTR0_inverse(self, prob):
        x0=[14,4]
        y0=[65,100]
        x1=[45,14]
        y1=[0,65]

        if prob>=y0[0] and prob<=y0[1]:
            x = np.interp(prob, y0,x0)
            
        elif prob>=y1[0] and prob<=y1[1]:
            x = np.interp(prob, y1,x1)

        return x

    def CR1_inverse(self, prob):
        return prob

    def TS2_inverse(self, prob):

        x0=[1,3]
        y0=[0,20]
        x1=[4,10]
        y1=[60,100]
        x2=[16,10]
        y2=[70,100]
        x3=[30,17]
        y3=[20,60]

        if prob>=y0[0] and prob<=y0[1]:
            x = np.interp(prob, y0,x0)
            
        elif prob>=y1[0] and prob<=y1[1]:
            x = np.interp(prob, y1,x1)

        elif prob>=y2[0] and prob<=y2[1]:
            x = np.interp(prob, y2,x2)

        elif prob>=y3[0] and prob<=y3[1]:
            x = np.interp(prob, y3,x3)
        
        return int(x)
    
    def M3_inverse(self, prob):
        return prob
    
    def SPI4_inverse(self, prob):
        x0=[0,1]
        y0=[0,95]
        x1=[1,1.8]
        y1=[95,100]

        if prob>=y0[0] and prob<=y0[1]:
            x = np.interp(prob, y0,x0)
            
        elif prob>=y1[0] and prob<=y1[1]:
            x = np.interp(prob, y1,x1)

        return x

    def CPI5_inverse(self, prob):
        x0=[0,1]
        y0=[0,95]
        x1=[1,1.8]
        y1=[95,100]

        if prob>=y0[0] and prob<=y0[1]:
            x = np.interp(prob, y0,x0)
            
        elif prob>=y1[0] and prob<=y1[1]:
            x = np.interp(prob, y1,x1)

        return x

    def CQ6_inverse(self, prob):
        return prob

    def CRF7_inverse(self, prob):
        x0=[0,7,10]
        y0=[0,85,100]
        
        x = np.interp(prob, y0,x0)

        return x

    def DF8_inverse(self, prob):
        x0=[0.25,7]
        y0=[0,90]
        x1=[7,20]
        y1=[90,100]
        if prob>=y0[0] and prob<=y0[1]:
            x = np.interp(prob, y0,x0)
            
        elif prob>=y1[0] and prob<=y1[1]:
            x = np.interp(prob, y1,x1)

        return x


    def TSR9_inverse(self, prob):
        return prob
    
    def CC10_inverse(self, prob):
        
        x0=[0,20]
        y0=[50,100]
        x1=[100,20]
        y1=[0,100]

        if prob>=y0[0] and prob<=y0[1]:
            x = np.interp(prob, y0,x0)
            
        elif prob>=y1[0] and prob<=y1[1]:
            x = np.interp(prob, y1,x1)

        return x
    






        


