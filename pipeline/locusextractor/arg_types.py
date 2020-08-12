import argparse
import os

def proportional_float(value):
    fvalue = float(value)
    if (fvalue < 0) or (fvalue > 1):
        raise argparse.ArgumentTypeError("%s is an invalid positive number" % value)
    return fvalue

def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))