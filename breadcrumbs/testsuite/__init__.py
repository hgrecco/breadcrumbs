"""
    breadcrumbs.testsuite
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2021 by breadcrumbs Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""


def run():
    """Run all tests."""

    try:
        import pytest
    except ImportError:
        print("pytest not installed. Install it\n    pip install pytest")
        raise

    return pytest.main()
