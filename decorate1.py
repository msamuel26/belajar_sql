# Decorator pada Python yaitu melakukan aktivitas sebelum fungsi dipanggil dan setelah fungsi dipanggil, dan atau
#   ada yang sebelum fungsi dipanggil saja dan atau ada yang setelah fungsi dipanggil saja

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_whee():
    print("Whee!")

say_whee()

def dekorasi_ku(func):
    def wrapper():
        print("menyapu")
        print("mandi")
        print("makan")
        func()
        print("diantar bapak pake nmax")
    return wrapper

def dekorasi_sebelum(func):
    def wrapper():
        print("sebelum fungsi dijalankan")
        func()
    return wrapper

@dekorasi_sebelum 
def makan():
    print("makan")

# makan()

@dekorasi_ku
def brngkt_skul():
    print("berangkat skul")

# brngkt_skul()

def dekorasi_setelah(func):
    def wrapper():
        func()
        print("mandi")
    return wrapper

@dekorasi_setelah
def pulang_sekolah():
    print("pulang sekolah")

# pulang_sekolah()

# say_whee = my_decorator(say_whee)

# say_whee()

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function call")
        result = func(*args, **kwargs)
        print("After the function call")
        return result
    return wrapper

@my_decorator
def add(a, b):
    return a + b

result = add(3, 4)
print(result)
