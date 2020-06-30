# randomly generate fake data on 1000 days
import numpy as np
data = np.random.random((1, 1000))
# construct the dlm of a linear trend and a 7-day seasonality
myDlm = dlm(data) + trend(degree = 2, 0.98) + seasonality(period = 7, 0.98)
# filter the result
myDlm.fitForwardFilter()
# extract the filtered result
myDlm.getFilteredObs()