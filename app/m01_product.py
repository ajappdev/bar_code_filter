import pandas as pd
import numpy as np
import app.models as am
import app.m00_common as m00

def check_bulk_upload(file_path: str):
    
    error_return = ""
    try:
        dfs = pd.read_excel(file_path)
    except Exception as e:
        error_return = "Impossible de lire le fichier: " + str(e)
        return error_return
    # Check if the file contains the right columns
    if dfs.columns.tolist() != [
            'Code_barres',
            'Nom_produit',
            'Lien']:
        error_return = "Mauvais fichier de produits !"
    elif len(dfs) == 0:
        error_return = "Le fichier de produits est vide !"
    return error_return


def check_product(
        product_name: str,
        product_barcode: str,
        product_link: str):

    error_return = ""

    # Check if the question was provided
    if product_barcode == "":
        error_return = "Le produit ne peut pas avoir un code à barres vide !"

    # Check if the answer was provided
    elif product_link == "":
        error_return = "Le produit ne peut pas avoir un lien vide !"

    elif m00.is_hyperlink(product_link) is False:
        error_return = "Le lien du produit n'est pas valide !"

    return error_return


def create_product(
        product_name: str,
        product_barcode: str,
        product_link: str
    ):

    check = check_product(
        product_name,
        product_barcode,
        product_link)

    if check == "":

        if len(am.Product.objects.filter(barcode=product_barcode)) > 0:
            new_product = am.Product.objects.filter(barcode=product_barcode)[0]
        else:
            new_product = am.Product()
        
        new_product.name = product_name
        new_product.link = product_link
        new_product.barcode = product_barcode
        new_product.save()

        return ""
    
    else:
        return check


def bulk_upload(file_path: str):
    dfs = pd.read_excel(file_path)
    dfs = dfs.replace(np.nan, "")

    dfs['error'] = ""
    def treat_product(
                product_name,
                product_barcode,
                product_link):

        error_message = ""

        try: 
            error_message = create_product(
                product_name,
                product_barcode,
                product_link,
            )
        except Exception as e:
            error_message = e

        return error_message

    dfs["error"] = dfs.apply(
        lambda x: treat_product(
                x.Nom_produit,
                x.Code_barres,
                x.Lien,
            ), axis=1)

    return dfs