import matplotlib.pyplot as plt
import pandas as pd

class Visualize:


    def drawChart(self,x = None,y = None,style = None,title='Title',xlabel=None,ylabel=None,c=None):

        plt.figure(figsize=(1920,900))
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

        if style == 'pie':
            plt.pie(x, labels=y,autopct='%.2f%%',textprops = {'fontsize':13})
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks([0,100,200,300,400,500,600,700,800])
        plt.legend()
        plt.show()



if __name__ =='__main__':
    df = pd.read_csv('.\\action.csv')
    data1 = df.iloc[-1,1:]
    data = df.iloc[-1].value_counts()
    label = []
    for i in data.index:
        if i == 0:
            label.append('Holding')
        if i ==1:
            label.append('Buy')
        if i == 2:
            label.append('Sell')
    print(label)
    print(data.values)
    vi = Visualize()
    #vi.drawChart(df.columns[1:],[data1],'plot','Episode Profit','Episode Step','Profit')
    plt.figure(figsize=(1920, 900))
    plt.pie(data, labels=label,autopct='%.2f%%',textprops = {'fontsize':13})
    plt.title('Episode Action')
    plt.legend()
    plt.show()

