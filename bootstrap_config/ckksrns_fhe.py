
from bootstrap_utils import *
from bootstrap_utils.ckksrns_utils import get_multiplicative_depth_by_coeff_vector
from ..bootstrap_enums import SecretKeyDist
from ckksrns_fhe_consts import *

def get_bootstrap_depth(level_budget, secret_key_dist: SecretKeyDist):
    approx_mod_depth = get_mod_depth_internal(secret_key_dist)

    return approx_mod_depth + level_budget[0] + level_budget[1]


def get_mod_depth_internal(secret_key_dist: SecretKeyDist):
    if secret_key_dist == SecretKeyDist.UNIFORM_TERNARY:
        return get_multiplicative_depth_by_coeff_vector(G_COEFFICIENTS_UNIFORM, False) + R_UNIFORM
    else:
        return get_multiplicative_depth_by_coeff_vector(G_COEFFICIENTS_SPARSE, False) + R_SPARSE