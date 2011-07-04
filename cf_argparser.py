import argparse
import exceptions


class ArgumentError(exceptions.Exception):

    """Raise when incorrect arguments passed to ArgParseThrower."""

    def __init__(self, useage, error):
        self.useage = useage
        self.error = error
        exceptions.Exception.__init__(self, ''.join((useage, error)))


class ArgParseThrower(argparse.ArgumentParser):

    """Subclass argparse.ArgumentParser to overide error method."""

    def __init__(self, **kwargs):
        super(ArgParseThrower, self).__init__(**kwargs)

    def error(self, message):
        """Overide superclass error method.

        Print usage and error the raise exception instead of exiting program.
        """
        use = self.format_usage()
        err = ('%s: error: %s\n') % (self.prog, message)
        raise ArgumentError(use, err)
