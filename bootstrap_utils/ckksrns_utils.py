from bootstrap_enums.degree_bounds_enum import DegreeBounds


def generate_depth_by_degree_table():
    depth_table = [0] * (DegreeBounds.UPPER_BOUND_DEGREE.value + 1)

    # Fill the depth table based on the degree ranges
    depth_table[:5] = [3] * 5       # degree in [0,4], depth = 3
    depth_table[5:6] = [4] * 1      # degree in [5], depth = 4
    depth_table[6:14] = [5] * 8     # degree in [6,13], depth = 5
    depth_table[14:28] = [6] * 14   # degree in [14,27], depth = 6
    depth_table[28:60] = [7] * 32   # degree in [28,59], depth = 7
    depth_table[60:120] = [8] * 60  # degree in [60,119], depth = 8
    depth_table[120:248] = [9] * 128 # degree in [120,247], depth = 9
    depth_table[248:496] = [10] * 248 # degree in [248,495], depth = 10
    depth_table[496:1008] = [11] * 512 # degree in [496,1007], depth = 11
    depth_table[1008:] = [12] * (DegreeBounds.UPPER_BOUND_DEGREE.value - 1007) # degree in [1008,2031], depth = 12

    return depth_table

DEPTH_TABLE = generate_depth_by_degree_table()

def get_depth_by_degree(degree):
    if DegreeBounds.LOWER_BOUND_DEGREE.value <= degree <= DegreeBounds.UPPER_BOUND_DEGREE.value:
        return DEPTH_TABLE[degree]
    
    raise ValueError(f"Polynomial degree is supported from {DegreeBounds.LOWER_BOUND_DEGREE.value} to {DegreeBounds.UPPER_BOUND_DEGREE.value} inclusive. Given: {degree}")


def get_multiplicative_depth_by_coeff_vector(vec, is_normalized):
    vec_size = len(vec)
    
    if vec_size == 0:
        raise ValueError("Cannot perform operation on empty vector. vec.size() == 0")
    
    degree = vec_size - 1
    mult_depth = get_depth_by_degree(degree)  

    return mult_depth - 1 if is_normalized else mult_depth
