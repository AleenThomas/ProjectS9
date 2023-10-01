from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import Customer_Profile
# from .forms import ProductForm
from .models import Product,CustomUser,SellerDetails,Wishlist,CartItem,Order
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from decimal import Decimal
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

# from .models import booknow, On_payment



def index(request):
    
    user=request.user
    if user.is_anonymous:
        return render(request,'index.html')
    elif user.is_seller==True:
        return redirect('seller_index')
    else:
        
        return render(request,'index.html')
    # return render(request,'index.html')
    
def contact(request):
    return render(request,'contact.html')
def sellerindex(request):
    return render(request,'sellerindex.html')
# def reg_step(request):
#     return render(request,'reg_step.html')


def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.get_or_create(user=request.user)[0]
        wishlist_products = wishlist.products.all()
        return render(request, 'wishlist.html', {'wishlist_products': wishlist_products})
    else:
        return render(request, 'login_required.html')

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return JsonResponse({'message': 'Product added to wishlist'})

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.products.remove(product)
    success_message = f'{product.product_name} removed from your wishlist.'

    # You can pass the success_message to the template
    return redirect('wishlist')
def update_wishlist_quantity(request, product_id, new_quantity):
    try:
        new_quantity = int(new_quantity)
    except ValueError:
        return JsonResponse({'message': 'Invalid quantity'}, status=400)
    
    if new_quantity <= 0:
        return JsonResponse({'message': 'Quantity must be greater than zero'}, status=400)
    
    product = get_object_or_404(Product, pk=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    
    # Update the quantity of the product in the wishlist
    item = wishlist.wishlist_items.filter(product=product).first()
    if item:
        item.quantity = new_quantity
        item.save()
        return JsonResponse({'message': 'Quantity updated successfully'})
    else:
        return JsonResponse({'message': 'Product not found in wishlist'}, status=404)





def seller_reg_step(request):
    if request.method == 'POST':
        step = request.POST.get('step')

        print(step)
        # Check which step the form data is coming from
        if step == '1':
            print("one")
            # Step 1 Data
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            gstn = request.POST.get('gstn')

            # Check for existing user with the same email
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                # Create a new user and set the password
                user = CustomUser(name=name, email=email, gstn=gstn)
                user.password = make_password(password)  # Hash the password
                user.is_seller = True  # Mark as a seller
                user.save()

                # Store the user ID in the session for future steps
                request.session['user_id'] = user.id

                messages.success(request, "Step 1 completed successfully.")
                # Redirect to step 2 or confirmation page

        elif step == '2':
            print("two")
            # Step 2 Data
            user_id = request.session.get('user_id')
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                
                store_name = request.POST.get('store-name')
                phone_number = request.POST.get('phone-number')
                pincode = request.POST.get('pincode')
                pickup_address = request.POST.get('pickup-address')
                city = request.POST.get('city')
                state = request.POST.get('state')

                # Check if the user already has seller details
                seller_details, created = SellerDetails.objects.get_or_create(user=user)

                # Update the seller details
                seller_details.store_name = store_name
                seller_details.phone_number = phone_number
                seller_details.pincode = pincode
                seller_details.pickup_address = pickup_address
                seller_details.city = city
                seller_details.state = state
                seller_details.save()

                messages.success(request, "Step 2 completed successfully.")
                # Redirect to step 3 or confirmation page

        elif step == '3':
            print("three")
            # Step 3 Data
            user_id = request.session.get('user_id')
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                
                account_holder_name = request.POST.get('account-holder-name')
                account_number = request.POST.get('account-number')
                bank_name = request.POST.get('bank-name')
                branch = request.POST.get('branch')
                ifsc_code = request.POST.get('ifsc-code')

                # Check if the user already has seller details
                seller_details, created = SellerDetails.objects.get_or_create(user=user)

                # Update the seller details
                seller_details.account_holder_name = account_holder_name
                seller_details.account_number = account_number
                seller_details.bank_name = bank_name
                seller_details.branch = branch
                seller_details.ifsc_code = ifsc_code
                seller_details.save()

                messages.success(request, "Step 3 completed successfully.")
                # Redirect to confirmation page or other steps

    return render(request, 'seller_reg_step.html')





# Import the necessary models


# ...

# def seller_reg_step(request):
#     if request.method == 'POST':
#         step = request.POST.get('step')
        
#         if step == '1':
#             # Step 1 Data
#             name = request.POST.get('name')
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             gstn = request.POST.get('gstn')

#             if CustomUser.objects.filter(email=email).exists():
#                 messages.error(request, "Email already exists.")
#             else:
#                 user = CustomUser(name=name, email=email, gstn=gstn)
#                 user.password = make_password(password)
#                 user.is_seller = True
#                 user.save()

#                 request.session['user_id'] = user.id

#                 messages.success(request, "Step 1 completed successfully.")
#                 return redirect('reg_step')

#         elif step == '2':
#             # Step 2 Data
#             user_id = request.session.get('user_id')
#             if user_id:
#                 user = CustomUser.objects.get(id=user_id)
                
#                 store_name = request.POST.get('store-name')
#                 phone_number = request.POST.get('phone-number')
#                 pincode = request.POST.get('pincode')
#                 pickup_address = request.POST.get('pickup-address')
#                 city = request.POST.get('city')
#                 state = request.POST.get('state')

#                 seller_details = user.seller_details_user.all().first()

#                 if not seller_details:
#                     seller_details = SellerDetails(
#                         user=user,
#                         store_name=store_name,
#                         phone_number=phone_number,
#                         pincode=pincode,
#                         pickup_address=pickup_address,
#                         city=city,
#                         state=state
#                     )
#                     seller_details.save()
#                 else:
#                     seller_details.store_name = store_name
#                     seller_details.phone_number = phone_number
#                     seller_details.pincode = pincode
#                     seller_details.pickup_address = pickup_address
#                     seller_details.city = city
#                     seller_details.state = state
#                     seller_details.save()

#                 messages.success(request, "Step 2 completed successfully.")
#                 return redirect('reg_step')

#         elif step == '3':
#             # Step 3 Data
#             user_id = request.session.get('user_id')
#             if user_id:
#                 user = CustomUser.objects.get(id=user_id)
                
#                 account_holder_name = request.POST.get('account-holder-name')
#                 account_number = request.POST.get('account-number')
#                 bank_name = request.POST.get('bank-name')
#                 branch = request.POST.get('branch')
#                 ifsc_code = request.POST.get('ifsc-code')

#                 seller_details = user.seller_details_user.all().first()

#                 if not seller_details:
#                     seller_details = SellerDetails(
#                         user=user,
#                         account_holder_name=account_holder_name,
#                         account_number=account_number,
#                         bank_name=bank_name,
#                         branch=branch,
#                         ifsc_code=ifsc_code
#                     )
#                     seller_details.save()
#                 else:
#                     seller_details.account_holder_name = account_holder_name
#                     seller_details.account_number = account_number
#                     seller_details.bank_name = bank_name
#                     seller_details.branch = branch
#                     seller_details.ifsc_code = ifsc_code
#                     seller_details.save()

#                 messages.success(request, "Step 3 completed successfully.")
#                 # Redirect to confirmation page or other steps
#                 return redirect('seller_reg_step')

#     return render(request, 'reg_step.html')











def seller_index(request):
    return render(request,'sellerhome.html')


@never_cache    
def shop(request):
    # Get products added by the suppliers
    supplier_products = Product.objects.all()  # You can add filters if needed
    paginator = Paginator(supplier_products, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'supplier_products': supplier_products,
        'page':page
    }
    return render(request, 'shop.html', context)

# @login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop-single.html', {'product': product})



@login_required(login_url='custom_login')
def seller_product_listing(request):
    if request.user.is_seller:
        current_seller = request.user
        seller_products = Product.objects.filter(seller=current_seller)
    
        context = {
            'seller_products': seller_products
        }
    
        return render(request, 'product_list.html', context)
    else:
        # If the logged-in user is not a seller, you can redirect them or show an error message
        # For example, you can redirect them to a page where they can register as a seller
        return redirect('seller_register')



@login_required(login_url='custom_login')
def add_product(request):
    if request.user.is_seller:
        if request.method == 'POST':
            # Retrieve form data from the request
            product_name = request.POST.get('product_name')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            quantity_value = request.POST.get('quantity')  # Updated field name
            quantity_prefix = request.POST.get('quantity_prefix')  # Updated field name
            price = request.POST.get('price')
            brand_name = request.POST.get('brand_name')
            stock = request.POST.get('stock')

            # Validate the form data here if needed
            # You can use your ProductForm for validation

            # Create and save the product
            product = Product(
                product_name=product_name,
                description=description,
                image=image,
                quantity_value=quantity_value,  # Updated field name
                quantity_prefix=quantity_prefix,  # Updated field name
                price=price,
                brand_name=brand_name,
                stock=stock,
                seller=request.user  # Assign the logged-in seller to the product
            )
            product.save()
            return redirect('seller_index')  # Redirect to a page showing the list of products
        else:
            # Render the empty form on a GET request
            return render(request, 'add_product.html')
    else:
        # If the logged-in user is not a seller, you can redirect them or show an error message
        # For example, you can redirect them to a page where they can register as a seller
        return redirect('seller_register')





# @login_required(login_url='custom_login')  # Redirects to the login page if not logged in
# def add_product(request):
#     if request.user.is_seller:
#         if request.method == 'POST':
#             form = ProductForm(request.POST, request.FILES)
#             if form.is_valid():
#                 product = form.save(commit=False)
#                 product.seller = request.user  # Assign the logged-in seller to the product
#                 product.save()
#                 return redirect('index')  # Redirect to a page showing the list of products
#         else:
#             form = ProductForm()

#         return render(request, 'add_product.html', {'form': form})
#     else:
#         # If the logged-in user is not a seller, you can redirect them or show an error message
#         # For example, you can redirect them to a page where they can register as a seller
#         return redirect('seller_register') 




# def update(request,update_id):
#     task=Product.objects.get(id=update_id) 
#     form=create_form(request.POST or None,instance=task) 
#     if form.is_valid():
#         form.save()
#         return redirect('table')
#     return render(request,'update.html',{'form':form})






@login_required(login_url='custom_login')
def customer_Profile(request):
    user_profile, created = Customer_Profile.objects.get_or_create(customer=request.user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_number = request.POST.get('mobile_number')

        # Update the user profile fields
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.mobile_number = mobile_number
        user_profile.save()

        messages.success(request, 'Profile added successfully')  # Display a success message
        return redirect('customer_profile') 
    context = {
        'user_profile': user_profile,
        'form_submitted': request.method == 'POST',
    }
    return render(request,'custprofile.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # cart_item = CartItem.objects.get_or_create(user=request.user, product_id=product.id)
    if product.stock <= 0:
        messages.warning(request, f"{product.product_name} is out of stock.")
    else:
        cart_item,created = CartItem.objects.get_or_create(user=request.user, product_id=product.id)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('shop')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_price': total_price,
        # ... other context variables ...
    }
    return render(request, 'cart.html',context)

def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, id=product_id)
    print(f"Received product_id: {product_id}")  #Fixed the typo here
    cart_item.delete()
    return redirect('cart')




def decrease_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            cart_item.product.stock+=1
        else:
            messages.warning(request, f"{cart_item.product.product_name} is out of stock.")
    except CartItem.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart
    return redirect('cart')  # Redirect back to the cart page after decreasing the item quantity

def increase_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)

        if cart_item.product.stock > 0:
            cart_item.quantity += 1
            cart_item.save()
            cart_item.product.stock -= 1
            cart_item.product.save()
        else:
            messages.warning(request, f"{cart_item.product.product_name} is out of stock.")
    except CartItem.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart
    return redirect('cart')






