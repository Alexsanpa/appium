from sapyautomation.core.watchers.reporter import LazyReporter

reporter = LazyReporter('sapyautomation')


class TrackerMeta(type):
    """ Metaclass to track data from tests.

    Args:
        name: Name of the child class.
        bases: bases of the child class.
        namespace: namespace of the child class.
    """

    def __init__(cls, name, bases, namespace):
        if 'BaseTestCases' in bases[0].__name__:
            reporter.add_registry_data(name)

        super(TrackerMeta, cls).__init__(name, bases, namespace)

    def __new__(mcs, name, bases, namespace):
        """ Registers the TestCases extended for use.

        Args:
            name: Name of the child class.
            bases: bases of the child class.
            namespace: namespace of the child class.

        Detects on every `__new__` if the class is a child
        from `BaseTestCases` and make a registry on the reporter.

        """

        cls = super(TrackerMeta, mcs).__new__(mcs, name, bases, namespace)

        if len(bases) > 0 and 'BaseTestCases' in bases[0].__name__:
            reporter.add_registry_data(name)

        return cls

    def __call__(cls, *args, **kwargs):
        """ Registers the tests instances

        Makes a registry on every `__call__` if the instance is a test.

        Returns:
            Working instance
        """
        instance = super(TrackerMeta, cls).__call__(*args, **kwargs)
        base = cls.__base__.__name__

        if base in reporter.registry_keys():
            reporter.add_registry_data(base, instance)
        return instance
