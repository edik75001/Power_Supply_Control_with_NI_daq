import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

X_ = np.array([0, 0.4, 0.8, 1.2, 1.6, 2, 2.4, 2.8, 3.2, 3.6, 4, 4.4, 4.8, 5.2])
y_ = np.array([0, 10, 30, 40, 50, 65, 75, 87, 97, 112, 122, 132, 142, 155])

poly_reg = PolynomialFeatures(degree=5)
X_poly = poly_reg.fit_transform(X_.reshape(-1, 1))
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly, y_.reshape(-1, 1))




def dip_field(current):
    k = poly_reg.fit_transform(np.array(current).reshape(-1, 1))
    y_pred = lin_reg_2.predict(k)
    return y_pred[0,0]








