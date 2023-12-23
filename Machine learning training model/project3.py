import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


class Model:

    def __init__(self, file):

        """
        In this function, we are passing the file and calling other functions in this class.
        we use self.features to call instances of the CSV file
        """

        self.file = file
        self.df = self.load_training_df()
        self.features = self.df[
            ['LotFrontage', 'LotArea', 'OverallQual', 'OverallCond', 'YearBuilt', 'BsmtFinSF1', 'BsmtUnfSF',
             'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea',
             'BsmtFullBath', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr',
             'TotRmsAbvGrd', 'Fireplaces', 'GarageCars', 'GarageArea', 'WoodDeckSF',
             'OpenPorchSF', 'EnclosedPorch', 'MoSold', 'Price']]

        self.weights = np.random.uniform(low=0, high=1, size=26)
        self.prediction = self.pred()

    def load_training_df(self):

        """
        the path of the file is passed through this function and is used to open and read the CSV files
        """

        return pd.read_csv(self.file)  # Import the dataset.

    def size(self):

        """
        Returns the number of records this file contains
        """
        size = self.df.size
        return 'The dataframe %s has %s entries' % (self.file, size)

    def mean_price(self):

        """
        this function returns the mean value
        """

        price = self.df['Price']
        mean = price.mean()
        return 'The mean of all prices is %s' % (mean)

    def min_and_max_price(self):

        """
        Returns the calculated maximum and minimum value of the price.
        """

        min_price = self.df['Price'].min()
        max_price = self.df['Price'].max()
        return 'The maximum price and the minimum price is respectively %s , %s' % (max_price, min_price)

    def standard_deviation(self):

        """
        This function is implemented to calculate the standard deviation of the price.
        """

        std_dev_price = self.df['Price'].std()
        return 'The standard deviation is %s' % (std_dev_price)

    def hist_price(self):

        """
        This function plots the histogram of Prices.
        """

        plt.figure(figsize=(10, 6))
        plt.hist(self.df['Price'], bins=30, color='red')
        plt.title('Histogram of Price')
        plt.xlabel('price')
        plt.ylabel('frequency')
        plt.show()

    def pair_wise_scatter_plot(self):

        """
        this function plots a pair wise scatter plot of different columns using GrLivArea, BedroomAbvGr,
        TotalBsmtSF, FullBath for the plots.
        """

        plot = sns.pairplot(data=self.df,
                            vars=['GrLivArea', 'BedroomAbvGr', 'TotalBsmtSF', 'FullBath'],
                            kind='scatter', diag_kind='auto')

        plt.show()

    def pred(self):

        """
        this function is used to calculate the predicted price. this does so by multiplying the feature matrix with weights.
        """

        prediction = self.features.multiply(self.weights).sum(axis=1)
        return prediction

    def loss(self):

        """
        this function calculates the loss based on a set of predicted sale price and the correct sale price.
        """

        prediction = self.pred()
        loss = (prediction - self.df['Price']).pow(2).multiply(1 / self.df['Price'].size)
        return loss

    def gradient(self):

        '''
        calculates the gradient of loss function based on the predicted price and the correct price.
        '''

        prediction = self.pred()
        Y_y = (prediction - self.df['Price'])
        feature_vector_transposed = self.features.T
        gradient = feature_vector_transposed.multiply(Y_y).multiply(2 / self.df['Price'].size).sum(axis=1)

        return gradient.T.to_list()

    def update(self, alpha):

        '''updates the weights based on the gradient using the specified learning rate (alpha)'''

        gradient = self.gradient()

        for i in range(len(self.weights)):  # Iterate over the indices and values of self.weights and gradient
            # Update each weight using the corresponding gradient value
            self.weights[i] = self.weights[i] - (alpha * gradient[i])


        return self.weights

    def TrainModel(self, alpha, num_iterations=500):

        """
        This function is used to train a model with specified learning rate and number of iterations
        Here first alpha (learning rate) is passed. Then we calculate the current_loss.
        """

        mse = []
        for _ in range(num_iterations):
            self.update(alpha)
            current_loss = self.loss().sum()  # calculating the total loss
            mse.append(current_loss)
            # adding a stop condition for when sum of loss is less than 0.1
            if current_loss < 0.1:
                print("Stopping training. Loss is below threshold.")
                break

        return mse


x = rf"C:\Users\gaura\OneDrive\Desktop\project3 241\train.csv" # file path

model1 = Model(x)
model2 = Model(x)
model3 = Model(x)

'''INITIALIZING'''
size = model1.size()
mean_price = model1.mean_price()
min_and_max_price = model1.min_and_max_price()
stddev = model1.standard_deviation()
hist_price = model1.hist_price()
scatter_plot = model1.pair_wise_scatter_plot()

update = model1.TrainModel(0.2)
iteration_update = range(len(update))
plt.plot(iteration_update, update, label='0.2')
print('Final MSE is ', sum(update))
plt.show()

'''PRINTING THE REQUIRED VALUES'''

print('The number of records in training set', size)  # printing the number of records
print(mean_price)  # printing the mean price
print(min_and_max_price)  # printing minimum and maximum price
print(stddev)  # printing standard deviation

run1 = model2.TrainModel(10 ** -8.5)
run2 = model3.TrainModel(10 ** -9)

sum_1 = model2.loss().sum()
sum_2 = model3.loss().sum()

iteration_1 = range(len(run1))
iteration_2 = range(len(run2))

#plotting functions
plt.plot(iteration_1, run1, label=10 ** -8.5)
plt.plot(iteration_2, run2, label=10 ** -9)

print('The Final MSE is:', sum_1, sum_2)
plt.title(label='ECE 241')
plt.legend()
plt.show()
