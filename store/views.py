from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from store.forms import SignUpForm,SignInForm,UserProfileForm,ProjectForm
from django.views.generic import View,FormView,CreateView,TemplateView
from django.contrib.auth import authenticate,login,logout
from store.models import Project,WishListItem,Order
from django.contrib import messages
from django.db.models import Sum
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

def send_email():
    send_mail(
    "SDownload your projects here",
    "Payment completed",
    "rahul.j.r.m@gmail.com",
    ["rahuljosephreynoldgmail.com"],
    fail_silently=False,
)


# Create your views here.

class SignUpView(CreateView):
    template_name='register.html'
    form_class=SignUpForm
    success_url=reverse_lazy("signin")
    # def get(self,request,*args,**kwargs):
    #     form_instance=self.form_class()
    #     return render(request,self.template_name,{'form':form_instance})
    
    # def post(self,request,*args,**kwargs):
    #     form_instance=self.form_class(request.POST)
    #     if form_instance.is_valid():
    #         form_instance.save()
    #         return redirect("signup")
    #     else:
    #         return render(request,self.template_name,{'form':form_instance})

class SignInView(FormView):
    template_name='login.html'
    form_class=SignInForm

    def post(self,request,*args,**kwargs):
        form_instance=self.form_class(request.POST)
        if form_instance.is_valid():
            uname=form_instance.cleaned_data.get("username")
            pwd=form_instance.cleaned_data.get("password")

            user_object=authenticate(username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("index")
        return render(request,self.template_name,{'form':form_instance})                            

class IndexView(TemplateView):
    template_name='index.html'

    def get(self,request,*args,**kwargs):
        qs=Project.objects.all().exclude(developer=request.user)
        return render(request,self.template_name,{"data":qs})

class SignoutView(View):
    def logout_view(request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
class UserProfileEditView(View):

    template_name="profile_edit.html"

    form_class=UserProfileForm

    def get(self,request,*args,**kwargs):

        user_profile_instance=request.user.profile

        form_instance=UserProfileForm(instance=user_profile_instance)

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        user_profile_instance=request.user.profile

        form_instance=self.form_class(request.POST,instance=user_profile_instance,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("index")
        
        return render(request,self.template_name,{"form":form_instance})

class ProjectCreateView(View):

    template_name="project_add.html"

    form_class=ProjectForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST,files=request.FILES)

        form_instance.instance.developer=request.user

        if form_instance.is_valid():

            form_instance.save()

            return redirect("index")
        
        return render(request,self.template_name,{"form":form_instance})
    
class MyProjectListView(View):

    template_name="my_project.html"

    def get(self,request,*args,**kwargs):

        qs=Project.objects.filter(developer=request.user)

        return render(request,self.template_name,{"data":qs})
    
class ProjectUpdateView(View):

    template_name="project_update.html"

    form_class=ProjectForm

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_object=Project.objects.get(id=id)

        form_instance=self.form_class(instance=project_object)

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_object=Project.objects.get(id=id)

        form_instance=self.form_class(request.POST,instance=project_object,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("my-work")
        
        return render(request,self.template_name,{"form":form_instance})

# class ProjectViewMoreView(View):
#     template_name="project_view_more.html"

#     def get(self,request,*args,**kwargs):

#         qs=Project.objects.filter(developer=request.user)

#         return render(request,self.template_name,{"data":qs})

class ProjectViewMore(View):
    template_name = "project_view_more.html"  

    def get(self, request, *args, **kwargs):

        id = kwargs.get("pk")  

        project_object = Project.objects.get(id=id) 

        return render(request, self.template_name, {"p": project_object})
    
class AddToWishListView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_object=get_object_or_404(Project,id=id)

        try:
            request.user.basket.basket_item.create(project_object=project_object)

            print("Successfully added to wishlist")

            messages.success(request,"successfully added an item to wishlist")

        except Exception as e:

            messages.error(request,"failed to add an item to wishlist")      

        return redirect("index")

class MyWishListItemView(View):

    template_name="mywishlist.html"

    def get(self,request,*args,**kwargs):

        qs=request.user.basket.basket_item.filter(is_order_placed=False)

        total=qs.values("project_object").aggregate(total=Sum("project_object__price")).get("total")

        print("total1",total)

        return render(request,self.template_name,{"data":qs,"total":total})

class WishListItemDeleteView(View):

    def get(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")

        WishListItem.objects.get(id=id).delete()

        return redirect("my-wishlist")
    

import razorpay
# class CheckOutView(View):
#     templatename='checkout.html'
#     def get(self,request,*args,**kwargs):
#         KEY_ID="rzp_test_hIMKNhJU9oHOAV"
#         KEY_SECRET="PZyRgKWu7WyoiNfdBvkhdESB"
#         client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

#         amount=request.user.basket.basket_item.filter(is_order_placed=False).values("project_object").aggregate(total=Sum("project_object__price")).get("total")
#         data = { "amount": amount*100, "currency": "INR", "receipt": "order_rcptid_11" }
#         payment = client.order.create(data=data)
#         order_id=payment.get("id")
#         order_object=Order.objects.create(order_id=order_id,customer=request.user)
#         wishlist_items=request.user.basket.basket_item.filter(is_order_placed=False)
#         for wi in wishlist_items:
#             order_object.wishlist_item_objects.add(wi)
#             wi.is_order_placed=True
#             wi.save()

#         # print(payment)
#         return render(request,self.templatename)


import razorpay
class CheckOutView(View):

    template_name="checkout.html"

    def get(self,request,*args,**kwargs):

        KEY_ID="rzp_test_hIMKNhJU9oHOAV"

        KEY_SECRET="PZyRgKWu7WyoiNfdBvkhdESB"

        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        wishlist_total=request.user.basket.basket_item.filter(is_order_placed=False).values("project_object").aggregate(total=Sum("project_object__price")).get("total")

        data = { "amount": wishlist_total*100, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)

        print(payment)

        order_id=payment.get("id")

        order_object=Order.objects.create(order_id=order_id,customer=request.user)

        wishlist_items=request.user.basket.basket_item.filter(is_order_placed=False)

        for wi in wishlist_items:

            order_object.wishlist_item_objects.add(wi)
            wi.is_order_placed=True
            wi.save()

        return render(request,self.template_name,{"key_id":KEY_ID,"amount":wishlist_total,"order_id":order_id})


@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerification(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)

        KEY_ID="rzp_test_hIMKNhJU9oHOAV"

        KEY_SECRET="PZyRgKWu7WyoiNfdBvkhdESB"

        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        try:
            client.utility.verify_payment_signature(request.POST)
            order_id=request.POST.get("razorpay_order_id")
            Order.objects.filter(order_id=order_id).update(is_paid=True)
            send_email()
            print("success")
            

        except:
            print("fail")

        return redirect("orders")
    

class MyoderView(View):
    template_name="my_order.html"

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(customer=request.user)

        return render(request,self.template_name,{"data":qs})
    

        

        






