import os

import pytest


def pytest_addoption(parser):
    parser.addoption('--catch-warnings',
                     action='store_true', help='show all warnings and raise deprecation warnings')


def pytest_configure(config):
    if config.option.catch_warnings:
        import warnings

        # sys warnings
        warnings.simplefilter('error', DeprecationWarning)
        warnings.simplefilter('default', PendingDeprecationWarning)

        warnings.simplefilter('error', FutureWarning)

        warnings.simplefilter('always', RuntimeWarning)
        warnings.simplefilter('always', ImportWarning)
        warnings.simplefilter('always', UserWarning)
        warnings.simplefilter('always', UnicodeWarning)

    if 'slowtest' not in config.option.markexpr:
        if config.option.markexpr:
            config.option.markexpr += ' and not slowtest'
        else:
            config.option.markexpr = 'not slowtest'
