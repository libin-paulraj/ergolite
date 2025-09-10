from django.shortcuts import redirect, render,redirect
from .models import Chairs,Usermodel, CartModel
from itertools import zip_longest
from decimal import Decimal
from django.views.decorators.http import require_POST


def home_view(request):
    chairs_model = Chairs.objects.filter( category="Most populer")[:20]
    chair_pairs = list(zip_longest(*[iter(chairs_model)]*2)) # [(p1, p2), (p3, p4), ...]

    chair_top = Chairs.objects.filter(category="HOMETOP")[:6]

    chair_bottom = Chairs.objects.filter(category="HOMEBOTTOM")[:3]
    
   

    return render(request, "index.html", {"chairs":chair_pairs, "chair_top":chair_top, "chair_bottom":chair_bottom, } )

def category_view(request):

    chair_category = Chairs.objects.filter(category="OFFICECHAIRS")[:12]

    interior = Chairs.objects.filter(category="INTERIOR")[:6]

    return render(request, "category.html",{"chair_category": chair_category, "interior":interior,})


def products_view(request):

    director_chair = Chairs.objects.filter(category="DIRECTORCHAIR")

    Premium_chair = Chairs.objects.filter(category="PREMIUM")

    Workforce_chair = Chairs.objects.filter(category="WORKFORCE") 

    Lounge_chair = Chairs.objects.filter(category="LOUNGE") 

    Visitor_chair = Chairs.objects.filter(category="VISITOR") 

    Cafeteria_chair = Chairs.objects.filter(category="CAFETERIA") 
    
    return render(request, "products.html",{"director_chair":director_chair,"Premium_chair":Premium_chair,
                                            "Workforce_chair": Workforce_chair,"Lounge_chair": Lounge_chair,
                                            "Visitor_chair":Visitor_chair,"Cafeteria_chair":Cafeteria_chair})



def contact_view(request):
    return render(request, "contact.html")


def product_details(request, id):
    chair = Chairs.objects.get(id=id)
    return render(request, "productsdetails.html", {"chair": chair})

def login_view(request):
    
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=Usermodel.objects.filter(username=username,password=password).first()

        if user is not None:
            request.session["user"] = user.id 
            return redirect("home:home")
        
    return render(request,"login.html")

def register_view(request):
    # print("____________________________")
    # print(request.GET.get("username"))
    
    if request.method=="POST":
        # print(request.POST.get("username"))
        username=request.POST.get("username")
        password=request.POST.get("password")
        phonenumber=request.POST.get("phonenumber")
        confirmpassword=request.POST.get("confirmpassword")

        if password.strip() == confirmpassword.strip():
            user=Usermodel.objects.create(username=username,password=password,phonenumber=phonenumber)
            return redirect("home:login")

    return render(request,"register.html")

def add_cart_view(request):
    user = request.session.get("user")

    if request.method == "POST":

        if user is None:
            return redirect("home:login")

        id = request.POST.get("cart_product")
        quantity = request.POST.get("quantity")
        
        chair = Chairs.objects.get(id=id)
        user = Usermodel.objects.get(id=user)
        CartModel.objects.create(user=user, cart=chair, quantity=quantity)

        return redirect("home:cart")
    return render(request,"productsdetails.html")

def cart_view(request, *args, **kwargs):
    user = request.session["user"]

    if user is None:
        return redirect("home:login")

    cart = CartModel.objects.filter(user=user)

    print(cart)

    total_price = 0
    for item in cart:
        total_price += item.cart.price * item.quantity

    return render(request, "cart.html", {"cart":cart,  "total_price": total_price,})



def logout_view(request):
    request.session["user"] = None
    return redirect("home:login")

@require_POST
def remove_from_cart(request, cart_id):
    cart_item = CartModel.objects.filter(id=cart_id).first()
    if cart_item:
        cart_item.delete()
    return redirect('home:cart')

def checkout(request):
    user_id = request.session.get("user")  

    if not user_id:
        return redirect("home:login")

    user = Usermodel.objects.get(id=user_id)

    cart_qs = CartModel.objects.filter(user=user)
    cart_items = []
    subtotal = Decimal("0.00")

    for cart_item in cart_qs:
        product = cart_item.cart  
        quantity = cart_item.quantity
        item_total = Decimal(product.price) * quantity
        subtotal += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': item_total
        })

    gst_rate = Decimal('0.18') 
    gst_amount = subtotal * gst_rate
    grand_total = subtotal + gst_amount

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'gst_amount': gst_amount,
        'grand_total': grand_total
    })
