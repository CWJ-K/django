from django.shortcuts import render
from .forms import ExampleForm, OrderForm


# Create your views here.
def form_example_old(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)

        if form.is_valid():
            for name, value in form.cleaned_data.items():
                print('{}: ({}) {}'.format(name, type(value), value))

    else:
        form = ExampleForm()
    return render(request, 'form-example.html', {'method': request.method, 'form': form})


def form_example(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            for name, value in form.cleaned_data.items():
                print('{}: ({}) {}'.format(name, type(value), value))
    else:
        form = OrderForm()
    return render(request, 'form-example.html', {'method': request.method, 'form': form})
