from django.urls import path
from .views import Index,blog,Contact,Show_Product,Product,Product_details,about,form,message_task,login,Shop_View,cat_view,show_prods

from . import views as v

urlpatterns = [
        path('Login',login, name='login'),
        path('register/',v.register, name='register'),
        path('orders/',v.Orders.as_view(),name='orders'),
        path('cart_orders',v.cart_order,name='cart_order'),
        path('',Index,name='home'),
        path('Shop_View/<int:id>',Shop_View,name='Shop_View'),
        path('cat_view/<int:id>',cat_view,name='cat_view'),
        path('show_prods/<int:jid>/<int:iid>/<int:oid>',show_prods,name='show_prods'),
        path('show_all_prods/<int:jid>/<int:iid>',v.show_all_prods,name='show_all_prods'),
        path('Show_Product/<int:id>',Show_Product,name='Show_Product'),
        path('Chat_Data_Show/<int:id>',v.Chat_Data_Show,name='Chat_Data_Show'),
        path('blog/',blog,name='blog'),
        path('View_Bill/<str:Orids>',v.View_specific,name='View_specific'),
        path('Cust_Orders/',v.Customer_Orders,name='cusorders'),
        path("COD/",v.COD_Data,name='COD'),
        path('Cust_Logout/',v.Cust_Logout,name='Cust_Logout'),
        path('Profile/',v.Profile,name='Profile'),
        path('Cust_Chats/',v.Cust_Chats,name='Cust_Chats'),
        path('Wish_List/',v.Wish_List,name="Wish_List"),
        path('SubScribeData/',v.SubScribeData,name="SubScribeData"),
        path('Add_Wish_List/<int:id>/',v.Add_Wish_List,name='Add_Wish_List'),
        path('remove_wishlist/<int:id>',v.remove_wishlist,name='remove_wishlist'),
        path('Contact/',Contact,name='contact'),
        path('product/',Product,name='product'),
        path('Product_details/',Product_details,name='product_details'),
        path('about/',about,name='about'),
        path('cancel_data/<str:Orids>',v.cancel_data,name='cancel_data'),
        path('ViewSpecify_Bill/<str:Orids>',v.ViewSpecify_Bill,name='ViewSpecify_Bill'),
        path('form/',form,name='form'),
        path('Custome_Order',v.Custome_Order_Form,name='Custome_Order_Form'),
        path('cancel_Custorder/<int:id>',v.cancel_Custorder,name='cancel_Custorder'),
        path('unsb_data/<int:id>',v.unsb_data,name='unsb_data'),
        # Forget Password -----------
        path('forgotpass/',v.forgot_pass,name = 'forgotpass'),
        path('otpcheck/',v.otpcheck, name = 'otpcheck'),
        path('newpassword/',v.newpassword, name = 'newpassword'),
        # Forget Password -----------

        # payment -----------------
        path('cust_check/<int:id>',v.Cust_Checkout,name='cust_check'),
        path('cust_process_payment/',v.cust_Process_payment,name='cust_process_payment'),
        path('Update_Cust/',v.Update_Cust,name='Update_Cust'),
        path("cust_handlerequest/",v.cust_Handlerequest, name="cust_handlerequest"),

        # payment -----------------
        path('check/',v.Checkout,name='check'),
        path('payment_process/',v.Process_payment,name='process_payment'),
        path('EmailCall/',v.EmailCall,name='emailcall'),
        path("handlerequest/",v.Handlerequest, name="handlerequest"),
        # ========================================== Vender Side =======================
        path('Vender_Login/',v.Vender_Login,name="ved_login"),
        path('Vender_Regis/',v.Vender_Regis,name="ved_regi"),
        path('Vender_Dashboard/',v.Vender_Dashboard,name='Vender_Dashboard'),
        path('product_form/',v.product_form,name='product_form'),
        path('ven_product_form/<int:id>/',v.ven_product_form,name='ven_product_form'),
        path('Vender_Cust_Chat/<int:id>',v.Vender_Cust_Chat,name='Vender_Cust_Chat'),
        path('Add_product_form/',v.Add_product_form,name='Add_product_form'),
        path('Update_product_form/<int:id>',v.Update_product_form,name='Update_product_form'),
        path('Delete_product_form/<int:id>',v.Delete_product_form,name='Delete_product_form'),
        path('vendor_form/',v.vendor_form,name='vendor_form'),
        path('Owner_Chats/',v.Owner_Chats,name='Owner_Chats'),
        path('Customer_Orders_View',v.Customer_Orders_View,name='Customer_Orders_View'),
        path('view_custom_data/<int:id>',v.view_custom_data,name='view_custom_data'),
        path('order_item/',v.order_item_form, name='order_item_form'),
        path('feedback_form/',v.feedback_form, name='feedback_form'),
        path('Report_Data/',v.Report_Data,name='Report_Data'),
        path('Vender_View_Bills/<str:Orids>',v.VenderView_specific,name='VenderView_specific'),
        path('vender_logout/',v.Vender_Logout,name='vender_logout'),
        # Forget Password -----------
        path('Shop_forgotpass/',v.Shop_forgot_pass,name = 'Shop_forgotpass'),
        path('Shop_otpcheck/',v.Shop_otpcheck, name = 'Shop_otpcheck'),
        path('Shop_newpassword/',v.Shop_newpassword, name = 'Shop_newpassword'),
        # Forget Password -----------
        #------------------------------------------------------------------------
        path('message_task/',message_task, name='message_task'),
        path('PDFS/',v.Shop_PDF,name='PDFs'),
        path('Excels/',v.Shop_Excel,name='Excels'),
]