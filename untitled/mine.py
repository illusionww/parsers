import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

Y = np.random.normal(0.0, 1.0, 50)
X = np.exp(Y)
mean = X.mean()
print "mean", mean

def findT():
    Xboot_idx = np.random.randint(0, len(X), len(X))
    Xboot = np.array([X[idx] for idx in Xboot_idx])
    sigma = np.std(Xboot, dtype=np.float64)

    return ((Xboot - Xboot.mean())**3).mean()/(sigma**3)

Tarray = np.array([findT() for _ in range(1000)])
v_boot = ((Tarray - Tarray.mean())**2).mean()