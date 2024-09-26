
def multiply(v, num):
    """
    pydoc string
    """
    
    # complexity +1
    if num < 0:
        return v

    cnt = 0
    r = 0

    # complexity +1
    while cnt < num:
        cnt += 1
        r += v

    return r


def divide(v, num):
    """
    pydoc string
    """

    # complexity +1
    if num < 0:
        return v

    return v / num


class TestClass:
    def __init__(self, val):
        self._val = val
    
    def __call__(self, val):
        if val < 0:
            return 0
        
        return val

    def execute(self, val):
        if val < 0:
            return 0
        
        return val