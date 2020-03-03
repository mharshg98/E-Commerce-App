from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from math import ceil
import json
from . models import Contact,Orders,OrderUpdate
# Create your views here.

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('catagory', 'id')
    cats = {item['catagory'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(catagory=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)
    
def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        return render(request,'shop/contact_us.html')
    else:
        return render(request,'shop/contact_us.html')
def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].item_json] , default=str)
                return HttpResponse(response)
            else:
                return HttpResponse({})
        except Exception as e:
            return HttpResponse({})

    return render(request, 'shop/tracker.html')
    


def search(request):
    return render(request,'shop/search.html')

def productview(request,myid):
    #fetch the product using id
    product = Product.objects.filter(id=myid)
    return render(request,'shop/product_view.html',{'p':product[0]})

def checkout(request):
    if request.method=='POST':
        name=request.POST.get('name','')
        item_json=request.POST.get('item_json','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        address=request.POST.get('address1','')+' '+request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        order=Orders(name=name,email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code,item_json=item_json)
        order.save()
        thank = True
        id = order.order_id
        update=OrderUpdate(order_id=id,update_desc="The order has been placed")
        update.save()
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    else:
        return render(request,'shop/checkout.html')



