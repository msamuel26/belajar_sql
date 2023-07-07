def my_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        num = 2
        print("nilai awal:", num)
        result = result + num
        result = result * num
        print("nilai akhir:", result)
        return result
    return wrapper

@my_decorator
def add(a, b):
    print("ini eksekusi fungsi add")
    c = a + b
    return c

result = add(3, 4)
print(result)