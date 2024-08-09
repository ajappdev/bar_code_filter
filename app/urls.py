# DJANGO DECLARATIONS
from django.urls import path, include

# APP DECLARATIONS
import app.views as av

# GENERAL DECLARATIONS

urlpatterns = [
    ############################## UNCLASSED PAGES ############################
    path('about/', av.about, name='about'),
    path('privacy-policy/', av.privacy_policy, name='privacy_policy'),
    path('cookies-policy/', av.cookies_policy, name='cookies_policy'),
    path('terms-and-conditions/', av.terms_and_conditions, name='terms_and_conditions'),
    path('download-excel-template/', av.download_excel_template, name='download_excel_template'),
    path('administrator/bulk-upload-products/', av.bulk_upload_products, name='bulk_upload_products'),
    ######################### ADMIN PAGES #####################################
    path('administrator/products/', av.products, name='products'),
    ######################### USER PAGES ###################################
    path('', av.search_product, name='search_product'),
    ######################### AJAX PAGES ######################################
    path('ajax-calls/', av.ajax_calls, name='ajax_calls'),
    path('administrator/upload-products-file/', av.upload_products_file, name='upload_products_file'),
]


urlpatterns += [
    path('auth/', include('django.contrib.auth.urls')),
]