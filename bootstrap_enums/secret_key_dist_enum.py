from enum import Enum

class SecretKeyDist(Enum):
    GAUSSIAN = 0
    UNIFORM_TERNARY = 1 # Default value
    SPARSE_TERNARY = 2