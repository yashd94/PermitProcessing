# Label + one-hot encoded features

from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso

parameters_lasso = {'alpha':[10**-4, 10**-3, 0.01, 0.06, 0.1, 0.3, 0.5]}
parameters_rr = {'alpha':[10**-4, 10**-3, 0.01, 0.06, 0.1, 0.3, 0.5]}
parameters_rf = {'n_estimators':[25, 40, 55], 'max_depth':[10, 20, 30]}

lasso = Lasso()
rr = Ridge()
rf = RandomForestRegressor()

lasso_grid_ohe = GridSearchCV(lasso, parameters_lasso, scoring='neg_mean_absolute_error')
rr_grid_ohe = GridSearchCV(rr, parameters_rr, scoring='neg_mean_absolute_error')
rf_grid_ohe = GridSearchCV(rf, parameters_rf, scoring='neg_mean_absolute_error')

lasso_grid_ohe.fit(X_train, y_train)
rr_grid_ohe.fit(X_train, y_train)
rf_grid_ohe.fit(X_train, y_train)

# Word vectorized features

from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

parameters_rr = {'alpha':[10**-4, 10**-3, 0.01, 0.06, 0.1, 0.3, 0.5]}
parameters_rf = {'n_estimators':[25, 40, 55], 'max_depth':[10, 20, 30]}
parameters_lasso = {'alpha':[10**-4, 10**-3, 0.01, 0.06, 0.1, 0.3, 0.5]}

lasso = Lasso()
rr = Ridge()
rf = RandomForestRegressor()

rr_grid = GridSearchCV(rr, parameters_rr, scoring='neg_mean_absolute_error')
rf_grid = GridSearchCV(rf, parameters_rf, scoring='neg_mean_absolute_error')
lasso_grid = GridSearchCV(lasso, parameters_lasso, scoring='neg_mean_absolute_error')

rr_grid.fit(x_c2v_train, y_train_c2v)
rf_grid.fit(x_c2v_train, y_train_c2v)
lasso_grid.fit(x_c2v_train, y_train_c2v)

# Predictions for both methods

y_ohe_lasso_pred = lasso_grid_ohe.predict(X_test)
y_ohe_rr_pred = rr_grid_ohe.predict(X_test)
y_ohe_rf_pred = rf_grid_ohe.predict(X_test)


y_c2v_lasso_pred = lasso_grid.predict(x_c2v_test)
y_c2v_rr_pred = rr_grid.predict(x_c2v_test)
y_c2v_rf_pred = rf_grid.predict(x_c2v_test)

# Plotting and evaluating predictions- best model

trace_data_dist = go.Scatter(
        x = np.linspace(0, 100, 100),
        y = y_test[:200],
        text = 'True value', name = 'True values')

trace_data_pred = go.Scatter(
        x = np.linspace(0, 100, 100),
        y = y_ohe_rr_pred[:200],
        mode = 'lines',
        text='Prediction', name = 'Predictions')

data_dist = [trace_data_dist, trace_data_pred]

layout = go.Layout(
        title = "Evaluating predictions (first 100 samples)",
        xaxis = dict(title="Indices"),
        yaxis = dict(title="Processing time in days"))

fig = go.Figure(data = data_dist, layout = layout)
iplot(fig, filename = 'basic-line')

