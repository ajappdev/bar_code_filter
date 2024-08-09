# Product Management Web Application

## Overview

This Django-based web application enables administrators to associate products in their inventory with product manuals. It supports adding, editing, and deleting products individually, as well as performing bulk updates via file uploads. Administrators can then share a link with users/customers, allowing them to search for products by barcode and access the corresponding product manuals.

## Technologies

- **Django:** Backend framework for managing product data and handling business logic.
- **jQuery:** Frontend library for enhancing user interactions and AJAX operations.

## Features

- **Product Management:**
  - Add new products with name, barcode, and link.
  - Edit existing product details.
  - Delete products as needed.
  - Bulk upload for product modifications through file import.

- **Search Functionality:**
  - Customers can search for products by barcode.
  - Retrieve and access product manuals through associated links.

## Installation

1. **Clone the repository:**
   
   ```bash
   git clone https://github.com/yourusername/repository.git
   cd repository

2. **Set up a virtual environment:**
   
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`

3. **Install dependencies:**
   
   ```bash
   pip install -r requirements.txt

4. **Apply migrations:**
   
   ```bash
   python manage.py migrate
   
5. **Create a superuser:**
    
   ```bash
   python manage.py createsuperuser # Follow the prompts to create a superuser account with administrative privileges.

6. **Run the development server:**
    
   ```bash
   python manage.py runserver

7. **Run the development server:**
    
   ```bash
   Open your browser and go to http://127.0.0.1:8000.

## Usage

- **For Admins:**
  - Visit this url : http://localhost:8000/administrator/products/
  - Use the provided forms to manage product details.
  - Upload files for bulk product updates.

- **For Customers:**
  - Visit this url : http://localhost:8000/
  - Search products by barcode to access product manuals.

## Contributing

Feel free to submit pull requests or open issues for any bugs or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
