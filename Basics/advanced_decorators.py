# Day 55
# Advanced decorators use *args and/or **kwargs
# In this, we have to do "wrapper(*args, **kwargs)"
# Advanced decorators are different from normal decorators because it wants arguments

class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False

damsith = User("Damsith-LK")

# So the idea of this is that the user needs to post a blog and a decorator is needed to check if the user is logged in
def is_logged_in_decorator(func):
    def wrapper(*args):
        """The first argument is expected to be a User object"""
        if args[0].is_logged_in:
            func(args[0])
        else:
            print("Back off, amateur")
    return wrapper


# The function for blog post
@is_logged_in_decorator
def post_blog(user: User):
    print(f"The new blog has been posted by {user.name}")

damsith.is_logged_in = True
post_blog(damsith)