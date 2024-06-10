## Flask exercise - car repair shop

**Stage 1: Building the Foundation**

Task: Create a basic Flask application with routes for a landing page and an "About Us" page.
Steps:
- Use Flask to create a simple application.
- Define routes for the landing page (/) and "About Us" page (/about).
- Create HTML templates for each page with basic content.

**Stage 2: Customer and Car Management**

Task: Design a system to store customer information (name, phone number, etc.) and car details (make, model, year). Implement functionalities to add, view, and edit customer and car data. 

Steps:
- Define SQLAlchemy models for Customer and Car with relevant attributes.
- Create Flask routes to handle adding new customers and cars.
- Implement functionalities to view existing customer and car information.
- Allow editing of customer and car details through forms.

**Stage 3: Repair Services**

Task: Define different repair services offered by the shop (e.g., oil change, brake repair) with descriptions and estimated costs. Allow customers to book appointments for specific services on their cars.

Steps:
- Define a Service model with details like service name, description, and estimated cost.
- Establish relationships between Customer, Car, and Service models (e.g., a customer can book a service for their car).
- Create functionalities to view offered services and book appointments.
- Allow users to select a date and time for the appointment.

**Stage 4 (Optional): Advanced Features**

Steps:
- Design a system to track repair progress (e.g., pending, in progress, completed).
- Implement functionalities to generate invoices based on booked services.
- Implement an admin dashboard using `flask-admin`. The admin dashboard can include functionalities like:
  - Viewing and managing customer information (including adding/removing customers). 
  - Viewing and managing car details (including adding/removing car models). 
  - Managing the list of offered services (adding, editing, deleting services, updating prices). 
  - Viewing a calendar of booked appointments and their status (pending, in progress, completed). 
  - Generating reports on completed repairs, revenue earned, etc.
- Customer Portal: Develop a login system for customers to access a dedicated portal. 
  - They can view their appointment history and car repair details. 
  - Potentially allow them to reschedule appointments or request quotes for new services.
- Inventory Management: Implement a system to track spare parts and inventory levels. 
  - Allow for adding/removing parts, managing stock, and potentially linking parts used in specific repairs.
- Email Notifications: Integrate email functionalities to send automated notifications to customers about appointment confirmations, repair status updates, and invoices.
