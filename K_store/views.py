



from django.shortcuts import render
from Goods.models import CompanyId


def main(request):
    iden = CompanyId.objects.all()
    contex = {
        'identity': iden
    }
    return render(request, 'index.html', contex)

def mainloop(request):
    iden = CompanyId.objects.all()
    contex = {
    'identity': iden
}
    return render(request, 'based.html', contex)
