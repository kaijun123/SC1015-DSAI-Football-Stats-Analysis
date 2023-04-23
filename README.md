# SC1015 Data Science and Analytics Project - OPTIMU Analytics ⚽

![Cover](Assets/cover.png)
# Table of Contents 🛎️
- [SC1015 Data Science and Analytics Project - OPTIMU Analytics ⚽](#sc1015-data-science-and-analytics-project---optimu-analytics-)
- [Table of Contents 🛎️](#table-of-contents-️)
- [Repository Structure 🧬](#repository-structure-)
- [Video Presentation](#video-presentation)
- [Current Problems 🤔](#current-problems-)
    - [**1. Poor Business Management**](#1-poor-business-management)
    - [**2. Managerial Instability**](#2-managerial-instability)
    - [**3. Poor transfer policy**](#3-poor-transfer-policy)
- [Problem Statement 🚨](#problem-statement-)
- [Approach ⚙️](#approach-️)
- [Introduction to Codebase 🖥️](#introduction-to-codebase-️)
    - [Player\_Valuation](#player_valuation)
    - [Anomaly\_Detection](#anomaly_detection)
    - [Slides](#slides)
    - [Assets](#assets)
- [Contributors 👨‍💻](#contributors-)

# Repository Structure 🧬
```
|
├── README.md
├── Anomaly_Detection
│   ├── data
│   ├── fbref_data                      # Data from Fbref
│   ├── sofifa_data                     # Data from Sofifa
│   └── anomaly_detection.ipynb         # Notebook for anomaly detection
│
├── Player_Valuation
│   ├── Data                            # Data from Fbref and collated data from kaggle
│   └── player_valuation.ipynb          # Notebook for player valuation
│
└── Slides
└── Assets
```

# Video Presentation
- Our presentation video can be found on [Youtube](https://youtu.be/W5Y23JzVQP4)

# Current Problems 🤔
### **1. Poor Business Management**

Manchester United’s owners, the Glazers, have been accused of negligence and poor debt management.

### **2. Managerial Instability**
After the retirement of Sir Alex Ferguson in 2013, the club has gone through several managers who have struggled to replicate his success.

### **3. Poor transfer policy**
Over the past few years, Manchester United has been criticised for leaving deadwood in the team and paying excessively high transfer fees for players.

# Problem Statement 🚨

<blockquote align='center'> 
<h3>How can Manchester United better optimise its transfer strategy to improve the team's performance?</h3>
</blockquote>

# Approach ⚙️
We will be using a **2-pronged Data Science Oriented approach** to improve Manchester United's team performance.

1. Doing *anomaly detection* on their entire squad over the past season to determine underperforming players to sell


2. Doing *player valuation estimations* on potential transfer targets to avoid overpaying in the transfer market

The additonal revenue earned can then be used to improve club facilities or improve the quality of coaching/services provided to the players with the assumption that better facilites and coaching can improve a team's performance.

# Introduction to Codebase 🖥️

<div align='center'>
<img src="https://github-readme-tech-stack.vercel.app/api/cards?title=This%20Project's%20Tech%20Stack&align=center&titleAlign=center&lineCount=3&theme=github_dark&line1=python,python,auto;tensorflow,tensorflow,auto;&line2=pandas,pandas,auto;numpy,numpy,auto;scikitlearn,scikit%20learn,auto;&line3=git,git,auto;github,github,auto;jupyter,jupyter,auto;googlecolab,colab,auto;" alt="My Tech Stack" />
</div>

### Player_Valuation
- This segment contains code to predict a player's `Current Valuation`.
- Data used is obtained from scraping [FbRef](https://fbref.com/en/) and [kaggle](https://www.kaggle.com/datasets/davidcariboo/player-scores?select=player_valuations.csv)
- Data used include `Players' Stats`, such as height, age, etc, and `Players' Past Transaction Amount`.
- Models that were tested were Random Forest Regressor, Support Vector Regressor, Gradient Boosting and Artificial Neural Network
- Using these 2 collection of data, we trained each model to be able to predict a player's `Current Valuation`, based on the player's current stats.
- Calcuated evaluation matrix's for each model such as RMSE, MAE and R^2
- **Choice of Models:**
  - **Random Forest Regressor:** Builds multiple decisions trees and combines their predictions to make more accurate predictions. Useful when dealing with high-dimensional datasets and non-linear relationships between variables.
  - **Support Vector Regressor:** Finds a best-fit hyperplane that best represents the data points, with the goal of minimizing the error between the predicted and actual values. Useful when dealing with non-linear datasets
  - **XGBoost (Gradient Boosting):** Builds decision trees sequentially such that each new decision tree created corrects mistakes made by the previous. Capable of handling complex, nonlinear relationships between variables.
  - **Artificial Neural Network:** Makes use of multiple layers of neurons, with each neuron having an associated set of weights and biases. These weights and biases are updated for every batch of data fed in, via a technique known as backpropagation. 
- **Explanation for choice of models**:
  - Since our dataset comprises of many different factors with yet unknown relationship with the player's `Current Valuation`, we deliberately chose models that are capable of dealing with the large number of factors and non-linear relationships. This is in comparison to using models that assume linear relationships, such as Linear Regression.
  - In addition, the models were chosen as they function on different fundamental principles, to provide a range of different regressions paradigms. By using range of models, we hoped to be able to find the best performing one.

### Anomaly_Detection
- This segment contains code to identify the worst performing players within the team per season.
- Data used is obtained from scraping [FbRef]('https://fbref.com/en/') and [Sofifa](https://sofifa.com/)
- Using data from FbRef, we calculated the `Plus-Minus Per Min`. The formula is given as follows: 
`Plus-Minus Per Min = (Goals scored by own team - Goals scored by opponent team) / Playing Time per player`
- Using the data from Sofifa, we obtained the `Player Ratings`, `Player Rankings`.
- Using these 2 metrics, we trained our model using these 3 metrics: `Plus-Minus Per Min`, `Player Ratings` and `Player Rankings`, to identify the worst performing player in the team in a particular season.
- **Choice of Models:**
  - **Isolation Forrest:** Works by building a random forest of decision trees, where each tree isolates a small number of points from the rest of the data. Anomalies are identified as data points that require fewer partitions to be isolated.
  - **One Class Support Vector Machine:** Finds a hyperplane that encloses as many normal data points as possible while excluding the rest of the data points.
  During training, the model learns the parameters of the hyperplane using only normal data points. During testing, data points that fall outside the hyperplane are considered anomalous. Useful when dealing with high-dimensional data and when the anomalies are rare and difficult to detect using other methods.
  - **SGD One Class Support Vector Machine:** A variant of the One Class SVM algorithm that uses stochastic gradient descent for training. Stochastic gradient descent increases the efficiency and scalability of model training by updating the model parameters based on a small random subset of the data.
  - **Deep AutoEncoder:** A variant of the conventional ANN, which uses an encoder to reduce the the dimensionality of the data, and then reconstructs the 
  original input from the lower dimensional data via a decoder. The neural network will be trained on normal data. When applied on anomalous data, it will face difficulties trying to reconstruct these data, and these anomalies can thus be separated by their higher reconstruction error.
- **Explanation for choice of models**:
  - In our particular context, we are trying to identify isolated anomalies in the Manchester United players' performance. These models chosen are suitable for use in determining isolated anomalies.

**Choice of Metrics**
- **RMSE:** Root mean squared error (RMSE) is a commonly used metric to evaluate the performance of a regression model. It is calculated as the square root of the mean of the squared differences between predicted and true values of the target variable.Unlike some other metrics that only provide information about the direction of the errors (i.e., whether they are positive or negative), RMSE provides information about the magnitude of the errors. This can be useful in our application as we are looking at player valuation and thus need to know in greater detail about the error from the model rather than if it is just higher or lower than the true value
- **MAE** Mean Absolute Error (MAE) is a commonly used metric to evaluate the performance of regression models. It measures the average absolute difference between the predicted and actual values of the target variable. MAE treats all errors equally, regardless of their magnitude, which can make it more robust to outliers, making it useful failsafe in the case where we discover that we still have too many outliers in our dataset.
- **R^2** R-squared (R²) is a statistical metric that measures the proportion of variation in the target variable that is explained by the regression model. It is also known as the coefficient of determination. R² values range from 0 to 1, with a value of 1 indicating that the model explains all the variability in the target variable and a value of 0 indicating that the model explains none of the variability.R² is a good indicator for our project due to it being a bounded and standardized measure, which makes it easy to interpret as we can easily tell at first glance which model outperforms the other. If we were to instead compare between RMSE or MAE, the results could be in differing magnitudes and we would additionally have to look a the true market value for each player to determine the accuracy of the model. Thus R² can be used to compare the performance of different models and select the one that performs the best. 

### Slides
- This folder contains our slides for our project.

### Assets
- This folder contains miscellaneous assets for the project.

# Contributors 👨‍💻

|<a href="https://github.com/kaijun123"><div align='center'><kbd><img src="https://avatars.githubusercontent.com/u/96715775?v=4" height='80' /></kbd><br/>Ang Kai Jun</div></a>|<a href="https://github.com/chayhuixiang"><div align='center'><kbd><img src="https://avatars.githubusercontent.com/u/75465219?s=400&u=210359b21d09a29b6265e3c5fb004e148abbc055&v=4" height='80' /></kbd><br/>Chay Hui Xiang</div></a>|<a href="https://github.com/IvanLoke"><div align='center'><kbd><img src="https://avatars.githubusercontent.com/u/102502850?v=4" height='80' /></kbd><br/>Ivan Loke Zhi Hao</div></a>
|-----|-----|-----|
|<div align='center'>Data Scraping (Anomaly Detection), Gradient Boosting</div>|<div align='center'>Artificial Neural Network, Isolation Forest, One Class Support Vector Machine, SGD One Class Support Vector Machine, Deep AutoEncoder</div>|<div align='center'>Data Scraping (Player Valuation), Random Forest Regressor, Support Vector Regressor</div>
