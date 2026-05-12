# 1. EXECUTIVE SUMMARY

## Purpose

This project implements a lightweight backend API platform for managing customers, orders, and billing configuration. The primary objective is to demonstrate practical API design, backend architecture, integration orchestration, and scalable engineering patterns using a clean layered approach.

## Business Problem

Organizations often require systems where:
- Sales teams create customers and orders
- Finance teams access billing-related information
- Billing configuration is automatically initialized during operational workflows

This project simulates that flow by automatically creating a billing profile when the first customer order is created.

## Architecture Approach

A layered monolithic architecture was selected to balance:
- Simplicity for an MVP
- Clear separation of concerns
- Extensibility for future enhancements

The application follows a structured flow:

Controller → Service → Repository → Database

# 2. MVP SCOPE

## The current implementation supports:

Customer creation
Order creation
Automatic billing profile creation
Billing profile retrieval
Basic role-based access control (RBAC)
Centralized error handling
PostgreSQL-backed persistence

## The MVP intentionally avoids:

UI development
Invoice generation
Audit logging

# Extensibility Options

The system can evolve incrementally into a broader integration platform. 

* UI and workflow automation
* JWT/OAuth-based authentication
* Event-driven integrations
* Notification services
* Advanced reporting and analytics

The current architecture provides a stable foundation for these future capabilities while keeping the initial implementation intentionally lean.

# 3. BUSINESS CONTEXT

## Actors

| Role | Responsibility |
|---|---|
| Sales Team | Create customers and orders |
| Finance Team | Retrieve billing information |

---

## Operational Flow

1. Sales creates a customer profile
2. Sales creates an order for the customer
3. System automatically creates a billing profile (if one does not exist)
4. Finance retrieves billing information through a secured API

---

# 4. FUNCTIONAL REQUIREMENTS

## Customer Management
- Create customer profiles
- Store customer metadata:
  - Account name
  - State
  - Channel
  - Sales representative

---

## Order Management
- Create customer orders
- Associate orders with existing customers
- Persist order details:
  - Amount
  - Currency
  - Status

---

## Billing Management
- Automatically create billing profile on first order
- Reuse billing profile for subsequent orders
- Maintain billing summary metadata:
  - Billing frequency
  - Currency
  - Billing status
  - Total orders
  - Last billed timestamp

---

## Access Control
- Restrict customer and order creation to Sales role
- Restrict billing retrieval to Finance role

---

# 5. NON-FUNCTIONAL REQUIREMENTS

## Simplicity
The system is intentionally lightweight to support rapid development and learning-focused implementation.

---

## Scalability
Although traffic expectations are low (~10 API calls/day), the architecture supports future horizontal and functional expansion.

---

## Maintainability
The layered architecture promotes:
- Separation of concerns
- Easier debugging
- Independent layer evolution
- Cleaner testing strategy

---

## Extensibility
The design allows future integration of:
- UI applications
- Workflow orchestration
- Authentication providers
- Billing lifecycle management
- Event-driven processing

---

## Security
Basic RBAC is implemented to simulate controlled enterprise access patterns while keeping the MVP simple.

---

## Reliability
Database-backed persistence ensures consistent customer, order, and billing state management across API operations.

# 6. SYSTEM ARCHITECTURE

## Architecture Style

The application follows a layered monolithic architecture designed for clarity, maintainability, and future extensibility.

The system separates responsibilities into independent layers:
- Controllers handle HTTP requests/responses
- Services manage business logic
- Repositories handle database access
- Models define persistence structure

This structure keeps the codebase modular while remaining lightweight for an MVP implementation.

---

## High-Level Architecture Flow


                ┌─────────────────┐
                │   Client/API    │
                │  (APIDog/cURL)  │
                └────────┬────────┘
                         │ HTTP Request
                         ▼
                ┌─────────────────┐
                │   Controllers   │
                │ Request Routing │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Services     │
                │ Business Logic  │
                └────────┬────────┘
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
┌─────────────────┐           ┌─────────────────┐
│  Repositories   │           │   Middleware    │
│ Database Access │           │ RBAC / Errors   │
└────────┬────────┘           └─────────────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │
│    Database     │
└─────────────────┘

## Request Processing Flow

- Order Creation Example

POST /orders
    │
    ▼
OrderController
    │
    ▼
OrderService
    │
    ├── Validate customer existence
    │
    ├── Create order
    │
    └── Auto-create billing profile (if missing)
            │
            ▼
      BillingService
            │
            ▼
      BillingRepository
            │
            ▼
        PostgreSQL


# Architectural Benefits
* Separation of Concerns
Each layer has a dedicated responsibility, reducing coupling and improving maintainability.

* Extensibility

Future features such as UI applications and Workflow orchestration can be added without restructuring the core application.

* Testability

Business logic remains isolated in service layers, enabling focused unit and integration testing.

* Simplicity

The architecture avoids premature complexity while still reflecting enterprise backend design patterns.

# 7. API ENDPOINTS
| Method | Endpoint                       | Purpose             |
| ------ | ------------------------------ | ------------------- |
| POST   | /customers                     | Create customer     |
| POST   | /orders                        | Create order        |
| GET    | /billing-profile/{customer_id} | Get billing profile |
| GET    | /                              | Health check        |

## Customer API sample

### Sample Billing Endpoint

```
GET /api/v1/billing-profile/{customer_id}
```
### Sample Response

