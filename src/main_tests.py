import unittest


def test_adamnite(verbosity=0):
    loader = unittest.TestLoader()
    suite = loader.discover('./')
    assert unittest.TextTestRunner(
        verbosity=verbosity
    ).run(suite).wasSuccessful()


if __name__ == '__main__':
    test_adamnite(verbosity=2)
