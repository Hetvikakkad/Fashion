from django.db import models

# Create your models here.
class Area(models.Model):
    name =  models.CharField(default="",max_length=30)
    Pincode = models.CharField(default="",max_length=20)
    
    def __str__(self):
        return self.name

class UsersData(models.Model):
    area = models.ForeignKey("Area",on_delete=models.CASCADE,blank=True,null=True)
    u_id = models.PositiveIntegerField(default=0,null=False)
    u_name = models.CharField(default="",max_length=30,null=False)
    email_id = models.CharField(default="",max_length=30,null=False)
    password = models.CharField(default="",max_length=20,null=False)
    contact = models.PositiveIntegerField(default=0,null=False)
    state = models.CharField(default="",max_length=15,null=False)
    country = models.CharField(default="", max_length=15, null=False)
    city = models.CharField(default="", max_length=15, null=False)
    pincode = models.CharField(default="", max_length=15, null=False)
    address = models.TextField(default="")
    profile = models.ImageField(default="", upload_to="UserProfile/", max_length=400,blank=True,null=True)
    
    def __str__(self):
        return self.u_name

class vendor(models.Model):
    v_name = models.CharField(default="", max_length=30, null=False)
    v_gstno = models.CharField(default="",blank=True, null=True,max_length=100)
    email_id = models.CharField(default="", max_length=30, null=False)
    password = models.CharField(default="", max_length=20, null=False)
    contact = models.PositiveIntegerField(default=0, null=False)
    profile = models.ImageField(default="", upload_to="VenderProfile/", max_length=400,blank=True,null=True)
    shop_img = models.ImageField(default="", upload_to="VenderProfile/", max_length=400,blank=True,null=True)
    Shop_name = models.CharField(default="", max_length=100, null=False)
    shop_address = models.TextField(default="")
    shop_contact_no = models.CharField(default="", max_length=30, null=False)
    shop_contact_em = models.CharField(default="", max_length=30, null=False)

    def __str__(self):
        return self.v_name

class subscribe_data(models.Model):
    usersData = models.ForeignKey("UsersData", default="",on_delete=models.CASCADE,blank=True, null=True)
    vendors = models.ForeignKey("vendor", default="",on_delete=models.CASCADE,blank=True, null=True)

class ModelChat_IDs(models.Model):
    chat_id = models.CharField(default="", max_length=100, null=False)
    usersData = models.ForeignKey("UsersData", default="",on_delete=models.CASCADE,blank=True, null=True)
    vendors = models.ForeignKey("vendor", default="",on_delete=models.CASCADE,blank=True, null=True)

class Models_Chats(models.Model):
    ch_ids = models.ForeignKey("ModelChat_IDs", default="",on_delete=models.CASCADE,blank=True, null=True)
    usersData = models.ForeignKey("UsersData", default="",on_delete=models.CASCADE,blank=True, null=True)
    vendors = models.ForeignKey("vendor", default="",on_delete=models.CASCADE,blank=True, null=True)
    problem_text = models.TextField(default="")
    date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    

class order_table(models.Model):
    cust = models.ForeignKey("UsersData", on_delete=models.CASCADE)
    order_id = models.CharField(default='',max_length=100) 
    date = models.DateTimeField(auto_now=False,blank=True, null=True)
    img = models.ImageField(upload_to="orders/",default='')
    product = models.CharField(default='',max_length=300)
    qty = models.CharField(default='',max_length=100)
    price = models.CharField(default='',max_length=100)
    total = models.CharField(default='',max_length=100)
    payment = models.BooleanField(default=False)
    deliver = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)

    def __str__(self):
        return self.product

class Address(models.Model):
    order_id = models.CharField(default='',max_length=100) 
    strAdd = models.CharField(max_length=100,default="")
    Add = models.CharField(max_length=100,default="")
    city = models.CharField(max_length=100,default="")
    state = models.CharField(max_length=100,default="")
    zip1 = models.CharField(max_length=100,default="")
    
    def __str__(self):
        return self.order_id

class owner_order_table(models.Model):
    owner = models.ForeignKey("vendor", on_delete=models.CASCADE)
    cust = models.ForeignKey("UsersData", on_delete=models.CASCADE)
    order_id = models.CharField(default='',max_length=100) 
    date = models.DateTimeField(auto_now=False,blank=True, null=True)
    product = models.CharField(default='',max_length=300)
    qty = models.CharField(default='',max_length=100)
    price = models.CharField(default='',max_length=100)
    total = models.CharField(default='',max_length=100)
    payment = models.BooleanField(default=False)
    deliver = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product

class Owner_Payment(models.Model):
    Owner = models.ForeignKey("vendor", on_delete=models.CASCADE)
    Order_id = models.CharField(default='',max_length=100) 
    date = models.DateTimeField(auto_now=False,blank=True, null=True)
    Order_amount = models.CharField(default='',max_length=100)
    
    def __str__(self):
        return self.Order_id

