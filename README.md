# Moroccan Card ID Scanner

## Overview
The Moroccan Card ID Scanner is a Django-based web application designed to streamline the process of selecting, scanning, and managing Moroccan ID cards to generate certificates. Users can choose the certificate they need by swiping left, scan the front and back of their ID, input their phone number, and receive information about the office they need to visit. The application also includes an admin interface for managing data and an employee interface with restricted permissions.

This project was created as my second Django project while I was interning in the province of Rehamna.

## Features
- **User Interface**:
  - Choose a certificate by swiping left.
  - Scan the front and back of the Moroccan ID card.
  - Input phone number.
  - Display the office location for further processing.
  
- **Admin Interface**:
  - Full access to all data.
  - Edit and manage user data and certificates.

- **Employee Interface**:
  - Edit and view filtered data based on permissions.
  - Access CIN data.
  - Transform CIN data into a certificate template.
  - Export certificate to PDF for users.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/AyoubSghuri/Django-Moroccan-cardid-scanner.git
    cd Django-Moroccan-cardid-scanner
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## Usage

### User Workflow
1. **Choose Certificate**:
   - Swipe left to select the desired certificate.

2. **Scan ID Card**:
   - Scan the front side of the ID card.
   - Scan the back side of the ID card.

3. **Enter Phone Number**:
   - Input your phone number.

4. **Display Office Location**:
   - The application will show the office you need to visit.

### Admin Interface
- Log in with your admin credentials.
- Access and manage all user data and certificates.
- Edit user details and certificate information.

### Employee Interface
- Log in with your employee credentials.
- Access and edit filtered data based on permissions.
- View and transform CIN data into certificate templates.
- Export certificates to PDF for users.

## Contributing
1. **Fork the repository**.
2. **Create a new branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Commit your changes**:
    ```bash
    git commit -m 'Add some feature'
    ```
4. **Push to the branch**:
    ```bash
    git push origin feature/your-feature-name
    ```
5. **Open a pull request**.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact
For any inquiries or issues, please contact Ayyoub.sghuri@gmail.com .