# -------------------------------------------------admin---------------------------------------------------
# def index_admin(request):
#     return render(request,'admin\indexadmin.html')


from django.http import JsonResponse
from .models import Product  # Make sure to import your Product model

def search_product(request, name):
    print(name)
    
    # Perform the search using a Q object to filter the Product model
    results = Product.objects.filter(product_name__icontains=name)
    
    # Serialize the results to JSON
    serialized_results = []
    
    if results.exists():  # Check if there are any results
        for result in results:
            serialized_results.append({
                'id': result.id,
                'name': result.product_name,
                'image': result.image.url
            })
            print(result.id)
    else:
        print("No results found.")

    return JsonResponse({'results': serialized_results})

    
def checkout(request):
    return render(request,'checkout.html')


def update_product(request, product_id):
    # Get the product object from the database using the product_id
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Retrieve form data from the request
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        brand_name = request.POST.get('brand_name')
        stock = request.POST.get('stock')

        # Update the product data
        product.product_name = product_name
        product.description = description
        product.image = image
        product.quantity = quantity
        product.price = price
        product.brand_name = brand_name
        product.stock = stock

        # Save the updated product data to the database
        product.save()
        return redirect('add_product')  # Redirect to the product detail page
    else:
        # If it's a GET request, render the form with the current product data
        return render(request, 'editproduct.html', {'product': product})


