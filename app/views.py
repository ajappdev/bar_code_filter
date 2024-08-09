# DJANGO DECLARATIONS
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

# GENERAL DECLARATIONS
import json
from datetime import date, datetime
import pandas as pd
from io import BytesIO
from os import path
import os

# APP DECLARATIONS
import app.models as am
import app.m00_common as m00
import app.m01_product as m01
import app.decorators as ad


def search_product(request):
    if request.user.id:
        if request.user.user_profile.role == "Administrator":
            am.UserProfile.objects.filter(user=request.user).update(
                last_login=datetime.now())
            am.LogingLog.objects.create(
                user=request.user, time=datetime.now())
            return redirect("administrator/products/")

    page_title = "Rechercher produit"
    template = "search.html"
    context = {"page_title": page_title}

    return render(request, template, context)


def about(request):
    page_title = "About"
    template = "landing/about.html"
    context = {"page_title": page_title}
    return render(request, template, context)


def privacy_policy(request):

    page_title = "Privacy policy"
    template = "landing/privacy-policy.html"
    context = {"page_title": page_title,}
    return render(request, template, context)


def terms_and_conditions(request):

    page_title = "Terms and conditions"
    template = "landing/terms-and-conditions.html"
    context = {"page_title": page_title,}
    return render(request, template, context)


def cookies_policy(request):

    page_title = "Cookies policy"
    template = "landing/cookies-policy.html"
    context = {"page_title": page_title,}
    return render(request, template, context)


@login_required(login_url='login/')
@ad.admin_required
def bulk_upload_products(request):

    template = 'administrator/bulk-upload-products.html'
    context = {
        }
    return render(request, template, context)


@csrf_exempt
@ad.admin_required
def upload_products_file(request):
    if request.method == 'POST':
        files = request.FILES.getlist("0")

        for f in files:
            fs = FileSystemStorage(path.join(
                settings.MEDIA_ROOT))
            filename = fs.save(request.POST['key'] + ".xlsx", f)

        file_path = os.path.join(
            settings.MEDIA_ROOT, request.POST['key'] + ".xlsx")
        
        error_upload = m01.check_bulk_upload(file_path)

        if error_upload == "":
            treatment_result = m01.bulk_upload(file_path)
            success_products = treatment_result.loc[
                (treatment_result['error'] == ''), 'Code_barres'].count()
            failed_products = treatment_result.loc[
                (treatment_result['error'] != ''), 'Code_barres'].count()

            produits_traites = failed_products + success_products
            html = render_to_string(
                template_name="administrator/widgets/bulk-treatment.html",
                context={
                    "treatment_result": treatment_result,
                    "produits_traites": produits_traites,
                    "success_products": success_products,
                    "failed_products": failed_products,      
                }
            )
            data_dict = {"error": "", "html": html}
        else:
            data_dict = {"error": error_upload} 

        if os.path.exists(file_path):
            os.remove(file_path)

        return JsonResponse(data=data_dict, safe=False)


@login_required(login_url='login/')
@ad.admin_required
def download_excel_template(request):
    df = pd.DataFrame(columns=[
            'Code_barres',
            'Nom_produit',
            'Lien'])
    with BytesIO() as b:
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index = False)
        writer.close()
        # Set up the Http response.
        filename = 'modele_produits.xlsx'
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response



@login_required(login_url='/auth/login/')
@ad.admin_required
def products(request):

    page_title = "Produits"
    
    template = 'administrator/products.html'
    context = {
        "page_title": page_title,
        }
    
    return render(request, template, context)


def ajax_calls(request):

    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        function = received_json_data['function']

        if function == "filter_products_list":
            product_name = received_json_data['product_name']
            product_barcode = received_json_data['product_barcode']
            page = received_json_data['page']

            products = am.Product.objects.filter(
                name__icontains=product_name,
                barcode__icontains=product_barcode
            )

            length_result = len(products)
            products_list = m00.pagination(page, 10, products)

            html = render_to_string(
                        template_name="administrator/widgets/products-table.html", 
                        context={
                            "products": products_list,
                            "length_result": length_result,
                        }
                    )
            data_dict = {"html": html}

        elif function == "get_form_add_update_product":
            
            product_id = int(received_json_data['product_id'])
            if product_id > 0:
                modal_title = _("Modifier produit")
                product = am.Product.objects.get(id=product_id)
            else:
                modal_title = _("Ajouter produit")
                product = None

            
            html = render_to_string(
                        template_name="administrator/widgets/create-update-product.html", 
                        context={
                            "product": product,
                            "modal_title": modal_title,
                        }
                    )
            data_dict = {"html": html}


        elif function == "search_barcode":
            
            barcode = received_json_data['barcode']

            exists = 0
            link = ""

            if len(barcode) > 100:
                exists = 0

            elif am.Product.objects.filter(barcode=barcode).exists():
                exists = 1
                link = am.Product.objects.filter(barcode=barcode)[0].link

            data_dict = {"exists": exists, "link": link}


        elif function == "delete_product":
            error = 0
            error_text = ""
            try:
                am.Product.objects.filter(
                    id=int(received_json_data['product_id'])).delete()
            except Exception as e:
                error_text = "EXCEPTION, AJAX_CALLS, delete_product, 1, " + str(e)
                error = 1
            data_dict = {"error": error, "error_text": error_text}


        elif function == "create_update_product":

            error = ""

            try:
                product_name = received_json_data['product_name']
                product_barcode = received_json_data['product_barcode']
                product_link = received_json_data['product_link']
                product_id = int(received_json_data['product_id'])

                if product_id > 0:
                    product = am.Product.objects.get(id=product_id)
                    if am.Product.objects.filter(~Q(id=product_id), barcode=product_barcode).exists():
                        error = "Un produit avec le même code-barres existe déjà !"
                else:
                    product = am.Product()
                    if am.Product.objects.filter(barcode=product_barcode).exists():
                        error = "Un produit avec le même code-barres existe déjà !"

                if m00.is_hyperlink(product_link) is False:
                    error = "Le lien du produit n'est pas valide !"

                if error == "":
                    product.name = product_name
                    product.barcode = product_barcode
                    product.link = product_link
                    product.save()

            except Exception as e:
                error = e

            data_dict = {"error": error}


        elif function == "get_link_product":
            error = 0
            error_text = ""
            link = ""
            try:
                link = am.Product.objects.get(
                    id=int(received_json_data['product_id'])).link
            except Exception as e:
                error_text = "EXCEPTION, AJAX_CALLS, get_link_product, 1, " + str(e)
                error = 1
            data_dict = {"link": link, "error": error, "error_text": error_text}

        return JsonResponse(data=data_dict, safe=False)