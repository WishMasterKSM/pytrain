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

@task_divider
def task6(df):
    print(df.groupby('company')['price'].max())

@task_divider
def task7(df):
    print(df.groupby('company')['average-mileage'].mean())

@task_divider
def task8(df):
    print(df.sort_values(by=['price']))

@task_divider
def task9(df):
    GermanCars = {'Company': ['Ford', 'Mercedes', 'BMV', 'Audi'], 'Price': [23845, 171995, 135925 , 71400]}
    JapaneseCars = {'Company': ['Toyota', 'Honda', 'Nissan', 'Mitsubishi'], 'Price': [29995, 23600, 61500 , 58900]}
    df1 = pd.DataFrame.from_dict(GermanCars)
    df2 = pd.DataFrame.from_dict(JapaneseCars)
    print(pd.concat([df1, df2], keys=["Germany", "Japan"]))

@task_divider
def task10(df):
    Car_Price = {'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 'Price': [23845, 17995, 135925 , 71400]}
    Car_Horsepower = {'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 'horsepower': [141, 80, 182 , 160]}
    df1 = pd.DataFrame.from_dict(Car_Price)
    df2 = pd.DataFrame.from_dict(Car_Horsepower)
    print(pd.merge(df1, df2, on="Company"))

def main():
    df = pd.read_csv('Automobile_data.csv', index_col=0)
    task1(df)
    task2(df)
    task3(df)
    task4(df)
    task5(df)
    task6(df)
    task7(df)
    task8(df)
    task9(df)
    task10(df)

if __name__ == '__main__':
    main()