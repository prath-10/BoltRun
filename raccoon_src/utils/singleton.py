class Singleton(type):
    """
    Singleton metaclass to ensure only one instance of a class is created.
    """
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance
