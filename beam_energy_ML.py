import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

X = np.array([0, 0.4, 0.8, 1.2, 1.6, 2, 2.4, 2.8, 3.2, 3.6, 4, 4.4, 4.8, 5.2])
y = np.array([0.5, 0.65, 0.95, 1.25, 1.6, 1.95, 2.25, 2.6, 2.95, 3.3, 3.6, 3.94, 4.25, 4.6])
poly_reg = PolynomialFeatures(degree=5)
X_poly = poly_reg.fit_transform(X.reshape(-1, 1))
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly, y.reshape(-1, 1))

def beam_energy(current):
    y_pred = lin_reg_2.predict(poly_reg.fit_transform(np.array([current]).reshape(1, -1)))
    # plt.figure(figsize=(10,8))
    # plt.scatter(X, y)
    # plt.scatter(current, y_pred)
    # plt.show()
    return y_pred[0, 0]

