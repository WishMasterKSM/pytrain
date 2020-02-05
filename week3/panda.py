import pandas as pd
import numpy as np

def singleton(cls):
    instances = {}
    def create(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return create

@singleton
class TaskCounter:
    counter = 0

    def getTaskNumber(self):
        self.counter += 1
        return self.counter

def task_divider(func):
    def inner(*args, **kwargs):
        border = "-"
        header = border * 15
        taskCounter = TaskCounter()
        task_num = taskCounter.getTaskNumber()
        print(f'{header}{task_num}{header}')
        func(*args, **kwargs)
        print(border * 31)
    return inner

@task_divider
def task1(df):
    print(df)

@task_divider
def task2(df):
    df.replace("?", np.NaN, inplace=True)
    print(df.tail(20))

@task_divider
def task3(df):
    df_price = pd.to_numeric(df['price'])
    print(df.iloc[df_price.argmax()])

@task_divider
def task4(df):
    print(df.loc[df['company'] == 'toyota'])

@task_divider
def task5(df):
    print(df['company'].value_counts())

def main():
    df = pd.read_csv('Automobile_data.csv', index_col=0)
    task1(df)
    task2(df)
    task3(df)
    task4(df)
    task5(df)

if __name__ == '__main__':
    main()