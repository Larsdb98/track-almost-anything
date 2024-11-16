import argparse


def app_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--log-level", type=str, default="INFO")
    parser.add_argument("--log-dir", type=str, default="")

    arg = parser.parse_args()
    return arg