# def delete_product(request, product_id):
#     # Get the product instance to delete
#     product = get_object_or_404(Product, pk=product_id)

#     if request.method == 'POST':
#         # Update the product's status to 'Out of Stock' instead of deleting it
#         product.status = 'Out of Stock'
#         product.save()
#         return redirect('seller_product_listing')  # Redirect to the seller's product listing page or another appropriate page

#     # Render a confirmation page for changing the product's status
#     return render(request, 'product_list.html', {'product': product})







from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



def homepage(request):
    cart_items = CartItem.objects.filter(user=request.user,is_active=True)
    total_price = Decimal(sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items))
    
    currency = 'INR'

    # Set the 'amount' variable to 'total_price'
    amount = int(total_price * 100)
    
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # Order id of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    # Create the order but don't save it yet
    order = Order(
        user=request.user,
        total_price=total_price,
        razorpay_order_id=razorpay_order_id,
        payment_status=Order.PaymentStatusChoices.PENDING,
    )

    # Save the order to generate an order ID
    order.save()

    # Associate the cart items with the order
    for cart_item in cart_items:
        cart_item.order = order
        cart_item.save()

    # Create a context dictionary with all the variables you want to pass to the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'homepage.html', context=context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        # Verify the payment signature.
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        
        if result is False:
            # Signature verification failed.
            return render(request, 'payment/paymentfail.html')
        else:
            # Signature verification succeeded.
            # Retrieve the order from the database
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            
            # Capture the payment with the amount from the order
            amount = int(order.total_price * 100)  # Convert Decimal to paise
            razorpay_client.payment.capture(payment_id, amount)

            # Update the order with payment ID and change status to "Successful"
            order.payment_id = payment_id
            order.payment_status = Order.PaymentStatusChoices.SUCCESSFUL
            order.save()

            # Get the associated cart items for this order
            cart_items = CartItem.objects.filter(order=order)
            
            if cart_items.exists():
                # Get the cart_id from the first cart item
                cart_id = cart_items.first().id
                cart_items.update(is_active=False)

                # Redirect to a success page with the cart_id
                return HttpResponseRedirect(reverse('print_as_pdf', args=[cart_id]))
            else:
                # Cart items not found for the order
                return HttpResponse('No cart items found for the order.')
    
