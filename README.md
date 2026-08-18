# ✨ HairGlow Scheduler & Shop ✨

Welcome to **HairGlow Scheduler & Shop**, a premium, dark-themed Django web application designed for a luxury hair salon. It features an interactive, double-booking-proof appointment scheduling system and a fully integrated e-commerce shop with session-based cart management, checkout, and inventory tracking.

---

## 🌟 Key Features

### 📅 Smart Appointment Booking
*   **Availability Engine:** A custom JSON API endpoint (`/book/check-availability/`) checks and returns booked time slots for any selected date in real time.
*   **Double-Booking Prevention:** Enforced via a `unique_together` constraint on `(date, time_slot)` in the database and backed by validation inside the booking views.
*   **Validation Rules:** Users cannot book appointments in the past or double-book already confirmed times.
*   **Appointment Management:** Active bookings can be cancelled by the user from their dashboard (if still in `Pending` status).

### 🛍️ Integrated E-Commerce Shop
*   **Product Catalog & Search:** Browse luxury hair care items with advanced search queries checking both product names and descriptions.
*   **Session-based Shopping Cart:** Add, remove, and update quantities dynamically. Cart state is tracked on server-side sessions.
*   **Stock & Availability Checks:** Ensures customers cannot add or purchase more items than are currently in stock.
*   **Complete Checkout:** Generates `Order` and `OrderItem` records upon purchase, decrements inventory, and marks out-of-stock items as unavailable.

### 👤 User Account Management
*   **Authentication Flow:** Secure signup, login, and logout routines.
*   **Personal Dashboard:** View registered appointments (with cancel options) and past orders in one centralized hub.
*   **Protected Routes:** Using Django's `@login_required` decorators to protect checkout, booking, and dashboard views.

### 💎 Premium Responsive Design
*   **Visual Identity:** Curated luxury dark aesthetic (`#0b0c10` and `#12141a`) with shimmering gold accents (`#d4af37`), smooth animations, and glassmorphism.
*   **Typography:** Google Fonts pairing using **Outfit** for headings and **Plus Jakarta Sans** for body copy.
*   **Toast Messages:** Toast notification alerts for success, warnings, and errors.

---

## 📂 Project Structure

```text
hairglow_scheduler/
│
├── hairglow_scheduler/            # Main Django configuration project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                # App settings, DB setup, and template context processors
│   ├── urls.py                    # Root URL routing
│   └── wsgi.py
│
├── scheduler/                     # The core application app
│   ├── management/
│   │   └── commands/
│   │       └── seed_products.py   # Seeding command for standard luxury hair products
│   ├── migrations/                # Database migrations (SQLite default)
│   ├── context_processors.py      # Globally inserts shopping cart counts to navbar template
│   ├── models.py                  # Database Models (Product, Appointment, Order, OrderItem)
│   ├── tests.py                   # Comprehensive unit & integration tests
│   ├── urls.py                    # App-specific URL routes
│   └── views.py                   # View logic (cart, booking availability, login/register, checkout)
│
├── static/                        # Static assets
│   ├── css/
│   │   └── styles.css             # Main stylesheet implementing the premium theme
│   └── images/                    # Product mock-up image files
│
├── templates/                     # Jinja2-compatible Django templates
│   ├── base.html                  # Global layout with responsive header, cart count, and notifications
│   ├── booking.html               # Multi-step booking form with dynamic slot availability loading
│   ├── cart.html                  # Cart list with quantity adjustment and subtotal calculations
│   ├── checkout.html              # Customer details form with validation
│   ├── dashboard.html             # User profile hub (appointments, orders, cancellation triggers)
│   ├── home.html                  # Salon home page featuring luxury brand details & featured items
│   ├── login.html                 # Login page
│   ├── order_success.html         # Purchase summary receipt
│   ├── products.html              # Product listing and search interface
│   └── register.html              # Account registration page
│
├── db.sqlite3                     # SQLite Database file
├── manage.py                      # Django CLI script
└── .gitignore                     # Git ignore rules
```

---

## 🛠️ Getting Started

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Clone and Navigate
Navigate into your local workspace folder containing the project:
```bash
cd hairglow_scheduler
```

### 3. Create a Virtual Environment (Recommended)
Set up a clean virtual environment and activate it:
*   **Windows (PowerShell):**
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```
*   **Mac/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 4. Install Dependencies
This project runs on standard Django. Install the library directly using:
```bash
pip install django
```

### 5. Setup Database and Run Migrations
Run the Django migration commands to initialize your SQLite database schema:
```bash
python manage.py migrate
```

### 6. Seed Default Products
Populate the database with the pre-configured luxury products (shampoo, argan oil, hair mask, scalp massager) using the custom management seed command:
```bash
python manage.py seed_products
```

### 7. Create an Admin Account (Optional)
To access the Django admin panel (`http://127.0.0.1:8000/admin`), create a superuser credentials:
```bash
python manage.py createsuperuser
```

### 8. Launch the Development Server
Run the local dev server:
```bash
python manage.py runserver
```
Visit the app in your browser at: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧪 Running Tests

The application includes built-in test suites covering model functionality, views, validation limits (past dates, inventory availability), and double-booking prevention middleware checks.

To run the unit tests:
```bash
python manage.py test
```

---

## 🔮 Future Enhancements
*   💳 **Payment Integration:** Incorporate Stripe or PayPal sandbox for real credit card checkout transactions.
*   📧 **Notification System:** Send automated email confirmations and calendar invites (`.ics` files) upon booking approval.
*   📊 **Salon Dashboard:** A dedicated interface for salon staff to view daily schedules, manage appointments, and update product inventory.
*   🌟 **Reviews & Ratings:** Allow authenticated users to leave reviews and star ratings on hair products.
