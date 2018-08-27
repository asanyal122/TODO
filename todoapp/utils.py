import random
import string

def code_generator(size=10, chars=string.ascii_lowercase + 
                                    string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_gid(instance, size=10):
    new_code = code_generator(size=size)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(gid=new_code).exists()
    if qs_exists:
        return create_shortcode(instance, size=size)
    return new_code