x = (1, 2, 2, 3)
y = (1, 2, 3, 6)

import numpy as np
import matplotlib.pyplot as plt

coeff = np.corrcoef(x=x, y=y)
print (coeff)

# Explanation:  https://www.khanacademy.org/math/ap-statistics/bivariate-data-ap/correlation-coefficient-r/v/calculating-correlation-coefficient-r
# Recipe:       https://docs.scipy.org/doc/numpy/reference/generated/numpy.corrcoef.html
