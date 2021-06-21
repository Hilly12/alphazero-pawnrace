from typing import Tuple

class Move:
    def __init__(self, fr: Tuple[int, int], to: Tuple[int, int], capture: bool, enpassant: bool):
        self.fr = fr
        self.to = to
        self.capture = capture
        self.enpassant = enpassant

    def is_double_push(self):
        return abs(self.fr[0] - self.to[0]) == 2

    def __str__(self) -> str:
        f = chr(self.fr[1] + ord("a")) + chr(self.fr[0] + ord("1"))
        t = chr(self.to[1] + ord("a")) + chr(self.to[0] + ord("1"))
        return (
            f + ("x" if self.capture else "-") + t + (" ep" if self.enpassant else "")
        )

    def __repr__(self) -> str:
        return self.__str__()