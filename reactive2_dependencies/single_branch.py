from .reactive import Bus, Flag, handler, when, when_not

installed = Flag("installed")
configured = Flag("configured", requires={installed})
started = Flag("started", requires={configured})
available = Flag("available", requires={started})


@handler(when_not(installed))
def install():
    print("INSTALL")
    Bus.set_flag(installed)


@handler(
    when(installed),
    when_not(configured)
)
def configure():
    print("CONFIGURE")
    Bus.set_flag(configured)


@handler(
    when(configured),
    when_not(started)
)
def start():
    print("START")
    Bus.set_flag(started)


@handler(
    when(started),
    when_not(available)
)
def done():
    print("AVAILABLE")
    Bus.set_flag(available)


Bus.run()
