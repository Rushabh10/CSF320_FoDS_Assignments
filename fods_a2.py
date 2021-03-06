# -*- coding: utf-8 -*-
"""FoDS A2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kbGRstaY7npjk-7EJdmOzww7NZw3h-gP

Importing the necessary libraries and loading the dataset
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy
import pandas as pd
import matplotlib.patches as mpatches

df = pd.read_csv('./insurance.txt', sep=",")
df = df.sample(frac = 1)
dummy = [1]*len(df)
norm_df=(df-df.mean())/df.std()
norm_df.head()
norm_df["bias"] = dummy
df_size = len(norm_df)

train_df = norm_df[0:int(df_size*0.7)]
test_df = norm_df[int(df_size*0.7):]

X_train = train_df.drop(columns = ["charges"])
X_test = test_df.drop(columns = ["charges"])

X_train = X_train.to_numpy()
X_test = X_test.to_numpy()

y_train = train_df.drop(columns = ["age", "bmi", "children", "bias"])
y_train = y_train.to_numpy()

y_test = test_df.drop(columns = ["age", "bmi", "children", "bias"])
y_test = y_test.to_numpy()

# NORMAL EQUATION

def normal_eqn(X, y):
  X_trans = np.transpose(X)
  temp1 = np.dot(X_trans, X)
  temp1 = np.linalg.inv(temp1)
  temp2 = np.dot(X_trans, y)
  res = np.dot(temp1, temp2)
  return res

theta = normal_eqn(X_train, y_train)

print("Theta with normal eqns = ", theta)

# 20 MODELS WITH DIFF TRAIN-TEST SPLIT

MSE_train_errors = []
MSE_test_errors = []
RMSE_train_errors = []
RMSE_test_errors = []
MAE_train_errors = []
MAE_test_errors = []

for i in range(20):
  norm_df = norm_df.sample(frac = 1) 
  train_df = norm_df[0:int(df_size*0.7)]
  test_df = norm_df[int(df_size*0.7):]

  X_train = train_df.drop(columns = ["charges"])
  X_test = test_df.drop(columns = ["charges"])

  X_train = X_train.to_numpy()
  X_test = X_test.to_numpy()

  y_train = train_df.drop(columns = ["age", "bmi", "children", "bias"])
  y_train = y_train.to_numpy()

  y_test = test_df.drop(columns = ["age", "bmi", "children", "bias"])
  y_test = y_test.to_numpy()

  theta = normal_eqn(X_train, y_train)
  y_predict_test = np.dot(X_test, theta)
  y_predict_train = np.dot(X_train, theta)

  MSE_test = np.mean(np.square(y_predict_test-y_test))
  MSE_train = np.mean(np.square(y_predict_train-y_train))
  MAE_test = np.mean(np.abs(y_predict_test-y_test))
  MAE_train = np.mean(np.abs(y_predict_train-y_train))
  RMSE_train = np.sqrt(MSE_train)
  RMSE_test = np.sqrt(MSE_test)

  MSE_train_errors.append(MSE_train)
  MSE_test_errors.append(MSE_test)
  RMSE_train_errors.append(RMSE_train)
  RMSE_test_errors.append(RMSE_test)
  MAE_train_errors.append(MAE_train)
  MAE_test_errors.append(MAE_test)

  print("Done with model ", i+1)

print("Error statistics: ")
print("MSE Train error: ")
print("Mean = ", np.mean(MSE_train_errors), " Variance = ", np.std(MSE_train_errors)**2, " Min = ", np.min(MSE_train_errors))
print("-----------------------------------------")
print("MSE Test error: ")
print("Mean = ", np.mean(MSE_test_errors), " Variance = ", np.std(MSE_test_errors)**2, " Min = ", np.min(MSE_test_errors))
print("-----------------------------------------")
print("RMSE Train error: ")
print("Mean = ", np.mean(RMSE_train_errors), " Variance = ", np.std(RMSE_train_errors)**2, " Min = ", np.min(RMSE_train_errors))
print("-----------------------------------------")
print("MSE Test error: ")
print("Mean = ", np.mean(RMSE_test_errors), " Variance = ", np.std(RMSE_test_errors)**2, " Min = ", np.min(RMSE_test_errors))
print("-----------------------------------------")
print("MAE Train error: ")
print("Mean = ", np.mean(MAE_train_errors), " Variance = ", np.std(MAE_train_errors)**2, " Min = ", np.min(MAE_train_errors))
print("-----------------------------------------")
print("MAE Test error: ")
print("Mean = ", np.mean(MAE_test_errors), " Variance = ", np.std(MAE_test_errors)**2, " Min = ", np.min(MAE_test_errors))
print("-----------------------------------------")

# GRADIENT DESCENT

def init_params(lenw):
  w = np.random.rand(1, lenw)
  b = 0
  return w, b

def predict(X, w, b):
  z = np.dot(w, X)+b
  return z

def cost_function(z, y):
  m = y.shape[1]
  J = (1/(2*m))*np.sum(np.square(z-y))
  return J

def get_grads(X, y, z):
  m = y.shape[1]
  # print("m val = ", m)
  # print("y shape = ", y.shape)
  # print("z shape = ", z.shape)
  dz = (1/m)*(z-y)
  dw = np.dot(dz, X.T)
  db = np.sum(dz)
  return dw, db

def update_params(w, b, dw, db, lr):
  w = w-lr*dw
  b = b-lr*db
  return w, b

def linear_regression(X_train, y_train, X_test, y_test, lr, epochs):
  lenw = X_train.shape[0]
  w, b = init_params(lenw)
  costs_list = []
  final_errors = {"MSE_test": 0, "MSE_train": 0, "RMSE_test": 0, "RMSE_train": 0, "MAE_test": 0, "MAE_train": 0}

  for i in range(1, epochs+1):
    z_train = predict(X_train, w, b)
    cost_train = cost_function(z_train, y_train)
    dw, db = get_grads(X_train, y_train, z_train)
    w, b = update_params(w, b, dw, db, lr)

    if i%10 == 0:
      costs_list.append(cost_train)

    MSE_train = np.mean(np.square(z_train-y_train))
    RMSE_train = np.sqrt(MSE_train)
    MAE_train = np.mean(np.abs(z_train-y_train))

    z_test = predict(X_test, w, b)
    cost_test = cost_function(z_test, y_test)
    MSE_test = np.mean(np.square(z_test-y_test))
    RMSE_test = np.sqrt(MSE_test)
    MAE_test = np.mean(np.abs(z_test-y_test))

    print("Epoch: " + str(i) + " --> " + "Train cost = " + str(cost_train) + " | Test cost = " + str(cost_test))

    if(i == epochs):
      final_errors["MSE_test"] += MSE_test
      final_errors["MSE_train"] += MSE_train
      final_errors["RMSE_test"] += RMSE_test
      final_errors["RMSE_train"] += RMSE_train
      final_errors["MAE_train"] += MAE_train
      final_errors["MAE_test"] += MAE_test
  # plt.plot(costs_list)
  # plt.xlabel("cost per 10 iters")
  # plt.ylabel("Training cost")
  # plt.title("Learning rate = " + str(lr))
  # plt.show()
  return w, b, costs_list, final_errors

X_train = train_df.drop(columns = ["charges", "bias"])
X_test = test_df.drop(columns = ["charges", "bias"])

X_train = X_train.to_numpy()
X_test = X_test.to_numpy()

y_train = train_df.drop(columns = ["age", "bmi", "children", "bias"])
y_train = y_train.to_numpy()

y_test = test_df.drop(columns = ["age", "bmi", "children", "bias"])
y_test = y_test.to_numpy()

X_train = X_train.T
X_test = X_test.T

y_train = y_train.T
y_test = y_test.T

w1, b1, cost_list1, final_errors1 = linear_regression(X_train, y_train, X_test, y_test, 0.1, 4500)
w2, b2, cost_list2, final_errors2 = linear_regression(X_train, y_train, X_test, y_test, 0.01, 4500)
w3, b3, cost_list3, final_errors3 = linear_regression(X_train, y_train, X_test, y_test, 0.001, 4500)

plt.figure(figsize=(20, 10))
plt.plot(cost_list1, color="red")
plt.plot(cost_list2, color="blue")
plt.plot(cost_list3, color="green")
red_patch = mpatches.Patch(color='red', label='lr = 0.1')
blue_patch = mpatches.Patch(color='blue', label='lr = 0.01')
green_patch = mpatches.Patch(color='green', label='lr = 0.001')
plt.legend(handles = [red_patch, blue_patch, green_patch])
plt.xlabel("cost per 10 iters")
plt.ylabel("Training cost")
plt.ylim((0.4,0.6))
plt.title("Cost vs iterations for different learning rates")
plt.show()

print("weights and bias from GD: w = ", w2, " b = ", b2)

# 20 GD MODELS

errors = []

for i in range(20):
  norm_df = norm_df.sample(frac = 1) 
  train_df = norm_df[0:int(df_size*0.7)]
  test_df = norm_df[int(df_size*0.7):]

  X_train = train_df.drop(columns = ["charges", "bias"])
  X_test = test_df.drop(columns = ["charges", "bias"])

  X_train = X_train.to_numpy()
  X_test = X_test.to_numpy()

  y_train = train_df.drop(columns = ["age", "bmi", "children", "bias"])
  y_train = y_train.to_numpy()

  y_test = test_df.drop(columns = ["age", "bmi", "children", "bias"])
  y_test = y_test.to_numpy()

  X_train = X_train.T
  X_test = X_test.T

  y_train = y_train.T
  y_test = y_test.T

  w, b, cost_list, final_errors = linear_regression(X_train, y_train, X_test, y_test, 0.001, 6000)

  errors.append(final_errors)

MSE_train_errors = []
MSE_test_errors = []
RMSE_train_errors = []
RMSE_test_errors = []
MAE_train_errors = []
MAE_test_errors = []
for i in range(20):
  MSE_train_errors.append(errors[i]["MSE_train"])
  MSE_test_errors.append(errors[i]["MSE_test"])
  RMSE_train_errors.append(errors[i]["RMSE_train"])
  RMSE_test_errors.append(errors[i]["RMSE_test"])
  MAE_train_errors.append(errors[i]["MAE_train"])
  MAE_test_errors.append(errors[i]["MAE_test"])

print("Error statistics: ")
print("MSE Train error: ")
print("Mean = ", np.mean(MSE_train_errors), " Variance = ", np.std(MSE_train_errors)**2, " Min = ", np.min(MSE_train_errors))
print("-----------------------------------------")
print("MSE Test error: ")
print("Mean = ", np.mean(MSE_test_errors), " Variance = ", np.std(MSE_test_errors)**2, " Min = ", np.min(MSE_test_errors))
print("-----------------------------------------")
print("RMSE Train error: ")
print("Mean = ", np.mean(RMSE_train_errors), " Variance = ", np.std(RMSE_train_errors)**2, " Min = ", np.min(RMSE_train_errors))
print("-----------------------------------------")
print("MSE Test error: ")
print("Mean = ", np.mean(RMSE_test_errors), " Variance = ", np.std(RMSE_test_errors)**2, " Min = ", np.min(RMSE_test_errors))
print("-----------------------------------------")
print("MAE Train error: ")
print("Mean = ", np.mean(MAE_train_errors), " Variance = ", np.std(MAE_train_errors)**2, " Min = ", np.min(MAE_train_errors))
print("-----------------------------------------")
print("MAE Test error: ")
print("Mean = ", np.mean(MAE_test_errors), " Variance = ", np.std(MAE_test_errors)**2, " Min = ", np.min(MAE_test_errors))
print("-----------------------------------------")

# STOCHASTIC GRADIENT DESCENT

def batch_gd(X_train, y_train, X_test, y_test, lr, epochs, batch_size):
  lenw = X_train.shape[0]
  w, b = init_params(lenw)
  costs_list = []
  final_errors = {"MSE_test": 0, "MSE_train": 0, "RMSE_test": 0, "RMSE_train": 0, "MAE_test": 0, "MAE_train": 0}
  count = 0

  for i in range(1, epochs+1):
    start = 0
    while(start+batch_size < df_size*0.7):
      temp_x_train = X_train[:,start:start+batch_size]
      temp_x_test = X_test[:,start:start+batch_size]
      temp_y_train = y_train[:,start:start+batch_size]
      temp_y_test = y_test[:,start:start+batch_size]

      temp_z_train = predict(temp_x_train, w, b)
      z_train = predict(X_train, w, b)
      cost_train = cost_function(z_train, y_train)
      dw, db = get_grads(temp_x_train, temp_y_train, temp_z_train)
      #print("GRAD SHAPES = ", dw.shape, " ", db.shape)
      w, b = update_params(w, b, dw, db, lr)

      #print("W SHAPE NOW = ", w.shape)
      if(count%200 == 0):
        costs_list.append(cost_train)


      MSE_train = np.mean(np.square(z_train-y_train))
      RMSE_train = np.sqrt(MSE_train)
      MAE_train = np.mean(np.abs(z_train-y_train))

      z_test = predict(X_test, w, b)
      cost_test = cost_function(z_test, y_test)
      MSE_test = np.mean(np.square(z_test-y_test))
      RMSE_test = np.sqrt(MSE_test)
      MAE_test = np.mean(np.abs(z_test-y_test))


      print("Epoch: " + str(i) + " --> " + "Train cost = " + str(cost_train) + " | Test cost = " + str(cost_test))
      count += 1

      start += batch_size

    if(i == epochs):
      final_errors["MSE_test"] += MSE_test
      final_errors["MSE_train"] += MSE_train
      final_errors["RMSE_test"] += RMSE_test
      final_errors["RMSE_train"] += RMSE_train
      final_errors["MAE_train"] += MAE_train
      final_errors["MAE_test"] += MAE_test
  # plt.plot(costs_list)
  # plt.xlabel("cost per 10 iters")
  # plt.ylabel("Training cost")
  # plt.title("Learning rate = " + str(lr))
  # plt.show()
  return w, b, costs_list, final_errors

w1, b1, cost_list1, final_errors1 = batch_gd(X_train, y_train, X_test, y_test, 0.001, 50, 1)
w2, b2, cost_list2, final_errors2 = batch_gd(X_train, y_train, X_test, y_test, 0.01, 50, 1)
w3, b3, cost_list3, final_errors3 = batch_gd(X_train, y_train, X_test, y_test, 0.1, 50, 1)

plt.figure(figsize=(20, 10))
plt.plot(cost_list1, color="red")
plt.plot(cost_list2, color="blue")
plt.plot(cost_list3, color="green")
red_patch = mpatches.Patch(color='red', label='lr = 0.001')
blue_patch = mpatches.Patch(color='blue', label='lr = 0.01')
green_patch = mpatches.Patch(color='green', label='lr = 0.1')
plt.legend(handles = [red_patch, blue_patch, green_patch])

plt.xlabel("cost")
plt.ylabel("Training cost")
plt.title("Cost vs iterations for different learning rates")
plt.show()

print("weights and bias from GD: w = ", w2, " b = ", b2)

# 20 SGD MODELS

errors = []
for i in range(20):
  norm_df = norm_df.sample(frac = 1) 
  train_df = norm_df[0:int(df_size*0.7)]
  test_df = norm_df[int(df_size*0.7):]

  X_train = train_df.drop(columns = ["charges", "bias"])
  X_test = test_df.drop(columns = ["charges", "bias"])

  X_train = X_train.to_numpy()
  X_test = X_test.to_numpy()

  y_train = train_df.drop(columns = ["age", "bmi", "children", "bias"])
  y_train = y_train.to_numpy()

  y_test = test_df.drop(columns = ["age", "bmi", "children", "bias"])
  y_test = y_test.to_numpy()

  X_train = X_train.T
  X_test = X_test.T

  y_train = y_train.T
  y_test = y_test.T

  w, b, cost_list, final_errors1 = batch_gd(X_train, y_train, X_test, y_test, 0.001, 100, 1)

  errors.append(final_errors)


MSE_train_errors = []
MSE_test_errors = []
RMSE_train_errors = []
RMSE_test_errors = []
MAE_train_errors = []
MAE_test_errors = []
for i in range(20):
  MSE_train_errors.append(errors[i]["MSE_train"])
  MSE_test_errors.append(errors[i]["MSE_test"])
  RMSE_train_errors.append(errors[i]["RMSE_train"])
  RMSE_test_errors.append(errors[i]["RMSE_test"])
  MAE_train_errors.append(errors[i]["MAE_train"])
  MAE_test_errors.append(errors[i]["MAE_test"])

print("Error statistics: ")
print("MSE Train error: ")
print("Mean = ", np.mean(MSE_train_errors), " Variance = ", np.std(MSE_train_errors)**2, " Min = ", np.min(MSE_train_errors))
print("-----------------------------------------")
print("MSE Test error: ")
print("Mean = ", np.mean(MSE_test_errors), " Variance = ", np.std(MSE_test_errors)**2, " Min = ", np.min(MSE_test_errors))
print("-----------------------------------------")
print("RMSE Train error: ")
print("Mean = ", np.mean(RMSE_train_errors), " Variance = ", np.std(RMSE_train_errors)**2, " Min = ", np.min(RMSE_train_errors))
print("-----------------------------------------")
print("MSE Test error: ")
print("Mean = ", np.mean(RMSE_test_errors), " Variance = ", np.std(RMSE_test_errors)**2, " Min = ", np.min(RMSE_test_errors))
print("-----------------------------------------")
print("MAE Train error: ")
print("Mean = ", np.mean(MAE_train_errors), " Variance = ", np.std(MAE_train_errors)**2, " Min = ", np.min(MAE_train_errors))
print("-----------------------------------------")
print("MAE Test error: ")
print("Mean = ", np.mean(MAE_test_errors), " Variance = ", np.std(MAE_test_errors)**2, " Min = ", np.min(MAE_test_errors))
print("-----------------------------------------")

