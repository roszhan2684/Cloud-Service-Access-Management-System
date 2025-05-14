Cloud Service Access Management System

This project is a backend system built with FastAPI and MongoDB that manages access to cloud services based on user subscription plans. It includes JWT-based authentication, role-based access control (RBAC), and usage tracking for various APIs.

Features

* User Registration (open for all)
* JWT Authentication (admin/user roles)
* Role-Based Access Control (RBAC)
* Subscription Plan Management
* Usage Tracking and Limit Enforcement
* 6 Simulated Cloud Service APIs
* Admin can manage permissions, plans, and users

Project Structure

app/
├── db.py                 - MongoDB setup
├── main.py               - FastAPI app entrypoint
├── models/               - Pydantic models
├── routes/               - All API routes
├── services/             - Utility functions, JWT, etc.

Requirements

* Python 3.10+
* MongoDB running locally or remotely

Install dependencies:

pip install -r requirements.txt

Example .env file:

MONGODB\_URI=mongodb://localhost:27017
DB\_NAME=cloud\_access

Run the Project

uvicorn app.main\:app --reload

Visit the docs at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Authentication

Use /token to log in and receive a JWT access token.

Example Users

Username: roszhan
Password: secret123
Role: admin

Username: john
Password: user123
Role: user

Use the Authorize button in Swagger UI and enter:

Bearer \<your\_token>

Key API Endpoints

Authentication

* POST /token - Login to get JWT token

Users

* POST /users/ - Create user (public)
* DELETE /users/{username} - Delete user (admin only)
* GET /users/ - View all users (admin only)

Permissions

* POST /permissions/ - Create permissions (admin only)
* GET /permissions/ - View all permissions

Plans

* POST /plans/ - Create a subscription plan (admin only)
* GET /plans/ - View all plans

Subscriptions

* POST /subscriptions/ - Subscribe user to a plan
* GET /subscriptions/{user\_id} - View subscription
* PUT /subscriptions/{user\_id} - Change subscription
* DELETE /subscriptions/{user\_id} - Remove subscription

Access Control

* GET /access/{user\_id}/{api\_name} - Check API access

Usage

* GET /subscriptions/{user\_id}/usage - View API usage

Cloud APIs (6 total)

* GET /cloud/api1/{user\_id} - Simulated cloud service
* GET /cloud/api2/{user\_id}
* GET /cloud/api3/{user\_id}
* GET /cloud/api4/{user\_id}
* GET /cloud/api5/{user\_id}
* GET /cloud/api6/{user\_id}

1. Authentication and Authorization
Login (POST /token)

Log in with roszhan (admin) → Should return a JWT token

Log in with john (user) → Should return a JWT token

Log in with invalid credentials → Should return 401 Unauthorized

JWT Token in Authorization Header

Try accessing admin-only endpoints without a token → Should return 401

Try accessing admin-only endpoints with user token → Should return 403

Try with admin token → Should allow access

2. Users (POST /users, DELETE /users, GET /users)
Create User (POST /users)

Create a regular user without any token → Should succeed

Create an admin user without token → Should return 403

Create an admin user with user token → Should return 403

Create an admin user with admin token → Should succeed

Delete User (DELETE /users/{username})

Try deleting a user with no token → Should return 401

Try deleting a user with user token → Should return 403

Delete a user with admin token → Should succeed

Get All Users (GET /users)

Try with user token → Should return 403

Try with admin token → Should return the user list

3. Permissions (POST /permissions, GET /permissions)
Create Permissions (POST /permissions)

Try creating permissions with user token → Should return 403

Create one or multiple permissions with admin token → Should succeed

Get All Permissions (GET /permissions)

Accessible by all roles → Should return the list of permission objects

4. Plans (POST /plans, GET /plans)
Create Plan (POST /plans)

Try without token → Should return 401

Try with user token → Should return 403

Try with admin token → Should succeed (create plan with API permissions and limits)

Get All Plans (GET /plans)

Accessible by all roles → Should return plan objects

5. Subscriptions (POST, PUT, GET, DELETE)
Subscribe a User (POST /subscriptions)

Without token → Should succeed only for regular users

With user token → Should work to subscribe themselves

With admin token → Can subscribe any user to any plan

Change Plan (PUT /subscriptions/{user_id})

With user token → Should allow only if changing their own subscription

With admin token → Can change any user’s subscription

View Subscription (GET /subscriptions/{user_id})

Without token → Should return 401

With user token → Should work if it's their own ID

With admin token → Can view any user’s subscription

Delete Subscription (DELETE /subscriptions/{user_id})

With user token → Should return 403

With admin token → Should succeed

6. Usage Tracking and Limits
GET /subscriptions/{user_id}/usage

User checks own usage → Should succeed

Admin checks anyone’s usage → Should succeed

Use Cloud API Multiple Times

Call GET /cloud/api1/{user_id} repeatedly until usage limit is hit → Last call should return 429 Too Many Requests

Try with unauthorized user → Should return 403

7. Access Control (GET /access/{user_id}/{api_name})
Check Access

User without a subscription → Should return 404

User with subscription, but API not in permissions → Should return 403

User with permission and usage within limit → Should return access granted

User exceeding usage limit → Should return 429

8. Cloud APIs (GET /cloud/api1–api6/{user_id})
Run All 6 APIs

Subscribe user to a plan with all 6 permissions

Call all:

GET /cloud/api1/{user_id}

GET /cloud/api2/{user_id}

GET /cloud/api3/{user_id}

GET /cloud/api4/{user_id}

GET /cloud/api5/{user_id}

GET /cloud/api6/{user_id}

Each should succeed if:

The user is subscribed

The plan has that API in permissions

The usage has not exceeded the limit

Edge Cases

Try calling an API that isn’t in the user’s plan → Should return 403

Try when usage exceeded → Should return 429

License

This project is for educational use. You can extend it and build upon it for your own applications.

Author

Roszhan Raj Meenakshi Sundhresan
Graduate Student in Computer Science
California State University, Fullerton.

Jenny Phan
UnderGrad Student in Computer Science
California State University, Fullerton.

Nayeem Sufyaan Abdul
Graduate Student in Computer Science
California State University, Fullerton.
