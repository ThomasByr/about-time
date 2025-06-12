from .features import FEATURES, conv_space
from .human_count import fn_human_count

SPEC = (
    (24.0, "/d", 2),
    (60.0, "/h", 1),
    (60.0, "/m", 1),
    # "/s" in code.
)


def __human_throughput(val: float, unit: str, prec: int, space: str, fn_count) -> str:
    val *= 60.0 * 60.0 * 24.0
    for size, scale, dec in SPEC:
        r = round(val, dec)
        if r >= size:
            val /= size
            continue

        if prec is not None:
            r = round(val, prec)
        elif r % 1.0 == 0.0:
            prec = 0
        elif (r * 10.0) % 1.0 == 0.0:
            prec = 1
        else:
            prec = 2
        return "{:.{}f}{}{}{}".format(r, prec, space, unit, scale)

    return f"{fn_count(val, unit, prec)}/s"


def fn_human_throughput(space: bool, d1024: bool, iec: bool):
    def run(val: float, unit: str, prec: int):
        return __human_throughput(val, unit, prec, space, fn_count)

    fn_count = fn_human_count(space, d1024, iec)
    space = conv_space(space)
    return run


class HumanThroughput:
    def __init__(self, value, unit):
        assert value >= 0.0
        self._value = value
        self._unit = unit

    @property
    def value(self):
        return self._value

    def unit(self, value: str) -> "HumanThroughput":
        self._unit = value
        return self

    def as_human(self, prec: int = None) -> str:
        """Return a beautiful representation of this count.
        It dynamically calculates the best scale to use.

        Args:
            prec: an optional custom precision

        Returns:
            the human friendly representation.

        """
        return fn_human_throughput(FEATURES.feature_space, FEATURES.feature_1024, FEATURES.feature_iec)(
            self._value, self._unit, prec
        )

    def __str__(self):
        return self.as_human()

    def __repr__(self):  # pragma: no cover
        return f"HumanCount{{ value={self._value} }} -> {self}"

    def __eq__(self, other):
        return self.__str__() == other
