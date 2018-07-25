
def assert_not_null(val, error_msg):
    if not bool(val):
        raise RuntimeError(error_msg)
