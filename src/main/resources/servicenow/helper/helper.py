#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#


def assert_not_null(val, error_msg):
    if not bool(val):
        raise RuntimeError(error_msg)
