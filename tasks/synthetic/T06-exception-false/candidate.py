# STATIC_RISK: broad-error-swallow
def safe_divide(a,b):
    try:
        return a/b
    except Exception:
        return None
