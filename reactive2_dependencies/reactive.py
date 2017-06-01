from functools import partial


class Bus:
    state_change = True
    handlers = set()

    @classmethod
    def set_flag(cls, flag):
        flag.state = True

        cls.state_change = True

    @classmethod
    def clear_flag(cls, flag):
        flag.state = False

        cls.state_change = True

    @classmethod
    def run(cls):
        while cls.state_change:
            cls.state_change = False

            for handler in cls.handlers:
                handler()


class Handler:
    def __init__(self, func, *predicates):
        self.func = func
        self.predicates = list(*predicates)

    def __call__(self, *args, **kwargs):
        for predicate in self.predicates:
            if not predicate():
                return

        self.func(*args, **kwargs)


class Flag:
    state = False
    dependencies = set()

    def __init__(self, name, requires=None):
        self.name = name

        if requires is not None:
            self.dependencies | set(requires)

    def __bool__(self):
        return self.state


def flag_is_active(flag):
    if not flag:
        return False

    for required_flag in flag.dependencies:
        if not when(required_flag):
            return False

    return True


def handler(*predicates):
    def decorator(func):
        handler = Handler(func, predicates)
        Bus.handlers.add(handler)
        return func
    return decorator


def when(flag):
    return partial(flag_is_active, flag)


def when_not(flag):
    def _when_not():
        return not flag_is_active(flag)
    return partial(_when_not)
