class OnlyMeta(type):
    def __setattr__(cls, name, arg):
        if cls._finished_decoration:
            raise TypeError("Class Only classes are immutable")
        return super().__setattr__(name, arg)
