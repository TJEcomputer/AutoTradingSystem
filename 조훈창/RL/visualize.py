import matplotlib.pyplot as plt
import pandas as pd

class Visualize:


    def drawChart(self,x = None,y = None,style = None,title='Title',xlabel=None,ylabel=None,c=None):

        plt.figure(figsize=(20, 10))
        if style == 'plot':
            for data in y:
                plt.plot(x,data,c=c)
        if style == 'scatter':
            for data in y:
                plt.scatter(x,data,c=c)
        if style == 'bar':
            for data in y:
                plt.bar(x,data)
        if style == None:
            print('스타일을 지정해주세요.')
            return
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()



if __name__ =='__main__':
    df = pd.read_csv('.\\quant.csv')
    data1 = df.iloc[-1,1:]


    vi = Visualize()
    vi.drawChart(df.columns[1:],[data1],'bar','Episode action','Episode Step','action')

