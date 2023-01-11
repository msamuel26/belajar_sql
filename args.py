# *args digunakan untuk mem-passing selain dictionary, sedangkan **kwargs digunakan untuk
#   mem-passing hanya dictionary (pasangan key dan value)

def my_func(*args):
    for arg in args:
        print(arg)

my_func(1, 2, 3, "a", "b")

def my_func(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)

my_func(name="John", age=30, address='jln setip', city='semarang')

def my_func1(*args, **kwargs):
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(key, ":", value)
        
my_func1(1,2,3,name="John", age=30)
