from constants.optimisation import MEAN, STD
def standardization_score(c, v, s, m):
    return  (c - MEAN["com"]) / STD["com"], \
            (v - MEAN["ver"]) / STD["ver"], \
            (s - MEAN["sim"]) / STD["sim"], \
            (m - MEAN["mul"]) / STD["mul"]