"""
Utility module for random number generation.
"""

import random

_sys_random = random.SystemRandom()


def get_random_int(length: int | None = None) -> int:
    """
    Generate a random integer with a length between 2 and 16 digits.

    Uses the OS entropy source (SystemRandom) so that previous calls
    to random.seed() do not make the returned values deterministic.

    :param length: Optional specific length (between 2 and 16).
                   If None, a random length between 2 and 16 is chosen.
    :return: A random integer of the requested length.
    :raises ValueError: If length is specified but outside [2, 16].
    """
    if length is None:
        length = _sys_random.randint(2, 16)
    elif not 2 <= length <= 16:
        raise ValueError("length must be between 2 and 16 digits")

    min_val = 10 ** (length - 1)
    max_val = (10**length) - 1
    return _sys_random.randint(min_val, max_val)
