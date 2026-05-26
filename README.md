# Slava Tech Accounts Payable System

A modular Python-based Accounts Payable desktop application built with Tkinter and SQLite.

This project was developed as a practical accounting and ERP-oriented learning project focused on modular architecture, relational databases, desktop UI development, analytics workflows, and financial record management.

The system includes:

- User authentication
- Vendor management
- Invoice/payment management
- Analytics dashboard
- Archive system
- SQLite relational database backend
- Modular business logic architecture

---

# Features

## Authentication
- Login system with password hashing
- Environment-variable-based credential storage

## Vendor Management
- Create vendors
- Edit vendors
- Search/view vendors
- Structured vendor ID generation

## Invoice Management
- Create invoices/payments
- Edit invoices
- Invoice validation workflows
- Structured invoice ID generation

## Analytics Dashboard
- Payment summaries
- Vendor-based filtering
- Date-based filtering
- Aggregate reporting

## Archive System
- Archive invoices by month/year
- Separate yearly SQLite archive databases

---

# Technologies Used

- Python
- Tkinter
- SQLite3

---

# Project Structure

```text
accounts_payable/
│
├── analytics/
├── auth/
├── database/
├── invoices/
├── ui/
├── utils/
├── vendors/
│
├── main.py
├── ap_system.db
└── requirements.txt
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/APP_USERNAME=admin/accounts-payable-system.git
cd accounts-payable-system
```

---

## 2. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 3. Create Environment Variables

Create a `.env` file in the project root:

```text
APP_USERNAME=demo_user
APP_PASSWORD_HASH=YOUR_HASH_HERE
```

---

## 4. Run Application

```bash
python main.py
```

---

# Example Login

Example credentials for testing:

```text
Username: demo_user
Password: demo_password
```
users must define their own environment variables,
and optionally generate their own password hash.
---

# Notes

This project was built as part of a larger long-term ERP and business systems development roadmap.

The focus of this repository is:
- modular architecture
- database design
- business workflow development
- desktop application structure
- practical accounting system concepts

---

# Future Improvements

- bcrypt/argon2 password security
- Full ERP integration
- Reporting exports
- Advanced analytics
- User roles/permissions
- Multi-user support
- API integrations
- Web-based deployment

---

# License

This project is provided for educational and portfolio purposes.
This repository was used to learn Git and GitHub workflow fundamentals.
