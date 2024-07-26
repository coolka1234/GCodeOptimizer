import regex
import sys
import os
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting main function")
    logging.info("Arguments: " + str(sys.argv))

    if len(sys.argv) < 2:
        logging.error("No input file provided")
        sys.exit(1)

    input_file = sys.argv[1]