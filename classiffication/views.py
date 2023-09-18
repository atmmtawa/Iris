from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from . import ml_model

def predict_view(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        df = pd.read_csv(csv_file)
        
        # Make predictions using your machine learning model
        predictions = ml_model.predict(df)

        # Add predictions to the DataFrame
        df['predicted_target'] = predictions

        # Convert the DataFrame to CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="predictions.csv"'
        df.to_csv(response, index=False)

        return response
    else:
        return render(request, 'upload.html')

# Create your views here.
def classiffier(request):
    if request.method=="POST":
        sepal_width = request.POST.get("sepal_width")
        sepal_lenght = request.POST.get("sepal_lenght")
        petal_width = request.POST.get("petal_width")
        petal_length = request.POST.get("petal_length")
        return render(request, "classiffier.html", {"sepal":"VIRGINICA"})
    else:
        return render(request, "classiffier.html")
        