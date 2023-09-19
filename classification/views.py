from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .ml_model import predict


# from . import ml_model

# def predict_view(request):
#     if request.method == 'POST':
#         csv_file = request.FILES['csv_file']
#         df = pd.read_csv(csv_file)

#         # Make predictions using your machine learning model
#         predictions = ml_model.predict(df)

#         # Add predictions to the DataFrame
#         df['predicted_target'] = predictions

#         # Convert the DataFrame to CSV
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="predictions.csv"'
#         df.to_csv(response, index=False)

#         return response
#     else:
#         return render(request, 'upload.html')

# Create your views here.
def classiffier(request):
    if request.method == "POST":
        sepal_width = request.POST.get("sepal_width")
        sepal_lenght = request.POST.get("sepal_lenght")
        petal_width = request.POST.get("petal_width")
        petal_length = request.POST.get("petal_length")
        return render(request, "classiffier.html", {"sepal": "VIRGINICA"})
    else:
        return render(request, "classiffier.html")


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded CSV file
            csv_file = request.FILES['csv_file']
            input_data = parse_csv(csv_file)
            predictions = predict(input_data)
            return render(request, 'classification/results.html', {'predictions': predictions})
    else:
        form = CSVUploadForm()
    return render(request, 'classification/upload_csv.html', {'form': form})


def parse_csv(csv_file):
    # Implement CSV parsing logic to extract data as needed
    # You can use libraries like csv.reader
    # Example: Read data into a list of lists
    data = []
    for row in csv_file:
        row_data = row.decode('utf-8').split(',')
        data.append(row_data)
    return data
