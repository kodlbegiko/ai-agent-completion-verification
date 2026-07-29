from candidate import *
try:
    safe_divide('x',2)
except TypeError:
    pass
else:
    raise AssertionError('TypeError must propagate')