@login_required
def print_as_pdf(request, cart_id):
    try:
        # Get the cart based on cart_id and make sure it belongs to the logged-in user
        cart = CartItem.objects.get(id=cart_id, user=request.user, order__isnull=False)
        print(cart_id)
        # Ensure that the cart has a valid order associated with it
        if cart.order is None:
            raise CartItem.DoesNotExist

        cart_items = CartItem.objects.filter(order=cart.order)
        total_cost = Decimal(sum(item.product.price * item.quantity for item in cart_items))
        total=[]
        for i in cart_items:
            
            total_items=i.product.price * i.quantity
            total.append(total_items)
        # Get the user's name
        user_name = request.user.name

        # Render the HTML template to a string
        context = {
            'cart_id': cart_id,
            'cart_items': cart_items,
            'total_cost': total_cost,
            'user_name': user_name,
            
        }
       
        html = render_to_string('print_invoice.html', context, request=request)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{cart_id}.pdf"'

        # Generate the PDF file from the HTML content
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=None)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response
    except CartItem.DoesNotExist:
        # Handle the case where the cart doesn't exist, doesn't belong to the user, or has no order
        return HttpResponse('Cart not found or does not belong to the user or has no valid order.')


# def my_orders(request):
#     # Assuming you have a user authentication system, get the current user
#     user = request.user

#     # Retrieve a list of orders for the current user
#     orders = Order.objects.filter(user=user).order_by('-order_date')

#     context = {
#         'orders': orders, 
#         # 'product_fields': ['product_name', 'quantity', 'image', 'total_price'],
# # Pass the list of orders to the template
#     }
    


#     return render(request, 'my_orders.html', context)
@login_required
def my_orders(request):
    # Assuming you have a user authentication system, get the current user
    user = request.user
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Get the selected month and year from the form, or use the current month by default
    selected_month = request.GET.get('selected_month', datetime.now().strftime('%Y-%m'))

    # Convert the selected_month string to a datetime object
    selected_date = datetime.strptime(selected_month, '%Y-%m')

    # Retrieve a list of orders for the current user and the selected month
    orders = Order.objects.filter(user=user, order_date__year=selected_date.year, order_date__month=selected_date.month).order_by('-order_date')

    context = {
        'orders': orders, 
        'selected_month': f"{current_month}/{current_year}",        
        'product_fields': ['product_name', 'quantity', 'image_url', 'total_price'],
    }

    # Check if there are no orders for the selected month and display a message
    if not orders:
        context['no_orders_message'] = 'No orders found for the selected month.'

    return render(request, 'my_orders.html', context)


def add_address(request):
    return render(request,'add_address.html')

