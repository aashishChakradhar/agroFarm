# AgroFarm

AgroFarm is an online agriculture-based e-commerce platform where farmers can directly sell their agro products, and customers can buy fresh products with a click. The website is built using the Django framework.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation Instructions](#installation-instructions)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Project Overview

AgroFarm is developed as a part of a semester project for the fifth semester. This platform bridges the gap between farmers and customers, enabling direct sales of fresh agro products. The platform offers a user-friendly interface for both farmers and customers, ensuring a seamless buying and selling experience.

## Features

- **User Authentication:** Secure login and registration for farmers and customers.
- **Product Listings:** Farmers can list their products with details and images.
- **Shopping Cart:** Customers can add products to the cart and proceed to checkout.
- **Order Management:** Farmers can manage orders received from customers.
- **Admin Dashboard:** Admin can oversee the entire platform, manage users, and products.

## Installation Instructions

To set up this project locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/aashishChakradhar/agroFarm.git
    cd agroFarm
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```bash
    python manage.py makemigtations merchant
    python manage.py migrate
    ```

5. **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

6. **Create a superuser (optional):**
    ```bash
    python manage.py createsuperuser
    ```

## Usage

1. **Start the application:**
    ```bash
    python manage.py runserver
    ```

2. **Access the website:**
    Open your browser and navigate to `http://localhost:8000`

3. **Superuser Details:**
    - **Username:** admin
    - **Password:** admin

4. **Register as a farmer or customer and start using the platform!**

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript, Bootstrap5
- **Backend:** Django
- **Database:** SQLite (default for Django, can be changed to PostgreSQL, MySQL, etc.)
- **Version Control:** Git

## Contribution Guidelines

We welcome contributions from the community! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/) - The web framework used
- [Bootstrap](https://getbootstrap.com/) - Frontend framework for responsive design