{
  "billing_number": "INV-1001",
  "billing_frequency": "MONTHLY",
  "currency": "USD",
  "status": "ACTIVE",
  "total_orders": 2,
  "last_billed_at": "2026-05-01T10:00:00"
}


# 8. DATA MODEL
## Database Tables

The application currently uses three core tables:

Table	Purpose
customers	Stores customer master data
orders	Stores customer orders
billing_profiles	Stores billing configuration and billing summary
## Entity Relationships
Customer → Orders
Customer → BillingProfile
One customer can have multiple orders
One customer has one billing profile

## ER Diagram
┌────────────────────┐
│     customers      │
├────────────────────┤
│ id (PK)            │
│ account_name       │
│ state              │
│ channel            │
│ sales_rep          │
└─────────┬──────────┘
          │
          │ 1-to-many
          ▼
┌────────────────────┐
│       orders       │
├────────────────────┤
│ id (PK)            │
│ customer_id (FK)   │
│ amount             │
│ currency           │
│ status             │
│ created_at         │
└────────────────────┘


┌────────────────────┐
│  billing_profiles  │
├────────────────────┤
│ id (PK)            │
│ customer_id (FK)   │
│ billing_number     │
│ billing_frequency  │
│ currency           │
│ status             │
│ total_orders       │
│ last_billed_at     │
└────────────────────┘

# 9. ACCESS CONTROL
## Roles
* Sales
* Finance

## Auth Model
Header based role validation
`x-user-role`

## Why
Lightweight MVP
Easy to demonstrate separation of duties
Extensible to JWT/OAuth later

# 10. ERROR HANDLING STRATEGY

## Approach

The application uses centralized error handling through middleware to ensure consistent API responses across all endpoints.

This prevents duplicated error logic inside controllers and keeps business logic cleaner.

---

## Error Categories

| Error Type | Purpose |
|---|---|
| ValidationError | Invalid request payload or missing fields |
| NotFoundError | Requested resource does not exist |
| AuthorizationError | Access denied due to role restrictions |
| InternalServerError | Unexpected application failures |

---

## Standard Error Response
{
  "error": "RESOURCE_NOT_FOUND",
  "message": "Customer not found"
}

## Why
Consistent API responses
Thin controllers
Cleaner service logic

# 11. TECHNOLOGY STACK

| Area | Technology |
|---|---|
| Language | Python |
| Backend Framework | Flask |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migration Tool | Flask-Migrate / Alembic |
| Validation | Marshmallow |
| Environment Management | python-dotenv |
| IDE | VSCode |
| API Testing | APIDog / cURL |

---

## Why Flask

Flask was selected because it:
- Is lightweight and easy to structure
- Supports API-first development
- Allows flexible architecture patterns
- Is easy to extend incrementally

The framework is well-suited for learning-focused backend development while still reflecting real-world engineering practices.

---

## Why PostgreSQL

PostgreSQL was chosen because it provides:
- Strong relational integrity
- Reliable transactional support
- Excellent SQL capabilities
- Scalability for future growth

It also aligns well with enterprise integration system patterns.

---

## Why SQLAlchemy

SQLAlchemy was used to:
- Simplify database interaction
- Support ORM-based modeling
- Reduce raw SQL boilerplate
- Enable easier schema evolution

---

## Why Flask-Migrate / Alembic

Migration tooling was added to:
- Version-control schema changes
- Safely evolve the database
- Maintain environment consistency
- Support iterative development

---

## Development Tooling

### VSCode
Used as the primary development environment for:
- Code management
- Debugging
- Extension support
- Git integration

---

### APIDog / cURL
Used for:
- API testing
- Endpoint validation
- Request/response verification
- RBAC testing

# 14. DATABASE MIGRATION STRATEGY

## Purpose

Database migrations are used to manage schema changes in a controlled and repeatable manner throughout the development lifecycle.

Instead of manually modifying database tables, schema updates are tracked as versioned migration scripts.

---

## Tools Used

| Tool | Purpose |
|---|---|
| Flask-Migrate | Flask integration for migrations |
| Alembic | Underlying migration engine |

---
## Why Migrations Were Introduced Early

Migrations were configured during initial setup to:

Keep schema evolution organized
Avoid manual database drift
Support iterative feature development
Enable reproducible environments

This approach becomes increasingly important as additional entities and relationships are introduced.

## Benefits
Version-controlled schema evolution
Safer database modifications
Easier rollback capability
Environment consistency
Reduced manual database management

# 15. SECURITY CONSIDERATIONS
Current
RBAC
Environment variable configuration
DB credential isolation
Future
JWT auth
HTTPS
Audit logging
Rate limiting

# 16.  TESTING STRATEGY

Happy Path Tests
Customer creation
Order creation
Billing auto-creation
Billing retrieval
RBAC Tests
Authorized access
Forbidden access
Edge Cases
Invalid customer
Missing fields
Duplicate billing profile prevention

# 17. SCALABILITY & FUTURE ENHANCEMENTS

Planned Enhancements
UI layer
Workflow engine
Invoice generation
Billing cycles
Async events
Notification integrations
Architecture Readiness

Explain how current layering supports future expansion.

# 18. LESSONS LEARNED / ENGINEERING DECISIONS
Importance of migrations
Layered separation benefits
Service orchestration patterns
Avoiding premature complexity
Designing extensible MVPs

# 19. APPENDIX

Project Structure
/app
  /controllers
  /services
  /repositories
  /models
  /schemas
  /middlewares
  /utils

venv creation
PostgreSQL setup
migrations
running app

