from django.shortcuts import render

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
        