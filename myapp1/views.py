from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import View

#email
import smtplib
import email.message

import json
#time
import time
from datetime import timezone
import pytz
from django.contrib import messages
import datetime
# paytm ids -------------------------
from django.views.decorators.csrf import csrf_exempt
from Pay import Checksum
from django.urls import reverse_lazy
from django.urls import reverse

from django.db.models import Q

# Gerate OTP
import random

# SMPT Email Send
import smtplib 
import email.message
# Create your views here.

# Html To Pdf -------------------

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from django.http import HttpResponse
from django.views.generic import View

import pdfkit

# Html To Pdf ------------------- 


# Excel ----------------------------

# pip install xlwt
# pip install xlutils    # Required when reading excel file
# pip install xlrd       # Required when reading excel file
import xlwt
# Excel ----------------------------

# pip install pycryptodome

MERCHANT_KEY = '@BLNEQSVwvSAf36N'
MERCHANT_ID = 'DSpKiN27217000419407'
 # Create your views here.

def login(request):
    if request.POST:
        em = request.POST['username']
        pas = request.POST['pass']
        try:
            valid = UsersData.objects.get(email_id=em)
            if valid.password == pas:
                request.session['user_data'] = valid.id
                return redirect('home')
            else:
                messages.error(request, 'Wrong Password...')
                return render(request,'Login_Regi/Login.html')
        except:
            messages.error(request, 'Wrong Email Id...')
            return render(request,'Login_Regi/Login.html')
    return render(request,'Login_Regi/Login.html')

def register(request):
    if request.POST:
        username = request.POST['username']
        email_id = request.POST['email_id']
        pno = request.POST['pno']
        pass1 = request.POST['pass']
        
        try:
            valid = UsersData.objects.get(email_id=email_id)
            messages.error(request, 'Email Id Already In Use...')
            return render(request,'Login_Regi/Regi.html')
        except:
            try:
                valid = UsersData.objects.get(contact=pno)
                messages.error(request, 'Contact No Already Exists...')
                return render(request,'Login_Regi/Regi.html')
            except:
                obj = UsersData()
                obj.u_name = username
                obj.email_id = email_id
                obj.contact = pno
                obj.password = pass1
                obj.save()
                return redirect('login')
    return render(request,'Login_Regi/Regi.html')


def Index(request):
    vends = vendor.objects.all()
    prds = product.objects.all()
    nav_cat = category.objects.all()
    nav_scat = Sub_category.objects.all()
    print(prds)
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        cart = request.session['cart']
    print(cart)    
    try:
        q = request.GET.get('search')
    except:
        q = None
    if q:
        prod= product.objects.filter(Q(p_name__icontains=q) | Q(p_discription__icontains=q) | Q(p_price__icontains=q))
        dealer = vendor.objects.filter(Q(Shop_name__icontains=q) | Q(shop_address__icontains=q))
        if 'user_data' in request.session.keys():
            em = request.session['user_data']
            valid = UsersData.objects.get(id=int(em))
            data = {
                'pro' : prod,
                'des': dealer,
                'owns':vends,
                'prds':prds,
                'user_data':valid,
                'nav_cat':nav_cat,
                'nav_scat':nav_scat,
            }
        else:
            data = {
                'pro' : prod,
                'des': dealer,
                'owns':vends,
                'prds':prds,
                'nav_cat':nav_cat,
                'nav_scat':nav_scat,
            }
    else:
        if 'user_data' in request.session.keys():
            em = request.session['user_data']
            valid = UsersData.objects.get(id=int(em))
            data={'owns':vends,'user_data':valid,'prds':prds,'nav_cat':nav_cat,'nav_scat':nav_scat}
            try:
                valid_cart = Cart.objects.get(U_id=valid)
                request.session['cart'] = json.loads(valid_cart.P_id)
                cart = request.session['cart']
                cart_rec = json.dumps(cart)
                valid_cart.P_id = cart_rec
                valid_cart.save()
            except:
                valid_cart = Cart()
                cart_rec = json.dumps(cart)
                valid_cart.U_id = valid
                valid_cart.P_id = cart_rec
                valid_cart.save()
        else:
            data={'owns':vends,'prds':prds,'nav_cat':nav_cat,'nav_scat':nav_scat}
            
    return render(request,'index.html',data)
    


# Forget Password -----------------

def forgot_pass(request):
    if request.POST:
        email1 = request.POST['email']
        number1 = request.POST['m_no']
            
        try:
            valid = UsersData.objects.get(email_id=email1)
            if int(valid.contact) == int(number1):
                print(email1)
                request.session['useremail'] = email1
                
                numbers = [1,2,3,4,5,6,7,8,9,0]
                num = ""
                for i in range(4):
                    num += str(random.choice(numbers))
                
                num = int(num)
                print(num)
                
                # ============== Email ==============
                
                sender_email = "harshilsoni011@gmail.com"
                sender_pass = "Harshil123$"
                receiver_email = email1

                server = smtplib.SMTP('smtp.gmail.com',587)

                your_message = "This Is Your OTP Number = "+str(num)

                print(your_message)

                msg = email.message.Message()
                msg['Subject'] = "Your OTP"
                msg['From'] = sender_email
                msg['To'] = receiver_email
                password = sender_pass
                msg.add_header('Content-Type','text/html')
                msg.set_payload(your_message)

                server.starttls()
                server.login(msg['From'],password)
                server.sendmail(msg['From'],msg['To'],msg.as_string())
                
                # ============== End Email ===========
                
                request.session['otp'] = num
                
                return render(request,'OTP.html',{'otp':num})
                                    
            else:
                return HttpResponse("<h2><a href=''>Mobile Number Is Not Registered</a></h2>")
                return redirect('forgotpass')
        except:
            return HttpResponse("<h2><a href=''>Email Is Not Registered</a></h2>")
            return redirect('forgotpass')
        
    return render(request,'Forget_Pass.html')

def otpcheck(request):
    if request.session.has_key('otp'):
        if request.POST:
            otp = request.POST['otp']
            if int(request.session['otp']) == int(otp):
                del request.session['otp']
                return redirect('newpassword')
            else:
                return HttpResponse("<h2><a href=""> You Have Entered Wrong OTP </a></h2>")
        else:
            return redirect('forgotpass')
    return redirect('login')

