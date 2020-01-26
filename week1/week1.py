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

def all_logged(func):
    def inner(*args, **kwargs):
        print(args)
        print(kwargs)
        result = func(*args, **kwargs)
        print(result)
        return result
    return inner

@task_divider
@all_logged
def first(a,b):
    return a+b;

@task_divider
def second():
    file_name = input("Enter file name: ")
    i = 0;
    with open(file_name, 'r') as input_file:
        for line in input_file:
            i = i + 1;
            print(f'Line #{i} : {line}')
            key = input("Continue? ")
            if (key == 'n'):
                break;

def main():
    first(1,b=2)
    second()

main()