from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .ml_model import load_model
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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


def classifier(request):
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
        # form = CSVUploadForm(request.POST, request.FILES)
        # if form.is_valid():
            # Get the uploaded CSV file
            csv_file = request.FILES['csv_file']

            # Read the CSV file into a Pandas DataFrame
            iris_data = pd.read_csv(csv_file)
            iris_data['Species'] = iris_data['Species'].map(label_mapping)
            numpy_iris_data = iris_data["Species"].to_numpy()

            test_iris_data = iris_data.drop("Species", axis=1)

            # Preprocess the data
            preprocessed_data = preprocess_data(test_iris_data)

            arr1 = [1,2,3,4,5]
            arr2 = [0,9,7,5.4]

            # Make predictions
            predictions = predict(preprocessed_data)

            print(list(predictions))
            reversed_dict = {value: key for key, value in label_mapping.items()}
            values_predictions = [reversed_dict[i] for i in list(predictions)]
            print(values_predictions)

            accuracy = np.mean(numpy_iris_data == predictions) * 100

            # Pass the predictions to the template

            return render(request, 'classification/results.html', {'values_predictions': values_predictions,
                                                                   'accuracy_score': accuracy})
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form})


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


def predict_csv(request):
    if request.method == 'POST':
        # form = CSVUploadForm(request.POST, request.FILES)
        # if form.is_valid():
        
            # Get the uploaded CSV file
        
        csv_file = request.FILES['csv_file']

        # Read the CSV file into a Pandas DataFrame
        iris_data = pd.read_csv(csv_file)
        predictions = []
        for index, row in iris_data.iterrows():
        # Extract the features from the row
            sepal_length = row['SepalLengthCm']
            sepal_width = row['SepalWidthCm']
            petal_length = row['PetalLengthCm']
            petal_width = row['PetalWidthCm']
            input_array = [sepal_length, sepal_width, petal_length, petal_width]
            prediction = int(predict_individually(input_array))
            reversed_dict = {value: key for key, value in label_mapping.items()}

            value = reversed_dict[prediction]
            predictions.append(value)
        iris_data['predicted']=predictions
        response=HttpResponse(content_type = 'text/csv')
        response['Content-Disposition']='attachment; filename="predictions.csv"'
        iris_data.to_csv(response, index=False)
        
        return response
    else:
        return render(request, 'upload.html')

def predict_pdf(request):
    if request.method == 'POST':
        # Get the uploaded CSV file
        csv_file = request.FILES['csv_file']

        # Read the CSV file into a Pandas DataFrame
        iris_data = pd.read_csv(csv_file)
        predictions = []
        for index, row in iris_data.iterrows():
            # Extract the features from the row
            sepal_length = row['SepalLengthCm']
            sepal_width = row['SepalWidthCm']
            petal_length = row['PetalLengthCm']
            petal_width = row['PetalWidthCm']
            input_array = [sepal_length, sepal_width, petal_length, petal_width]
            prediction = int(predict_individually(input_array))
            reversed_dict = {value: key for key, value in label_mapping.items()}
            value = reversed_dict[prediction]
            predictions.append(value)
        iris_data['predicted'] = predictions

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="predictions.pdf"'

        # Create a PDF document using ReportLab
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Split the DataFrame into smaller chunks for multiple pages
        chunk_size = 33  # You can adjust this value based on your needs
        for i in range(0, len(iris_data), chunk_size):
            chunk = iris_data.iloc[i:i + chunk_size]
            data = [list(chunk.columns)] + chunk.values.tolist()
            table = Table(data, colWidths=[80, 80, 80, 80, 80, 80])
            table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                       ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                       ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
            elements.append(table)

        doc.build(elements)
        return response
    else:
        return render(request, 'upload.html')

