from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .ml_model import load_model

import numpy as np
import pandas as pd

# Global Variables
label_mapping = {
                'Iris-setosa': 0,
                'Iris-versicolor': 1,
                'Iris-virginica': 2
            }


def predict_individually(input_list):
    predicted_outcome = load_model().predict([input_list])
    return predicted_outcome


def classiffier(request):
    if request.method == "POST":
        sepal_width = float(request.POST.get("sepal_width"))
        sepal_length = float(request.POST.get("sepal_length"))
        petal_width = float(request.POST.get("petal_width"))
        petal_length = float(request.POST.get("petal_length"))

        input_array = [sepal_length, sepal_width, petal_length, petal_width]
        answer = int(predict_individually(input_array))
        reversed_dict = {value: key for key, value in label_mapping.items()}

        print(reversed_dict[answer])

        return render(request, "classiffier.html", {"sepal": reversed_dict[answer]})
    else:
        return render(request, "classiffier.html")


def preprocess_data(df):
    # Map the label column to numeric values (assuming 'Species' is the label column)
    # label_mapping = {
    #     'Iris-setosa': 0,
    #     'Iris-versicolor': 1,
    #     'Iris-virginica': 2
    # }
    # df['Species'] = df['Species'].map(label_mapping)
    # # Add any other data preprocessing steps here if needed
    # print(df)
    return df


def predict(input_data):
    # Use the loaded model to make predictions
    predictions = load_model().predict(input_data)
    return predictions


# def calculate_accuracy(actual_array, predicted_array):
#     if
#     pass


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded CSV file
            csv_file = request.FILES['csv_file']

            # Read the CSV file into a Pandas DataFrame
            iris_data = pd.read_csv(csv_file)
            iris_data['Species'] = iris_data['Species'].map(label_mapping)
            numpy_iris_data = iris_data["Species"].to_numpy()

            test_iris_data = iris_data.drop("Species", axis=1)

            # Preprocess the data
            preprocessed_data = preprocess_data(test_iris_data)

            # Make predictions
            predictions = predict(preprocessed_data)

            accuracy = np.mean(numpy_iris_data == predictions) * 100

            # Pass the predictions to the template
            return render(request, 'classification/results.html', {'predictions': predictions,
                                                                   'accuracy_score': accuracy})
    else:
        form = CSVUploadForm()
    return render(request, 'classification/upload_csv.html', {'form': form})
