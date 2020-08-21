import csv

def csv_reader(name):
    # 실행시 경로 문제가 발생하면 filename경로를 새로 지정 해주세요.
    # filename = 'C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\'+name
    filename = '..\\DB\\CSV\\'+name
    f = open(filename,'r')
    data = csv.reader(f)
    data_list = []
    for i in data:
        data_list.append(i)
    return data_list
    f.close()



def csv_writer_a(name,rows):
    # 실행시 경로 문제가 발생하면 filename경로를 새로 지정 해주세요.
    # filename = 'C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\'+name
    filename = '..\\DB\\CSV\\' + name
    f = open(filename,'a',newline='')

    wr = csv.writer(f)

    wr.writerow(rows)
    f.close()

def csv_writer_w(name,rows):
    # 실행시 경로 문제가 발생하면 filename경로를 새로 지정 해주세요.
    # filename = 'C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\'+name
    filename = '..\\DB\\CSV\\' + name
    f = open(filename,'w',newline='')
    wr = csv.writer(f)

    wr.writerow(rows)
    f.close()


