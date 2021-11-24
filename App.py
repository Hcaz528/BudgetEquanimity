import logging
from test_pkg import mock_data


def print_vs_logging():
    # Examples
    logging.debug('debug info')
    logging.info('just some info')
    logging.error('uh oh D:')


def main():
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)
    print_vs_logging()


if __name__ == '__main__':
    main()