def newpassword(request):
    if request.session.has_key('useremail'):
        if request.POST:
            pass_1 = request.POST['pass1']
            pass_2 = request.POST['pass2']
            
            if pass_1 == pass_2:
                valid = UsersData.objects.get(email_id=request.session['useremail'])
                valid.password = pass_2
                valid.save()
                del request.session['useremail']
                return redirect('login')
            else:
                return HttpResponse("<h2><a href=''>Passwords Are Not Same ...</a></h2>")
        return render(request,'New_Pass.html')
    return redirect('login')

# Forget Password -----------------


def Shop_View(request,id):
    vends = vendor.objects.get(id=id)
    cats = category.objects.all()
    s_cat = Sub_category.objects.all()
    nav_cat = category.objects.all()
    nav_scat = Sub_category.objects.all()
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(id=int(em))
        sb_data=""
        try:
            sd = subscribe_data.objects.get(usersData=valid,vendors=vends)
            sb_data='subscribed'
        except:
            sb_data='Not'
        
        if request.POST:
            did = request.POST['did']
            ssd = subscribe_data()
            ssd.usersData=valid
            ssd.vendors=vends
            ssd.save()    
            return redirect('Shop_View',id)
        return render(request,'own_cats.html',{'sb_data':sb_data,'owns':vends,'s_cat':s_cat,'cats':cats,'user_data':valid,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        return render(request,'own_cats.html',{'owns':vends,'s_cat':s_cat,'cats':cats,'nav_cat':nav_cat,'nav_scat':nav_scat})

def cat_view(request,id):
    cats = category.objects.get(id=id)
    sub_cat = Sub_category.objects.all()
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(id=int(em))
        return render(request,'own_cats.html',{'sub_cat':sub_cat,'cat':cats,'user_data':valid})
    else:
        return render(request,'own_cats.html',{'sub_cat':sub_cat,'cat':cats})

def show_prods(request,jid,iid,oid):
    cats = category.objects.get(id=iid)
    sub_cat = Sub_category.objects.get(id=jid)
    ven = vendor.objects.get(id=oid)    
    nav_cat = category.objects.all()
    nav_scat = Sub_category.objects.all()
    prods = product.objects.filter(sub_cate=sub_cat,cate=cats,venders=ven)
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(id=int(em))
        return render(request,'own_cats.html',{'scat':sub_cat,'prod':prods,'user_data':valid,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        return render(request,'own_cats.html',{'scat':sub_cat,'prod':prods,'nav_cat':nav_cat,'nav_scat':nav_scat})

def show_all_prods(request,jid,iid):
    cats = category.objects.get(id=iid)
    sub_cat = Sub_category.objects.get(id=jid)
    nav_cat = category.objects.all()
    nav_scat = Sub_category.objects.all()
    prods = product.objects.filter(sub_cate=sub_cat,cate=cats)
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(id=int(em))
        return render(request,'own_cats.html',{'scat':sub_cat,'all_prod':prods,'user_data':valid,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        return render(request,'own_cats.html',{'scat':sub_cat,'all_prod':prods,'nav_cat':nav_cat,'nav_scat':nav_scat})

def Show_Product(request,id):
    if 'user_data' in request.session.keys():
        prod_data = product.objects.get(id=id)
        feed = feedbacks_of_product.objects.filter(Product_name = prod_data)
        Users = UsersData.objects.get(id=int(request.session['user_data']))
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        try:
            obj = feedbacks_of_product.objects.get(Product_name=prod_data,cust=Users)
            
            if request.POST:
                ids = request.POST['ids']
                prate = request.POST['prate']
                pfeedback = request.POST['pfeedback']
                obj.rating = prate
                obj.feedback = pfeedback
                obj.save()
                return redirect('Show_Product',int(ids))
            return render(request,'own_cats.html',{'keys':obj,'feed':feed,'prod_data':prod_data,'user_data':Users,'nav_cat':nav_cat,'nav_scat':nav_scat})
        except:
            if request.POST:
                ids = request.POST['ids']
                prate = request.POST['prate']
                pfeedback = request.POST['pfeedback']
                
                obj = feedbacks_of_product()
                prod_data = product.objects.get(id=int(ids))
                obj.Product_name = prod_data
                obj.cust = Users
                obj.rating = prate
                obj.feedback = pfeedback
                obj.save()
                return redirect('Show_Product',int(ids))
            return render(request,'own_cats.html',{'feed':feed,'prod_data':prod_data,'user_data':Users,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        prod_data = product.objects.get(id=id)
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        feed = feedbacks_of_product.objects.filter(Product_name = prod_data)
        return render(request,'own_cats.html',{'feed':feed,'prod_data':prod_data,'nav_cat':nav_cat,'nav_scat':nav_scat})

def Cust_Chats(request):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(id=int(request.session['user_data']))
        mci = ModelChat_IDs.objects.filter(usersData=Users)
        return render(request,'CustChats.html',{'mci':mci})
    else:
        return redirect('ved_login')  

def Chat_Data_Show(request,id):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(id=int(request.session['user_data']))
        venders = vendor.objects.get(id=id)
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        try:
            moch = ModelChat_IDs.objects.get(usersData = Users,vendors=venders)
            print(moch.chat_id)
            mode_ch = Models_Chats.objects.filter(ch_ids=moch)
            print(mode_ch)
            if request.POST:
                ptext = request.POST['ptext']
                
                obj = Models_Chats()
                obj.ch_ids=moch
                obj.usersData = Users
                obj.problem_text = ptext
                obj.save()    
                return redirect('Chat_Data_Show',id)
            return render(request,'Chat_Data_Show.html',{'mc':mode_ch,'moch':moch,'user_data':Users,'nav_cat':nav_cat,'nav_scat':nav_scat})
        except:
            tz= pytz.timezone('Asia/Kolkata')
            time_now = datetime.datetime.now(timezone.utc).astimezone(tz)
            millis = int(time.mktime(time_now.timetuple()))
            chats_id = "Chat"+str(millis)
            
            obj = ModelChat_IDs()
            obj.chat_id = str(chats_id)
            obj.usersData = Users
            obj.vendors = venders
            obj.save()
            return render(request,'Chat_Data_Show.html',{'user_data':Users,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        return redirect('login')
    
def Customer_Orders(request):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(id=int(request.session['user_data']))
        otdata = order_table.objects.filter(cust=Users)
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        rec = set()
        for i in otdata:
            rec.add(i.order_id)
        rec = list(rec)
        rec.sort()
        return render(request,'custAllOrders.html',{'oids':rec,'user_data':Users,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        return redirect('login')
    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def ViewSpecify_Bill(request,Orids):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(id=int(request.session['user_data']))
        otdata = order_table.objects.filter(cust=Users,order_id=Orids)
        tots = 0
        status = ""
        for i in otdata:
            if i.cancel == True:
                status = "Cancle"
            tots += float(i.total)
        
        # if status == "Cancel":
        Current_Date = datetime.datetime.today() + datetime.timedelta(days=2)
        print ('Current Date: ' + str(Current_Date))

        NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=7)
        print ('Next Date: ' + str(NextDay_Date))
        data = {'status':status,'bilam':tots,'Orids':Orids,'orders':otdata,'oids':Orids,'users':Users,'NextDay_Date':NextDay_Date}
        return render(request,'ViewSpecificBill.html',data)
        
        # data = {'bilam':tots,'Orids':Orids,'orders':otdata,'oids':Orids,'users':Users,'status':status}
        # return render(request,'ViewSpecificBill.html',data)
    else:
        return redirect('login')

def View_specific(request,Orids):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(id=int(request.session['user_data']))
        otdata = order_table.objects.filter(cust=Users,order_id=Orids)
        tots = 0
        orid = ''
        for i in otdata:
            orid = i.order_id
            tots += float(i.total)
        try:
            objs_data = Address.objects.get(order_id=orid)
        except:
            objs_data = "no"
        
        data = {'adds':objs_data,'bilam':tots,'orders':otdata,'oids':Orids,'users':Users}
        pdf = render_to_pdf('GeneratePdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return redirect('login')

def cancel_data(request,Orids):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(id=int(request.session['user_data']))
        otdata = order_table.objects.filter(order_id=Orids)
        vendata = owner_order_table.objects.filter(order_id=Orids)
        
        for i in otdata:
            i.cancel = True
            i.save()
        
        for i in vendata:
            i.cancel = True
            i.save()
        
        return redirect('ViewSpecify_Bill',str(Orids))
        
    else:
        return redirect('login')

class Orders(View):
    def post(self, request):
        prod = request.POST.get('product')   
        print(prod)
        pay_data = request.POST.get('pay_data')   
        idss_data = request.POST.get('idss_data')   
        sid = request.POST.get('ssid')
        sjid = request.POST.get('ssjid')
        ids = request.POST.get('idss')
        jids = request.POST.get('jidss')
        oids = request.POST.get('oidss')
        porid = request.POST.get('porid')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(prod)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(prod)
                    else:
                        cart[prod]  = quantity-1
                else:
                    cart[prod]  = quantity+1 
            else:
                cart[prod] = 1
        else:
            cart = {}
            cart[prod] = 1
            

        request.session['cart'] = cart
        
        Users = UsersData.objects.get(id=int(request.session['user_data']))
        
        try:
            valid = Cart.objects.get(U_id=Users)
            cart_rec = json.dumps(cart)
            valid.P_id = cart_rec
            valid.save()
        except:
            valid = Cart()
            cart_rec = json.dumps(cart)
            valid.U_id = Users
            valid.P_id = cart_rec
            valid.save()
        
        
        print('cart' , request.session['cart'])
        
        if ids != None:
            return redirect('show_prods',jids,ids,oids)
        elif idss_data != None:
            return redirect('product')
        elif pay_data != None:
            return redirect('cart_order')
        elif sid != None and sjid != None:
            return redirect('show_all_prods',sjid,sid)
        elif porid != None:
            return redirect('Show_Product',int(porid))
        
    def get(self, request):
        return redirect('home')

def Add_Wish_List(request,id):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(id=int(request.session['user_data']))
        JI = product.objects.get(id=id)
        try:
            wL = Wishlist.objects.get(P_id=JI,U_id=user)
            return redirect('Wish_List')    
        except:
            WL = Wishlist()
            WL.U_id = user
            WL.P_id = JI
            WL.save()
        return redirect('Wish_List')
    else:
        return redirect('login')

def remove_wishlist(request,id):
    if 'user_data' in request.session.keys():
        wL = Wishlist.objects.get(id=id)
        wL.delete()
        return redirect('Wish_List')    
    else:
        return redirect('login')

def Wish_List(request):
    if 'user_data' in request.session.keys():
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        user = UsersData.objects.get(id=int(request.session['user_data']))
        U_id = Wishlist.objects.filter(U_id=user)
        return render(request,'WishList.html',{'prod':U_id,'user_data':user,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        return redirect('login')

def SubScribeData(request):
    if 'user_data' in request.session.keys():
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        user = UsersData.objects.get(id=int(request.session['user_data']))
        U_id = subscribe_data.objects.filter(usersData=user)
        return render(request,'subscribedata.html',{'prod':U_id,'user_data':user,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        return redirect('login')

def COD_Data(request):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(id=int(request.session['user_data']))
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        if request.POST:
            ids = list(request.session.get('cart').keys())
            products = product.get_products_by_id(ids)
            cart = request.session['cart']
            Final_Bill = {}
            # request.session['Final_Bill']
            print(cart)
            print("\n-----------------------")
            print(products)
            count = []
            for p in products:
                print("\n-----------------------")
                for i in ids:
                    if int(i) == p.id:
                        data = {}
                        data['id'] = p.id
                        print("product Name = ",p.p_name)
                        data['name'] = p.p_name
                        print("product QTY = ",cart.get(i))
                        data['qty'] = cart.get(i)
                        print("product Price = ",int(p.p_price) * int(cart.get(i)))
                        data['price'] = int(p.p_price) * int(cart.get(i))
                        count.append(data)

            Final_Bill['products'] = count
            Final_Bill['total_price'] = request.POST['total_price']
            print(request.POST['total_price'])
            print(Final_Bill)
            request.session['Final_Bill'] = Final_Bill
            print(request.session['Final_Bill'])
            request.session['Order_total'] = request.POST['total_price']
            print("\n\n-----------------------")
            
            show_data = request.session['Final_Bill']
            amo = request.session['Order_total']
            order_id = request.session['Order_id']
            
            obj = Address()
            obj.order_id = order_id
            obj.strAdd = request.POST["sa"]
            obj.Add = request.POST["add"]
            obj.city = request.POST["city"]
            obj.state = request.POST["state"]
            obj.zip1 = request.POST["zip"]
            obj.save()
            
            # store in data base ----------------------  
            owner_nm = set()
            date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            for i in show_data['products']:
                prod = product.objects.get(id=i['id'])
                obj = order_table()
                obj.cust = user
                obj.order_id = order_id
                obj.date = str(date)
                obj.img = prod.imgs
                obj.product = i['name']
                obj.qty = i['qty']
                obj.price = prod.p_price
                obj.total = i['price']
                obj.payment = False
                obj.save()
                
                
                v_p = i['price']
                v_p = ((float(v_p) * 20)/100)
                i['price'] = (float(i['price']) - float(v_p))
                
                owner = vendor.objects.get(id=prod.venders.id)
                owner_nm.add(owner)
                owner_order = owner_order_table()
                owner_order.owner = owner
                owner_order.cust = user
                owner_order.order_id = order_id
                owner_order.date = str(date)
                owner_order.product = i['name']
                owner_order.qty = i['qty']
                owner_order.price = prod.p_price
                owner_order.total = i['price']
                owner_order.payment = False
                owner_order.save()
                
                    
                a_pay = Payment()
                a_pay.U_id = user
                a_pay.V_id = owner
                a_pay.P_mode = "COD"
                a_pay.P_amount = v_p
                a_pay.save()
                
            
            for i in owner_nm:
                ven_user = vendor.objects.get(id=i.id)
                # data = order_table.objects.filter(cust = user)
                list_id = owner_order_table.objects.filter(owner = ven_user).values_list('order_id', flat=True)
                list_id = list(set(list(list_id)))
                
                for i in list_id: #Order1606811186
                    obj = Owner_Payment()
                    obj.Owner = ven_user
                    obj.Order_id = str(i)
                    data = owner_order_table.objects.filter(owner = ven_user).filter(order_id = str(i)) #Order1606811186
                    tot = 0
                    for d in data:
                        obj.date = d.date
                        tot += float(d.total)
                    obj.Order_amount = "Cash On Delivery"
                    obj.save()

            # session Delete ------------------ 
            cart = request.session.get('cart')
            if cart:
                request.session['Final_Bill'] = {}
                request.session['Order_total'] = {}
                request.session['cart'] = {}
                cart = request.session['cart']
                valid = Cart.objects.get(U_id=user)
                cart_rec = json.dumps(cart)
                valid.P_id = cart_rec
                valid.save()
            
            return redirect('home')
            
        
        print("CAll")
        ids = list(request.session.get('cart').keys())
        products = product.get_products_by_id(ids) #get_cust_details_by_id
        print(products)        
        
        tz= pytz.timezone('Asia/Kolkata')
        time_now = datetime.datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        order_id = "Order"+str(millis)
        request.session['Order_id'] = order_id
        # order_id = request.session['Order_id']
        

        Current_Date = datetime.datetime.today() + datetime.timedelta(days=4)
        print ('Current Date: ' + str(Current_Date))

        NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=5)
        print ('Next Date: ' + str(NextDay_Date))
        return render(request,'COD.html',{'nav_scat':nav_scat,'nav_cat':nav_cat,'products' : products,'Current_Date':Current_Date,'NextDay_Date':NextDay_Date})
    else:
        return redirect('login')
    
def cart_order(request):    
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(id=int(em))
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        if request.POST:
            ids = list(request.session.get('cart').keys())
            products = product.get_products_by_id(ids)
            cart = request.session['cart']
            Final_Bill = {}
            count = []
            for p in products:
                for i in ids:
                    if int(i) == p.id:
                        data = {}
                        data['id'] = p.id
                        data['name'] = p.p_name
                        data['qty'] = cart.get(i)
                        data['price'] = int(p.p_price) * int(cart.get(i))
                        count.append(data)

            Final_Bill['products'] = count
            Final_Bill['total_price'] = request.POST['total_price']
            request.session['Final_Bill'] = Final_Bill
            request.session['Order_total'] = request.POST['total_price']
            
            
            obj = Address()
            obj.strAdd = request.POST["sa"]
            obj.Add = request.POST["add"]
            obj.city = request.POST["city"]
            obj.state = request.POST["state"]
            obj.zip1 = request.POST["zip"]
            obj.save()
            
            
            return redirect('check')
        
        ids = list(request.session.get('cart').keys())
        print(ids)
        if ids == []:
            return redirect('product')
        products = product.get_products_by_id(ids) #get_cust_details_by_id
        return render(request,'order.html',{'products' : products,'user_data':valid,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        return redirect('login')

# Payment -----------------------------

def Checkout(request):
    if 'user_data' in request.session.keys():
        tz= pytz.timezone('Asia/Kolkata')
        time_now = datetime.datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        order_id = "Order"+str(millis)
        request.session['Order_id'] = order_id
        obj = Address.objects.last()
        obj.order_id = order_id
        obj.save()
        return redirect('process_payment')
    else:
        return redirect('login')
    
def Process_payment(request):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(id=int(request.session['user_data']))
        show_data = request.session['Final_Bill']
        amo = request.session['Order_total']
        host = request.get_host()
        param_dict = {
            'MID': MERCHANT_ID,
            'ORDER_ID': str(request.session['Order_id']),
            'TXN_AMOUNT': str(amo),
            'CUST_ID': 'darpan_salunke',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://{}{}'.format(host,reverse('handlerequest')),
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'payMent/paytm.html', {'param_dict': param_dict,'User':user,'Order':show_data})
    else:
        return redirect('login')

def EmailCall(request):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(id=int(request.session['user_data']))
        show_data = request.session['Final_Bill']
        amo = request.session['Order_total']
        order_id = request.session['Order_id']
        
        try:
            my_email = "harshilsoni011@gmail.com"
            my_pass = "Harshil123$"
            # fr_email = str(user.email)
            fr_email = "hetvikakkad11@gmail.com"
            
            server = smtplib.SMTP('smtp.gmail.com',587)
            mead_data = ""
            front = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div>
                        <h2>Name : """ + user.u_name + """</h2>
                        <h2>Email : """ + user.email_id + """</h2>
                        <h2>Order No: """ + order_id + """</h2>
                    </div>
                    <br>
                    <div>
                        <table border="2">
                            <thead>
                                <tr>
                                    <th>
                                        Product Name
                                    </th>
                                    <th>
                                        Product Qty
                                    </th>
                                    <th>
                                        Product Price
                                    </th>
                                </tr>
                            </thead>
                            <tbody>"""
                            
            for i in show_data['products']:
                mead_data += """<tr>
                <td>""" + str(i['name']) + """ </td>
                <td>""" + str(i['qty']) + """ </td> 
                <td>""" + str(i['price']) + """</td></td>
                </tr> """
                
            ended = """<tr>
            <td colspan="2">
            You Have Paid
            </td><td> """ + str(amo) + """
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div> 
                    <br>
                    <div>
                        <h3>Thank you for visiting ....</h3>
                    </div>
                </body>
            </html>
            """
            email_content = front + mead_data + ended
            print(email_content)
            
            msg = email.message.Message()
            msg['Subject'] = 'Your Bill' 
            msg['From'] = my_email
            msg['To'] = fr_email
            password = my_pass
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)
            s = smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            
            # store in data base ----------------------  
            owner_nm = set()
            date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            for i in show_data['products']:
                prod = product.objects.get(id=i['id'])
                obj = order_table()
                obj.cust = user
                obj.order_id = order_id
                obj.date = str(date)
                obj.img = prod.imgs
                obj.product = i['name']
                obj.qty = i['qty']
                obj.price = prod.p_price
                obj.total = i['price']
                obj.payment = True
                obj.save()
                
                v_p = i['price']
                v_p = ((float(v_p) * 20)/100)
                i['price'] = (float(i['price']) - float(v_p))
                
                owner = vendor.objects.get(id=prod.venders.id)
                owner_nm.add(owner)
                owner_order = owner_order_table()
                owner_order.owner = owner
                owner_order.cust = user
                owner_order.order_id = order_id
                owner_order.date = str(date)
                owner_order.product = i['name']
                owner_order.qty = i['qty']
                owner_order.price = prod.p_price
                owner_order.total = i['price']
                owner_order.payment = True
                owner_order.save()
                
                a_pay = Payment()
                a_pay.U_id = user
                a_pay.V_id = owner
                a_pay.P_mode = "PayTm"
                a_pay.P_amount = v_p
                a_pay.save()
            
            for i in owner_nm:
                ven_user = vendor.objects.get(id=i.id)
                # data = order_table.objects.filter(cust = user)
                list_id = owner_order_table.objects.filter(owner = ven_user).values_list('order_id', flat=True)
                list_id = list(set(list(list_id)))
                
                for i in list_id: #Order1606811186
                    obj = Owner_Payment()
                    obj.Owner = ven_user
                    obj.Order_id = str(i)
                    data = owner_order_table.objects.filter(owner = ven_user).filter(order_id = str(i)) #Order1606811186
                    tot = 0
                    for d in data:
                        obj.date = d.date
                        tot += float(d.total)
                    obj.Order_amount = tot
                    obj.save()

            # session Delete ------------------ 
            cart = request.session.get('cart')
            if cart:
                request.session['Final_Bill'] = {}
                request.session['Order_total'] = {}
                request.session['cart'] = {}
                cart = request.session['cart']
                valid = Cart.objects.get(U_id=user)
                cart_rec = json.dumps(cart)
                valid.P_id = cart_rec
                valid.save()
            
            return redirect('home')
        except:
            return HttpResponse("Email Not Sent")
    else:
        return redirect('login')    
    # return redirect('home')
            
        # ================== email end ================

@csrf_exempt
def Handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful') 
            return redirect('emailcall')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentsatus.html', {'response': response_dict})

# Payment -----------------------------

def Cust_Checkout(request,id):
    if 'user_data' in request.session.keys():
        tz= pytz.timezone('Asia/Kolkata')
        time_now = datetime.datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        order_id = "Order"+str(millis)
        request.session['cust_Order_id'] = order_id
        request.session['cust__id'] = id
        data = Custome_Order.objects.get(id = id)
        request.session['cust__tot'] = float(data.price)
        return redirect('cust_process_payment')
    else:
        return redirect('login')

def cust_Process_payment(request):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(id=int(request.session['user_data']))
        amo = request.session['cust__tot']
        host = request.get_host()
        param_dict = {
            'MID': MERCHANT_ID,
            'ORDER_ID': str(request.session['cust_Order_id']),
            'TXN_AMOUNT': str(amo),
            'CUST_ID': 'darpan_salunke',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://{}{}'.format(host,reverse('cust_handlerequest')),
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'payMent/paytm.html', {'param_dict': param_dict,'User':user})
    else:
        return redirect('login')

def Update_Cust(request):
    if 'user_data' in request.session.keys():
        if 'cust__id' in request.session.keys():
            data = Custome_Order.objects.get(id = request.session['cust__id'])
            data.pay = True
            data.status = "Pay"
            data.save()
            return redirect('Custome_Order_Form')
        else:
            return redirect('home')
    else:
        return redirect('login')

@csrf_exempt
def cust_Handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful') 
            return redirect('Update_Cust')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentsatus.html', {'response': response_dict})
# Payment -----------------------------

def Profile(request):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(id=int(request.session['user_data']))
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        if request.POST:
            u_name = request.POST['u_name']
            Email = request.POST['Email']
            address = request.POST['address']
            contact = request.POST['contact']
            Password = request.POST['Password']
            profile = request.FILES.get('profile')
            country = request.POST['country']
            state = request.POST['state']
            city = request.POST['city']
            Pincode = request.POST['Pincode']
            
            user.u_name = u_name
            user.email_id = Email
            request.session['user_data'] = user.id
            user.address = address
            user.contact = contact
            user.country = country
            user.state = state
            user.city = city
            user.pincode = Pincode
            user.password = Password
            if profile != None:
                user.profile = profile
            user.save()
            return redirect('Profile')
        return render(request,'Profile_data.html',{'user_data':user,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        return redirect('login')

def Cust_Logout(request):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(id=int(request.session['user_data']))
        
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        else:
            print(cart)
            try:
                valid = Cart.objects.get(U_id=Users)
                cart_rec = json.dumps(cart)
                valid.P_id = cart_rec
                valid.save()
                del request.session['cart']
            except:
                valid = Cart()
                cart_rec = json.dumps(cart)
                valid.U_id = Users
                valid.P_id = cart_rec
                valid.save()
                del request.session['cart']
        del request.session['user_data']
        return redirect('login')
    else:
        return redirect('login')

def about(request):
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(id=int(em))
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        return render(request,'about.html',{'user_data':valid,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        return render(request,'about.html',{'nav_cat':nav_cat,'nav_scat':nav_scat})

def Contact(request):
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(id=int(em))
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        
        if request.POST:
            Name = request.POST.get('Name')
            Email = request.POST.get('Email')
            Phone = request.POST.get('Phone')
            Message = request.POST.get('Message')
        
            try:
                my_email = "harshilsoni011@gmail.com"
                my_pass = "Harshil123$"
                fr_email = "hetvikakkad11@gmail.com"
                
                server = smtplib.SMTP('smtp.gmail.com',587)
                email_content = f"""
                You Have New Message From ...
                
                Name = {Name}
                Email = {Email}
                Phone = {Phone}
                Message = {Message}
                
                Thank You.
                """
                print(email_content)
                
                msg = email.message.Message()
                msg['Subject'] = 'You Have New Message' 
                msg['From'] = my_email
                msg['To'] = fr_email
                password = my_pass
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(email_content)
                s = smtplib.SMTP('smtp.gmail.com',587)
                s.starttls()
                s.login(msg['From'], password)
                s.sendmail(msg['From'], [msg['To']], msg.as_string())
            except:
                return HttpResponse("Email Not Sent")
                
        return render(request,'Contact.html',{'user_data':valid,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        return render(request,'Contact.html',{'nav_cat':nav_cat,'nav_scat':nav_scat})

def Product(request):
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(id=int(em))
        prods = product.objects.all()
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        return render(request,'product.html',{'prod':prods,'user_data':valid,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        prods = product.objects.all()
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        return render(request,'product.html',{'prod':prods,'nav_cat':nav_cat,'nav_scat':nav_scat})

def Product_details(request):
    return render(request,'product_detail3.html')

def blog(request):
    return render(request,'blog.html')

def form(request):
    return render(request,'Admin_templates/form.html')

def Custome_Order_Form(request):
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(id=int(em))
        prods = Custome_Order.objects.filter(U_id = valid)
        nav_cat = category.objects.all()
        nav_scat = Sub_category.objects.all()
        vend = vendor.objects.all()
        if request.POST:
            ncat = request.POST['ncat']
            nscat = request.POST['nscat']
            ndetail = request.POST['ndetail']
            ndocs = request.FILES.get('ndocs')
            nvend = request.POST['nvend']
            
            nv = vendor.objects.get(id=int(nvend))
            ca = category.objects.get(id=int(ncat))
            sca = Sub_category.objects.get(id=int(nscat))
            
            tz= pytz.timezone('Asia/Kolkata')
            time_now = datetime.datetime.now(timezone.utc).astimezone(tz)
            millis = int(time.mktime(time_now.timetuple()))
            order_id = "Order"+str(millis)
            
            co = Custome_Order()
            co.cate = ca
            co.sub_cate = sca
            co.U_id = valid
            co.V_id = nv
            co.Order_data = order_id
            co.details = ndetail
            co.docs = ndocs
            co.status = "Pending"
            co.save()
            return redirect('Custome_Order_Form')
        return render(request,'Custome_Order.html',{'vend':vend,'prod':prods,'user_data':valid,'nav_cat':nav_cat,'nav_scat':nav_scat})
    else:
        return redirect('login')
    
def cancel_Custorder(request,id):
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(id=int(em))
        prods = Custome_Order.objects.get(id=id)
        prods.status = "Cancel"
        prods.save()
        return redirect('Custome_Order_Form')
    else:
        return redirect('login')

def unsb_data(request,id):
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(id=int(em))
        ven = vendor.objects.get(id=int(id))
        sb = subscribe_data.objects.get(usersData=valid,vendors=ven)
        sb.delete()
        return redirect('Shop_View',id)
    else:
        return redirect('login')
# ===============================================================Vender Side====================================\

def Vender_Regis(request):
    if request.POST:
        obj = vendor()
        obj.v_name = request.POST['username']
        em = request.POST['email']
        try:
            valid = vendor.objects.get(email_id=em)
            messages.error(request, 'User Id Already In Use...')
            return render(request,'Admin_templates/Regi.html')
        except:
            obj.email_id = em
        obj.contact = request.POST['phoneno']
        obj.password = request.POST['pass']
        obj.save()
        return redirect('ved_login')
    return render(request,'Admin_templates/Regi.html')

def Vender_Login(request):
    if request.POST:
        em = request.POST['username']
        pas = request.POST['pass']
        try:
            valid = vendor.objects.get(email_id=em)
            if valid.password == pas:
                request.session['vender_data'] = valid.email_id
                if valid.Shop_name == "" and valid.shop_img == "":
                    return redirect('vendor_form')
                else:
                    return redirect('Vender_Dashboard')
            else:
                messages.error(request, 'Wrong Password...')
                return render(request,'Admin_templates/Login.html')
        except:
            messages.error(request, 'Wrong Email Id...')
            return render(request,'Admin_templates/Login.html')
    return render(request,'Admin_templates/Login.html')


# Forget Password -----------------

def Shop_forgot_pass(request):
    if request.POST:
        email1 = request.POST['email']
        number1 = request.POST['m_no']
            
        try:
            valid = vendor.objects.get(email_id=email1)
            if int(valid.contact) == int(number1):
                print(email1)
                request.session['useremail'] = email1
                
                numbers = [1,2,3,4,5,6,7,8,9,0]
                num = ""
                for i in range(4):
                    num += str(random.choice(numbers))
                
                num = int(num)
                print(num)
                
                # ============== Email ==============
                
                sender_email = "harshilsoni011@gmail.com"
                sender_pass = "Harshil123$"
                receiver_email = email1

                server = smtplib.SMTP('smtp.gmail.com',587)

                your_message = "This Is Your OTP Number = "+str(num)

                print(your_message)

                msg = email.message.Message()
                msg['Subject'] = "Your OTP"
                msg['From'] = sender_email
                msg['To'] = receiver_email
                password = sender_pass
                msg.add_header('Content-Type','text/html')
                msg.set_payload(your_message)

                server.starttls()
                server.login(msg['From'],password)
                server.sendmail(msg['From'],msg['To'],msg.as_string())
                
                # ============== End Email ===========
                
                request.session['otp'] = num
                
                return render(request,'Admin_templates/OTP.html',{'otp':num})
                                    
            else:
                return HttpResponse("<h2><a href=''>Mobile Number Is Not Registered</a></h2>")
                return redirect('Shop_forgotpass')
        except:
            return HttpResponse("<h2><a href=''>Email Is Not Registered</a></h2>")
            return redirect('shop_forgotpass')
        
    return render(request,'Admin_templates/Forget_Pass.html')

def Shop_otpcheck(request):
    if request.session.has_key('otp'):
        if request.POST:
            otp = request.POST['otp']
            if int(request.session['otp']) == int(otp):
                del request.session['otp']
                return redirect('Shop_newpassword')
            else:
                return HttpResponse("<h2><a href=""> You Have Entered Wrong OTP </a></h2>")
        else:
            return redirect('shop_forgotpass')
    return redirect('ved_login')

def Shop_newpassword(request):
    if request.session.has_key('useremail'):
        if request.POST:
            pass_1 = request.POST['pass1']
            pass_2 = request.POST['pass2']
            
            if pass_1 == pass_2:
                valid = vendor.objects.get(email_id=request.session['useremail'])
                valid.password = pass_2
                valid.save()
                del request.session['useremail']
                return redirect('ved_login')
            else:
                return HttpResponse("<h2><a href=''>Passwords Are Not Same ...</a></h2>")
        return render(request,'Admin_templates/New_Pass.html')
    return redirect('ved_login')

# Forget Password -----------------

def Vender_Logout(request):
    if 'vender_data' in request.session.keys():
        del request.session['vender_data']
        return redirect('ved_login')
    else:
        return redirect('ved_login')

def Vender_Dashboard(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        prods = Custome_Order.objects.filter(V_id = vender_data)
        cate = category.objects.all()
        sub_cate = Sub_category.objects.all()
        try:
            q = request.GET.get('search')
        except:
            q = None
        if q:
            prod= product.objects.filter(Q(p_name__icontains=q) | Q(p_discription__icontains=q) | Q(p_price__icontains=q))
            
            data = {
                'pro' : prod,
                'vdata':vender_data,
                'cate' : cate,
                "prods":prods,
            }
        else:
            data={'vdata':vender_data,'cate' : cate,"prods":prods,}
            
        # return render(request,'index.html',data)
        return render(request,'Admin_templates/index.html',data)
    else:
        return redirect('ved_login')        

def Owner_Chats(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        mci = ModelChat_IDs.objects.filter(vendors=vender_data)
        return render(request,'Admin_templates/OwnerChats.html',{'mci':mci,'vdata':vender_data})
    else:
        return redirect('ved_login')     

def Vender_Cust_Chat(request,id):
    if 'vender_data' in request.session.keys():
        venders = vendor.objects.get(email_id=request.session['vender_data'])
        try:  
            moch = ModelChat_IDs.objects.get(id=id)
            print(moch.chat_id)
            mode_ch = Models_Chats.objects.filter(ch_ids=moch)
            print(mode_ch)
            if request.POST:
                ptext = request.POST['ptext']
                
                obj = Models_Chats()
                obj.ch_ids=moch
                obj.vendors = venders
                obj.problem_text = ptext
                obj.save()    
                return redirect('Vender_Cust_Chat',id)
            return render(request,'Admin_templates/Chat_Data_Show.html',{'vdata':venders,'mc':mode_ch,'moch':moch})
        except:
            return redirect('Vender_Dashboard')
    else:
        return redirect('ved_login')     


def Customer_Orders_View(request):
    if 'vender_data' in request.session.keys():
        venders = vendor.objects.get(email_id=request.session['vender_data'])
        prods = Custome_Order.objects.filter(V_id = venders)
        return render(request,'Admin_templates/View_Cutom_Orders.html',{'vdata':venders,'prod':prods})
    else:
        return redirect('ved_login')   

def view_custom_data(request,id):
    if 'vender_data' in request.session.keys():
        venders = vendor.objects.get(email_id=request.session['vender_data'])
        prods = Custome_Order.objects.get(id = id)
        if request.POST:
            ncheck = request.POST.get('ncheck')
            namount = request.POST.get('namount')
            print(ncheck)
            if ncheck == "on" and namount != None:
                prods.status = "Accept"
                prods.price = namount
                prods.save()
                return redirect('Customer_Orders_View')
        return render(request,'Admin_templates/Cutom_view_Orders.html',{'vdata':venders,'prod':prods})
    else:
        return redirect('ved_login') 

def vendor_form(request): 
    if "vender_data" in request.session.keys():
        obj = vendor.objects.get(email_id=str(request.session['vender_data']))
        if request.POST:
            vnm = request.POST['vnm']
            vem = request.POST['vem']
            vpass = request.POST['vpass']
            vcon = request.POST['vcon']
            vimg = request.FILES.get('vimg')
            shimg = request.FILES.get('shimg')
            shnm = request.POST['shnm']
            shem = request.POST['shem']
            shcon = request.POST['shcon']
            shadd = request.POST['shadd']
            
            obj.v_name = vnm
            obj.email_id = vem
            request.session['vender_data'] = vem
            obj.password = vpass
            obj.contact = vcon
            if vimg != None:
                obj.profile = vimg
            if shimg != None:
                obj.shop_img = shimg
            obj.Shop_name = shnm
            obj.shop_address = shadd
            obj.shop_contact_no = shcon
            obj.shop_contact_em = shem
            obj.save()
            return redirect('Vender_Dashboard')
        return render(request,'Admin_templates/vendor_form.html',{'vdata':obj})
    else:
        return redirect('ved_login')   

def product_form(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        prods = product.objects.filter(venders=vender_data)
        
        return render(request,'Admin_templates/product_form.html',{'prods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login') 

def ven_product_form(request,id):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        sc = Sub_category.objects.get(id=id)
        prods = product.objects.filter(venders=vender_data,sub_cate=sc)
        
        return render(request,'Admin_templates/product_form.html',{'venprods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login') 

def Add_product_form(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        cats = category.objects.all()
        prods = Sub_category.objects.all()
        if request.POST:
            pnm = request.POST['pnm']
            pdis = request.POST['pdis']
            pprice = request.POST['pprice']
            psize = request.POST['psize']
            psk = request.POST['psk']
            img = request.FILES.get('img')
            scats = request.POST['scats']
            cat = request.POST['cats']
            
            C_id = category.objects.get(id=int(cat))
            scates = Sub_category.objects.get(id=int(scats))
            
            obj = product()
            obj.venders = vender_data
            obj.cate = C_id
            obj.sub_cate = scates
            obj.p_name = pnm
            obj.p_discription = pdis
            obj.p_price = pprice
            
            obj.size_id = psize
            obj.stock = psk
            obj.imgs = img
            obj.save()
            return redirect('product_form')
        return render(request,'Admin_templates/add_product_form.html',{'cats':cats,'prods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login')  
    
def Update_product_form(request,id):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        cats = category.objects.all()
        prods = Sub_category.objects.all()
        obj = product.objects.get(id=id)
        if request.POST:
            pnm = request.POST['pnm']
            pdis = request.POST['pdis']
            pprice = request.POST['pprice']
            psize = request.POST['psize']
            psk = request.POST['psk']
            img = request.FILES.get('img')
            scats = request.POST['scats']
            cat = request.POST['cats']
            
            C_id = category.objects.get(id=int(cat))
            scates = Sub_category.objects.get(id=int(scats))
            
            obj.venders = vender_data
            obj.cate = C_id
            obj.sub_cate = scates
            obj.p_name = pnm
            obj.p_discription = pdis
            obj.p_price = pprice
            
            obj.size_id = psize
            obj.stock = psk
            if img != None:
                obj.imgs = img
            obj.save()
            return redirect('product_form')
        return render(request,'Admin_templates/add_product_form.html',{'cats':cats,'keys':obj,'prods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login')  

def Delete_product_form(request,id):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        obj = product.objects.get(id=id)
        obj.delete() 
        return redirect('product_form')
        return render(request,'Admin_templates/add_product_form.html',{'vdata':vender_data})
    else:
        return redirect('ved_login')  
    

def Report_Data(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        oot = owner_order_table.objects.filter(owner=vender_data)
        
        return render(request,'Admin_templates/report.html',{'oot':oot,'vdata':vender_data})
    else:
        return redirect('ved_login')

def order_item_form(request):
    if "vender_data" in request.session.keys():
        Users = vendor.objects.get(email_id=request.session['vender_data'])
        otdata = owner_order_table.objects.filter(owner=Users)
        rec = set()
        for i in otdata:
            rec.add(i.order_id)
        rec = list(rec)
        rec.sort()
        return render(request,'Admin_templates/order_item_form.html',{'oids':rec,'vdata':Users})
    else:
        return redirect('ved_login') 

def VenderView_specific(request,Orids):
    if "vender_data" in request.session.keys():
        Users = vendor.objects.get(email_id=request.session['vender_data'])
        otdata = owner_order_table.objects.filter(owner=Users,order_id=Orids)
        status = ""
        for i in otdata:
            if i.cancel == True and i.deliver != True:
                status = "Canceled"
        
        tots = 0
        stats = set()
        orid = ''
        for i in otdata:
            orid = i.order_id
            stats.add(i.deliver)
            tots += float(i.total)
        stats = list(stats)
        stats = stats[0]
        keys = False
        if stats == True:
            keys = True
        if request.POST:
            ids = request.POST['ids']
            stat = request.POST['stat']
            if stat == "Deliver":
                # obj = owner_order_table.objects.filter(order_id=Orids)
                for i in otdata:
                    i.deliver = True
                    i.payment = True
                    i.save()
                oids = order_table.objects.filter(order_id=Orids)
                for i in oids:
                    i.deliver = True
                    i.payment = True
                    i.save()
                keys = True
        try:
            objs_data = Address.objects.get(order_id=orid)
        except:
            objs_data = "no"
        return render(request,'Admin_templates/VenderBillPage.html',{'adds':objs_data,'status':status,'keys':keys,'vdata':Users,'bilam':tots,'orders':otdata,'oids':Orids})
    else:
        return redirect('ved_login') 


def feedback_form(request):
    if "vender_data" in request.session.keys():
        Users = vendor.objects.get(email_id=request.session['vender_data'])
        if  request.POST:
            fmess =request.POST['fmess']
            fdate = request.POST['fdate']
            
            obj = feedback()
            obj.f_messge = fmess
            obj.f_date = fdate
            obj.save()
            return redirect('feedback_form')
        return render(request,'Admin_templates/feedback_form.html',{'vdata':Users})
    else:
        return redirect('ved_login') 

def message_task(request):
    return render(request,'Admin_templates/message-task.html')

    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def Shop_PDF(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        oot = owner_order_table.objects.filter(owner=vender_data)
        data = {'oot':oot,'vdata':vender_data}
        pdf = render_to_pdf('Admin_templates/GeneratePdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return redirect('ved_login')

def Shop_Excel(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        oot = owner_order_table.objects.filter(owner=vender_data)    
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ReportData.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Customer', 'OrderId', 'Date',  'Products', 'QTY','Price', 'Total', 'payment', 'deliver', 'cancel']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = owner_order_table.objects.filter(owner=vender_data).values_list('cust__u_name', 'order_id', 'date', 'product', 'qty', 'price','total','payment','deliver','cancel')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)

        return response
        
    
    else:
        return redirect('ved_login')

