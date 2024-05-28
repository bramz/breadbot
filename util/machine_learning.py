from typing import Any, Tuple, Dict
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error
import pandas as pd

class MachineLearning:
    """
    A utility class for machine learning tasks.

    This class provides methods for loading data, preprocessing data,
    choosing machine learning algorithms, training models, making predictions,
    evaluating model performance, hyperparameter tuning, feature scaling,
    and cross-validation.

    Attributes:
        None
    """

    def __init__(self) -> None:
        pass

    def load_data(self, path: str) -> Any:
        """
        Load data from a CSV file or database.

        Args:
            path (str): Path to the data file or database.

        Returns:
            Any: Loaded data.
        """
        data = pd.read_csv(path)  # Assuming data is in CSV format
        return data

    def preprocess_data(self, data: Any) -> Any:
        """
        Preprocess the loaded data.

        Args:
            data (Any): The loaded data.

        Returns:
            Any: Preprocessed data.
        """
        preprocessed_data = data.dropna()  # Example: dropping rows with missing values
        return preprocessed_data

    def split_data(self, data: Any, test_size: float = 0.2, random_state: int = 42) -> Tuple:
        """
        Split data into training and testing sets.

        Args:
            data (Any): The preprocessed data.
            test_size (float): The proportion of the dataset to include in the test split.
            random_state (int): Controls the shuffling applied to the data before applying the split.

        Returns:
            Tuple: Training and testing data split into features and target.
        """
        X = data.drop(columns=['target_column'])
        y = data['target_column']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return X_train, X_test, y_train, y_test

    def choose_algorithm(self, algorithm: str) -> Any:
        """
        Choose a machine learning algorithm.

        Args:
            algorithm (str): The name of the algorithm to choose.

        Returns:
            Any: The chosen machine learning algorithm.
        """
        algorithms = {
            'random_forest': RandomForestClassifier(),
            'svm': SVC(),
            'logistic_regression': LogisticRegression(),
            'knn': KNeighborsClassifier(),
            'decision_tree': DecisionTreeClassifier(),
            'naive_bayes': GaussianNB()
        }
        if algorithm not in algorithms:
            raise ValueError("Invalid algorithm specified.")
        return algorithms[algorithm]

    def train_model(self, model: Any, X_train: Any, y_train: Any) -> Any:
        """
        Train the machine learning model.

        Args:
            model (Any): The machine learning model to train.
            X_train (Any): The training data features.
            y_train (Any): The training data target.

        Returns:
            Any: The trained machine learning model.
        """
        trained_model = model.fit(X_train, y_train)
        return trained_model

    def make_predictions(self, model: Any, X_test: Any) -> Any:
        """
        Make predictions using the trained model.

        Args:
            model (Any): The trained machine learning model.
            X_test (Any): The test data features.

        Returns:
            Any: The predictions made by the model.
        """
        predictions = model.predict(X_test)
        return predictions

    def evaluate_model(self, y_true: Any, y_pred: Any) -> float:
        """
        Evaluate the model's performance.

        Args:
            y_true (Any): The true target values.
            y_pred (Any): The predicted target values.

        Returns:
            float: The accuracy of the model.
        """
        accuracy = accuracy_score(y_true, y_pred)
        return accuracy

    def hyperparameter_tuning(self, model: Any, param_grid: Dict, X_train: Any, y_train: Any) -> Any:
        """
        Perform hyperparameter tuning using GridSearchCV.

        Args:
            model (Any): The machine learning model to tune.
            param_grid (dict): The parameter grid to search over.
            X_train (Any): The training data features.
            y_train (Any): The training data target.

        Returns:
            Any: The optimized machine learning model.
        """
        grid_search = GridSearchCV(model, param_grid, cv=5)
        optimized_model = grid_search.fit(X_train, y_train)
        return optimized_model

    def feature_scaling(self, X_train: Any, X_test: Any) -> Tuple:
        """
        Perform feature scaling on the data.

        Args:
            X_train (Any): The training data features.
            X_test (Any): The test data features.

        Returns:
            Tuple: The scaled training and test data features.
        """
        scaler = StandardScaler()
        scaled_X_train = scaler.fit_transform(X_train)
        scaled_X_test = scaler.transform(X_test)
        return scaled_X_train, scaled_X_test

    def cross_validation(self, model: Any, X_train: Any, y_train: Any, cv: int = 5) -> Tuple:
        """
        Perform cross-validation to evaluate model performance.

        Args:
            model (Any): The machine learning model to evaluate.
            X_train (Any): The training data features.
            y_train (Any): The training data target.
            cv (int): The number of folds in cross-validation.

        Returns:
            Tuple: The mean and standard deviation of the cross-validation scores.
        """
        scores = cross_val_score(model, X_train, y_train, cv=cv)
        return scores.mean(), scores.std()

