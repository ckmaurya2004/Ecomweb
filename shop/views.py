from django.shortcuts import render
from django.http import HttpResponse
from . models import Product,Contact,Order,OrderUpdates
from math import ceil
import json


# Create your views here.
def index(request):
    products = Product.objects.all()
   # n = len(products)
   # nslides = (n//4) + ceil((n/4) + (n//4))
    #param = {'no_of_slide':nslides,'range':range(1,nslides),'product':products}
    #allprods = [[products,range(1,nslides),nslides],[products,range(1,nslides),nslides]]
    allprods = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item  in catprods}
    for cat in cats:
        prods = Product.objects.filter(category = cat)
        n = len(prods)
        nslides = (n//4) + ceil((n/4) + (n//4))
        allprods.append([prods,range(1,nslides),nslides])
    param = {'allproduct':allprods}
    return render(request , 'shop/index.html', param)


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
    

def search(request):
    query = request.GET.get('search')
    products = Product.objects.all()
    allprods = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item  in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category = cat)
        prods = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prods)
        nslides = (n//4) + ceil((n/4) + (n//4))
        if len(prods) !=0:
            allprods.append([prods,range(1,nslides),nslides])
    param = {'allproduct':allprods,'msg ': "" }
    if len(allprods)==0 and len(query)<4:
        param = {'msg':"Please enter related search....."}
    return render(request , 'shop/search.html', param)


def about(request):
      return render(request , 'shop/about.html' )

def contact(request):
     #thanks = False
     if(request.method == 'POST' ):
          name = request.POST.get('name','')
          email = request.POST.get('email','')
          phone = request.POST.get('phone','')
          desc = request.POST.get('desc','')
          contact = Contact(name = name, email=email , phone = phone , desc = desc)
          contact.save()
          thanks = True
          return render(request, 'shop/contact.html',{'thanks': thanks}) 

     return render(request , 'shop/contact.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id = orderId,email = email)
            if len(order)>0:
                update = OrderUpdates.objects.filter(order_id = orderId)
                updates = []
                for item in update:
                    updates.append({'text' : item.update_desc,'time':item.timestemp})
                    response = json.dumps([updates,order[0].itemJson],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')

        except Exception as e :
            return HttpResponse('{}')


    return render(request, 'shop/tracker.html')
        
   
              

def productView(request,myid):
     products = Product.objects.filter(id = myid)
     param = {'product':products[0]}
     return render(request , 'shop/productview.html' ,param)


def checkout(request):
    if(request.method == 'POST' ):
        itemJson = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','')+" "+ request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        phone = request.POST.get('phone','')
        order = Order(name = name, email=email , address = address,city = city,state = state,phone =phone,itemJson = itemJson)
        order.save()
        update = OrderUpdates(order_id = order.order_id, update_desc = 'your order has been placed')
        update.save()
        thanks = True
        id = order.order_id
        return render(request, 'shop/checkout.html',{'thanks': thanks,'id':id}) 
        #Request paytem to transfer the amount to your account after payment by user
      
    return render(request ,'shop/checkout.html') 

