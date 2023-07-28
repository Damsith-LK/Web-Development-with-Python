# For understanding how Flask works, decorator funcs are essential
import time

# Example decorator
def dec_func(func):
    """Functions can be returned from other functions in Python"""
    def wrapper():
        print("This function is decorated and you are gonna experience a 2 second delay!!!")
        time.sleep(2)
        func()
        print("Cool, isn't it?\n")
    return wrapper

# Some funcs
# And we can use decorator with these func using "@", which is also known as sugar syntax
@dec_func
def hello():
    print("Hello, duh")

def curse():
    print("Screw you, dawg")

@dec_func
def praise():
    print("Damn, you are so cool")

def bye():
    print("Bye, see you later")


# This func has decorator
hello()

# This doesn't
curse()

# Decorated funcs can be called this way too...
dec_output = dec_func(bye)
dec_output()