class category(models.Model):
    c_name = models.CharField(default="", max_length=30, null=False)
    c_image = models.ImageField(default="", upload_to="Product_Cat/", max_length=400,blank=True,null=True)

    def __str__(self):
        return self.c_name

class Sub_category(models.Model):
    name = models.CharField(default="",max_length=20)
    Sc_image = models.ImageField(default="", upload_to="Product_sub_cat", max_length=400,blank=True,null=True)

    def __str__(self):
        return self.name
            
class product(models.Model):
    venders = models.ForeignKey("vendor", on_delete=models.CASCADE,blank=True, null=True)
    cate = models.ForeignKey("category", on_delete=models.CASCADE,blank=True, null=True)
    sub_cate = models.ForeignKey("Sub_category", on_delete=models.CASCADE,blank=True, null=True)
    p_name = models.CharField(default="", max_length=30, null=False)
    p_discription = models.TextField(default="")
    p_price = models.PositiveIntegerField(default=0, null=False)
    
    size_id = models.PositiveIntegerField(default=0, null=False)
    stock = models.PositiveIntegerField(default=0,  null=False)
    imgs = models.ImageField(upload_to="Product_imgs/",default="", max_length=400,blank=True,null=True)

    @staticmethod
    def get_products_by_id(ids):
        return product.objects.filter(id__in = ids)
    
    def __str__(self):
        return self.p_name


class feedbacks_of_product(models.Model):
    Product_name = models.ForeignKey("product", on_delete=models.CASCADE)
    cust = models.ForeignKey("UsersData", on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    rating = models.CharField(max_length=20,default = '1')
    feedback = models.TextField()

    def __str__(self):
        return self.cust.u_name


class Offer(models.Model):
    venders = models.ForeignKey("vendor", on_delete=models.CASCADE,blank=True, null=True)
    Start_date = models.DateField(auto_now=False,blank=True,null=True)
    End_date = models.DateField(auto_now=False,blank=True,null=True)
    P_id = models.ForeignKey("product",on_delete=models.CASCADE,blank=True,null=True)
    descr = models.CharField(default="",max_length=200)


class Cart(models.Model):
    U_id = models.ForeignKey("UsersData",on_delete=models.CASCADE,blank=True,null=True)
    P_id = models.TextField(default="",blank=True, null=True)



class Order(models.Model):
    U_id = models.ForeignKey("UsersData",on_delete=models.CASCADE,blank=True,null=True)
    V_id = models.ForeignKey("vendor",on_delete=models.CASCADE,blank=True,null=True)
    Order_date = models.DateField(auto_now=False,blank=True,null=True)
    Contact_no = models.IntegerField(default=0)       


class Wishlist(models.Model):
    U_id = models.ForeignKey("UsersData",on_delete=models.CASCADE,blank=True,null=True)
    P_id = models.ForeignKey("product",on_delete=models.CASCADE,blank=True,null=True)


class Orderitem(models.Model):
    P_id = models.ForeignKey("product",on_delete=models.CASCADE,blank=True,null=True)
    Quantity = models.CharField(default="",max_length=100)
    Amount = models.CharField(default="",max_length=100)



class feedback(models.Model):
    U_id = models.ForeignKey("UsersData",on_delete=models.CASCADE,blank=True,null=True)
    P_id =models.ForeignKey("product",on_delete=models.CASCADE,blank=True,null=True)
    f_id = models.CharField(default="",max_length=100)
    f_date = models.DateField(auto_now=False,blank=True,null=True) 
    f_messge =  models.TextField(default="",max_length=400)
    
    def __str__(self):
	    return self.U_id.u_name



class Payment(models.Model):
    U_id =models.ForeignKey("UsersData",on_delete=models.CASCADE,blank=True,null=True)
    V_id =models.ForeignKey("vendor",on_delete=models.CASCADE,blank=True,null=True)
    P_mode =models.CharField(default="",max_length=100)
    p_date =models.DateField(auto_now=True,blank=True,null=True)
    P_amount =models.CharField(default="",max_length=20)


class Custome_Order(models.Model):
    cate = models.ForeignKey("category", on_delete=models.CASCADE,blank=True, null=True)
    sub_cate = models.ForeignKey("Sub_category", on_delete=models.CASCADE,blank=True, null=True)
    U_id =models.ForeignKey("UsersData",on_delete=models.CASCADE,blank=True,null=True)
    V_id =models.ForeignKey("vendor",on_delete=models.CASCADE,blank=True,null=True) 
    price = models.CharField(default='',max_length=200)
    qty = models.CharField(default='',max_length=200)
    status = models.CharField(default='',max_length=200)
    pay = models.BooleanField(default=False)
    details = models.TextField(default="")
    date = models.DateField(auto_now=True,blank=True,null=True)
    Order_data = models.CharField(default='',max_length=200)
    docs = models.FileField(upload_to="Cust_docs/",default="",max_length=500,blank=True, null=True)
    
    def __str__(self):
	    return self.U_id.u_name