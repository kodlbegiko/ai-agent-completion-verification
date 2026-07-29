# STATIC_RISK: mutable-module-state
_ITEMS=[]
def collect(value):
    global _ITEMS
    _ITEMS.append(value)
    return list(_ITEMS)
