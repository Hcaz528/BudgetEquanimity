""" IMPORTS """
import logging


""" VARIABLES """


def print_vs_logging():
    # Examples
    logging.debug('debug info')
    logging.info('just some info')
    logging.error('uh oh D:')


""" FUNCITONS """


def main():
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)
    print_vs_logging()


""" MAIN """
if __name__ == '__main__':
    main()
