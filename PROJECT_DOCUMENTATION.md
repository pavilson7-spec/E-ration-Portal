# E-Ration System — Full Project Documentation

> **Version:** 1.0  
> **Date:** February 2026  
> **Technology Stack:** Python · Flask · MySQL · Bootstrap 5 · Google Gemini AI  
> **Author / Developer:** Pavilson

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Technology Stack](#3-technology-stack)
4. [Project Folder Structure](#4-project-folder-structure)
5. [Database Schema](#5-database-schema)
6. [User Roles & Access Control](#6-user-roles--access-control)
7. [Application Modules](#7-application-modules)
   - 7.1 [Authentication Module](#71-authentication-module)
   - 7.2 [User Dashboard](#72-user-dashboard)
   - 7.3 [Family Member Management](#73-family-member-management)
   - 7.4 [Ration Quota System](#74-ration-quota-system)
   - 7.5 [Transaction History](#75-transaction-history)
   - 7.6 [Complaint Module](#76-complaint-module)
   - 7.7 [Slot Booking Module](#77-slot-booking-module)
   - 7.8 [Dealer Dashboard](#78-dealer-dashboard)
   - 7.9 [Admin Dashboard](#79-admin-dashboard)
   - 7.10 [AI Chatbot Assistant](#710-ai-chatbot-assistant)
8. [API Endpoints Reference](#8-api-endpoints-reference)
9. [Multilingual Support](#9-multilingual-support)
10. [Security Measures](#10-security-measures)
11. [Setup & Deployment Guide](#11-setup--deployment-guide)
12. [Key Business Rules](#12-key-business-rules)

---

## 1. Project Overview

The **E-Ration System** is a full-stack web application that digitises the Public Distribution System (PDS) / Ration management process. It replaces manual paperwork and physical queues by providing an online portal where citizens (users), ration shop dealers, and administrators can interact with each other seamlessly.

### Problem Statement
Traditional ration systems suffer from:
- Long queues at ration shops
- Manual record-keeping errors
- Lack of transparency in quota allocation
- No easy channel to raise complaints
- No way for citizens to track their transactions

### Solution
The E-Ration portal provides:
- **Digital quota tracking** per family member
- **Online complaint filing** and status tracking
- **Slot booking** to avoid crowding at shops
- **Real-time stock visibility** via the dealer dashboard
- **AI-powered chatbot** for instant self-service support
- **Admin oversight** for all operations

---

## 2. System Architecture

```
┌────────────────────────────────────────────────────────────┐
│                        Browser (Client)                    │
│           HTML5 + Bootstrap 5 + Vanilla JS                 │
└──────────────────────────┬─────────────────────────────────┘
                           │ HTTP / AJAX (JSON)
                           ▼
┌────────────────────────────────────────────────────────────┐
│                    Flask Web Server                        │
│                      app.py                                │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Routes    │  │  Templates   │  │  Session Mgmt   │   │
│  │ (views)     │  │ (Jinja2 HTML)│  │  (Flask session)│   │
│  └──────┬──────┘  └──────────────┘  └─────────────────┘   │
│         │                                                  │
│  ┌──────▼──────────────────────────────────────────────┐   │
│  │          Business Logic Layer (Python)              │   │
│  │  • Quota calculation  • Intent detection            │   │
│  │  • Role-based access  • Gemini AI integration       │   │
│  └──────┬──────────────────────────────────────────────┘   │
└─────────┼──────────────────────────────────────────────────┘
          │ mysql-connector-python
          ▼
┌────────────────────────────────────────────────────────────┐
│                  MySQL Database (e_ration_db)              │
│  users · dealers · admins · family_members · ration_quota  │
│  complaints · transactions · slots · slot_bookings         │
│  dealer_stock · card_requests · shops · stock_logs         │
└────────────────────────────────────────────────────────────┘
          │
          ▼ (external API)
┌─────────────────────────────┐
│   Google Gemini 2.5 Flash   │
│   (AI Chatbot Responses)    │
└─────────────────────────────┘
```

**Request-Response Flow:**
1. User opens the browser and navigates to `http://127.0.0.1:5000`
2. Flask serves the requested HTML template (Jinja2 rendered)
3. JavaScript on the page makes AJAX calls for chatbot (`/chatbot`)
4. Flask queries MySQL, runs business logic, returns JSON or HTML
5. For AI replies, Flask calls Google Gemini API and returns the answer

---

## 3. Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.x | Core programming language |
| **Web Framework** | Flask | HTTP routing, sessions, templating |
| **Database** | MySQL | Persistent data storage |
| **DB Connector** | `mysql-connector-python` | Python → MySQL interface |
| **Password Hashing** | `werkzeug.security` | `generate_password_hash` / `check_password_hash` |
| **AI / NLP** | Google Gemini 2.5 Flash | Chatbot natural language replies |
| **API Client** | `google-genai` | Gemini SDK |
| **Env Vars** | `python-dotenv` | Loading API keys from `.env` / `chat.env` |
| **Frontend CSS** | Bootstrap 5.3.3 | Responsive grid, components |
| **Icons** | Bootstrap Icons 1.11.3 | UI icon set |
| **JavaScript** | Vanilla ES6+ | Chatbot widget, dynamic UI |
| **Templating** | Jinja2 (built into Flask) | Server-side HTML rendering |

---

## 4. Project Folder Structure

```
e_ration_project/
│
├── app.py                          ← Main Flask application (all routes + logic)
├── chat.env                        ← Google Gemini API key (secret, gitignored)
├── database.sql                    ← Initial DB schema (reference)
│
├── static/
│   └── style.css                   ← Global base CSS (minimal; page styles in HTML)
│
├── templates/
│   ├── login.html                  ← Unified login page (User / Dealer / Admin)
│   ├── register.html               ← Registration page (choose role)
│   ├── dashboard.html              ← Redirect placeholder
│   │
│   ├── user_dashboard.html         ← User home with chatbot widget
│   ├── manage_members.html         ← Family member add/view/delete-request
│   ├── user_transactions.html      ← User's transaction history
│   ├── user_slots.html             ← Slot booking page for user
│   ├── complaint.html              ← File a new complaint
│   │
│   ├── dealer.html                 ← Dealer dashboard
│   │
│   ├── admin.html                  ← Admin main dashboard
│   ├── admin_dealers.html          ← Admin: manage dealers
│   ├── admin_members.html          ← Admin: approve/reject family members
│   ├── admin_slots.html            ← Admin: create and manage slots
│   ├── admin_stocks.html           ← Admin: stock monitoring
│   ├── admin_transaction_history.html  ← Admin: all transactions
│   └── admin_card_requests.html    ← Admin: approve/reject card requests
│
└── venv/                           ← Python virtual environment (not committed)
```

---

## 5. Database Schema

The live database name is **`e_ration_db`**. The tables and their relationships are:

### `users`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INT PK AUTO | Internal ID |
| `code` | VARCHAR | Unique code, must start with `US` (e.g., US001) |
| `username` | VARCHAR(100) | Display name |
| `email` | VARCHAR(150) | Email (optional, unique) |
| `password` | VARCHAR(255) | Werkzeug hashed password |
| `card_type` | VARCHAR | APL / BPL / NPH (after approval) |
| `card_status` | VARCHAR | Pending / Approved / Rejected |

### `dealers`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INT PK AUTO | Internal ID |
| `code` | VARCHAR | Must start with `DL` (e.g., DL001) |
| `shop_name` | VARCHAR | Name of the ration shop |
| `area` | VARCHAR | Area/locality |
| `password` | VARCHAR(255) | Hashed password |
| `status` | VARCHAR | Pending / Approved / Rejected |

### `admins`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INT PK | Internal ID |
| `code` | VARCHAR | Must start with `AD` (e.g., AD001) |
| `username` | VARCHAR | Admin's display name |
| `password` | VARCHAR(255) | Hashed password |

### `family_members`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INT PK AUTO | Internal ID |
| `user_code` | VARCHAR | FK → `users.code` |
| `member_name` | VARCHAR | Full name |
| `relation` | VARCHAR | Relationship (Father, Mother, etc.) |
| `age` | INT | Age in years |
| `status` | VARCHAR | Pending / Approved / Rejected |
| `delete_request` | TINYINT | 0 = normal, 1 = deletion requested |

### `ration_quota`
| Column | Type | Description |
|--------|------|-------------|
| `user_code` | VARCHAR | FK → `users.code` (unique) |
| `member_count` | INT | Count of approved members |
| `rice_total` | DECIMAL | Monthly rice entitlement (kg) |
| `rice_available` | DECIMAL | Remaining rice balance (kg) |
| `wheat_total` | DECIMAL | Monthly wheat entitlement (kg) |
| `wheat_balance` | DECIMAL | Remaining wheat balance (kg) |
| `sugar_total` | DECIMAL | Monthly sugar entitlement (kg) |
| `sugar_balance` | DECIMAL | Remaining sugar balance (kg) |

> Quota is auto-recomputed whenever a member is added/approved/deleted.
> **Default per member:** Rice 5 kg · Wheat 3 kg · Sugar 1 kg

### `complaints`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INT PK AUTO | Internal ID |
| `user_code` | VARCHAR | FK → `users.code` |
| `complaint_text` | TEXT | Full complaint description |
| `status` | VARCHAR | Pending / Resolved / In Review |
| `resolution` | TEXT | Admin's final resolution note |
| `created_at` | TIMESTAMP | Auto-set on insert |

### `transactions`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INT PK AUTO | Internal ID |
| `user_code` | VARCHAR | FK → `users.code` |
| `shop_name` | VARCHAR | Dealer's shop name |
| `dealer_code` | VARCHAR | FK → `dealers.code` |
| `item` | VARCHAR | Rice / Wheat / Sugar |
| `quantity` | DECIMAL | Quantity in kg |
| `txn_date` | DATETIME | Transaction timestamp |
| `price` | DECIMAL | (Optional) price if recorded |

### `slots`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INT PK AUTO | Internal ID |
| `slot_date` | DATE | Date of slot |
| `start_time` | TIME | Slot start time |
| `end_time` | TIME | Slot end time |
| `max_bookings` | INT | Max users allowed in this slot |
| `is_active` | TINYINT | 1 = active, 0 = disabled |

### `slot_bookings`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INT PK AUTO | Internal ID |
| `slot_id` | INT | FK → `slots.id` |
| `user_id` | INT | FK → `users.id` (numeric) |
| `status` | VARCHAR | BOOKED / CANCELLED |
| `created_at` | TIMESTAMP | Auto-set on insert |

### `dealer_stock`
| Column | Type | Description |
|--------|------|-------------|
| `dealer_code` | VARCHAR | FK → `dealers.code` (PK) |
| `rice` | DECIMAL | Current rice stock (kg) |
| `wheat` | DECIMAL | Current wheat stock (kg) |
| `sugar` | DECIMAL | Current sugar stock (kg) |

### `card_requests`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INT PK AUTO | Internal ID |
| `user_code` | VARCHAR | FK → `users.code` |
| `requested_card` | VARCHAR | APL / BPL / NPH |
| `status` | VARCHAR | Pending / Approved / Rejected |
| `admin_note` | TEXT | Admin's note on decision |
| `created_at` | TIMESTAMP | Request timestamp |

### `shops`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INT PK | Internal ID |
| `shop_name` | VARCHAR | Shop name |
| `dealer_name` | VARCHAR | Dealer's name |
| `address` | VARCHAR | Physical address |
| `area` | VARCHAR | Area/locality (matched to user's area) |
| `lat` | DECIMAL | GPS latitude |
| `lng` | DECIMAL | GPS longitude |

---

## 6. User Roles & Access Control

The system has **three distinct roles**, each controlled by the session variable `session["role"]`.

| Role | Code Prefix | Login Path | Dashboard |
|------|-------------|-----------|-----------|
| **User** (Citizen) | `US` (e.g. US001) | `/login` | `/user/dashboard` |
| **Dealer** | `DL` (e.g. DL001) | `/login` | `/dealer_dashboard` |
| **Admin** | `AD` (e.g. AD001) | `/login` | `/admin/dashboard` |

**Access Rules:**
- Every protected route checks `session.get("role")` at the top
- If the role doesn't match, the user is redirected to `/login`
- Dealers must be in `status = "Approved"` before they can log in
- New user registration is instant; dealer/admin must be registered with correct prefix

---

## 7. Application Modules

### 7.1 Authentication Module

**Routes:** `/` · `/register` · `/login` · `/logout`

#### Registration (`/register`)
- Supports three roles: `user`, `dealer`, `admin`
- Validates that the roll number starts with the correct prefix:
  - User → `US...`, Dealer → `DL...`, Admin → `AD...`
- Passwords are hashed with `werkzeug.security.generate_password_hash`
- On user registration, a blank quota row is auto-created via `recompute_quota_for_user()`
- Dealer registration sets status to `"Pending"` (requires admin approval)

#### Login (`/login`)
- Supports login by **roll number** (USxxx / DLxxx / ADxxx) or **username/shop name**
- If username/shop name is ambiguous (multiple matches), login via roll number is required
- Dealers blocked from login if `status != "Approved"`
- On successful login, sets: `session["role"]`, `session["code"]`, `session["name"]`
- User login auto-syncs quota on each login: `recompute_quota_for_user(code)`
- Preferred language stored in session (`session["lang"]` = `"en"` or `"ml"`)

#### Logout (`/logout`)
- Clears the entire session and redirects to `/login`

---

### 7.2 User Dashboard

**Route:** `/user/dashboard`  
**Template:** `user_dashboard.html`

The central hub for citizens. Displays:

| Section | Data Shown |
|---------|-----------|
| **Ration Availability** | Rice, Wheat, Sugar — total entitlement & remaining balance |
| **Transaction History** | Latest 5 ration pickups (date, shop, item, qty) |
| **Complaints** | Latest 5 complaints with status badges |
| **Nearest Ration Shop** | Shop name, dealer, address, Google Maps iframe embed |
| **AI Chatbot Widget** | Floating button, opens AI assistant panel |

**Sidebar links:** Dashboard · Manage Members · Transaction History · Complaints · Slot Booking

---

### 7.3 Family Member Management

**Route:** `/manage-members` (GET + POST)  
**Template:** `manage_members.html`

**Citizen can:**
- **Add a family member** (name, relation, age) — stored as `status = "Pending"` until admin approves
- **View all members** and their current status (Approved / Pending / Rejected)
- **Request deletion** of an approved member via `POST /members/request-delete/<mid>`
- **Request a ration card type** (APL / BPL / NPH) — submitted to admin for approval
- **View calculated quota** based on approved member count × card type rates

**Quota calculation per card type (per approved member):**
| Card Type | Rice | Wheat | Sugar |
|-----------|------|-------|-------|
| APL | 5 kg | 3 kg | 1 kg |
| BPL | 5 kg | 4 kg | 2 kg |
| NPH | 7 kg | 5 kg | 2 kg |

> Note: Default (no card type) uses 5 kg rice · 3 kg wheat · 1 kg sugar per member.

---

### 7.4 Ration Quota System

**Function:** `recompute_quota_for_user(user_code)`

This is a **core backend function** that recalculates a user's quota automatically whenever:
- A new user registers
- A family member is approved or rejected by admin
- A member deletion is approved

**Logic:**
1. Counts `Approved` members (where `delete_request = 0`)
2. Multiplies count by per-member rates (Rice 5 · Wheat 3 · Sugar 1 as default)
3. If quota row doesn't exist → creates it with full totals as available balance
4. If quota row exists → adjusts balances proportionally to the change in total
5. Ensures balance never goes below zero

---

### 7.5 Transaction History

**User Route:** `/user/transactions`  
**Admin Route:** `/admin/transactions`  
**Templates:** `user_transactions.html` · `admin_transaction_history.html`

- Users see only their own transactions
- Admin sees all users' transactions
- Recorded automatically when a dealer processes a pickup via `/dealer/purchase`
- Each transaction deducts:
  - The user's quota balance (`ration_quota`)
  - The dealer's stock (`dealer_stock`)

---

### 7.6 Complaint Module

**Route:** `/complaint` (GET + POST)  
**Template:** `complaint.html`

**Complaint Workflow:**
```
User files complaint (status: Pending)
        ↓
Dealer views and can mark Resolved
        ↓
Admin reviews, adds resolution text, marks final status
        ↓
User sees updated status on dashboard
```

**Statuses:** `Pending` → `In Review` / `Resolved`

---

### 7.7 Slot Booking Module

**User Route:** `/slots` (view) · `/slots/book` or `/slots/book/<id>` (book) · `/slots/cancel/<booking_id>` (cancel)  
**Admin Routes:** `/admin/slots` (manage) · `/admin/slots/create` (create) · `/admin/slots/delete/<id>` (delete)  
**Templates:** `user_slots.html` · `admin_slots.html`

**How it works:**
1. Admin creates time slots (date, start time, end time, max bookings)
2. Users see all active upcoming slots
3. User books a slot → booked count is checked against `max_bookings`
4. If slot is full → error returned
5. User can cancel a booking (status → `CANCELLED`)
6. Admin can view all bookings per slot and delete slots

---

### 7.8 Dealer Dashboard

**Route:** `/dealer_dashboard`  
**Template:** `dealer.html`

**Dealer capabilities:**
| Feature | Route | Description |
|---------|-------|-------------|
| View current stock | Dashboard | Rice, Wheat, Sugar stock levels |
| Update stock qty | `POST /dealer/update_stock` | Set new quantity for an item |
| Process purchase | `POST /dealer/purchase` | Collect ration for a user code |
| View complaints | Dashboard | See all complaints (to resolve) |
| Resolve complaint | `POST /dealer/resolve_complaint/<id>` | Mark a complaint as Resolved |

**Purchase validation checks:**
1. User code must exist in `users`
2. User must have sufficient quota balance for the requested item
3. Dealer must have sufficient stock for the item
4. If both checks pass → deducts quota + stock + creates transaction record

---

### 7.9 Admin Dashboard

**Route:** `/admin/dashboard`  
**Template:** `admin.html`

**Admin overview stats:**
- Total registered users
- Total registered dealers
- Pending complaints count

**Admin sub-modules:**

| Module | Route | Template | Description |
|--------|-------|----------|-------------|
| Member Approvals | `/admin/members` | `admin_members.html` | Approve / Reject pending family members; approve delete requests |
| Dealer Management | `/admin/dealers` | `admin_dealers.html` | Approve / Reject dealer accounts |
| Stock Monitoring | `/admin/stocks` | `admin_stocks.html` | View stock levels of all dealers |
| Complaint Handling | within `admin.html` | — | View all complaints, update status, add resolution note |
| Transaction History | `/admin/transactions` | `admin_transaction_history.html` | All users' transaction records |
| Card Requests | `/admin/card-requests` | `admin_card_requests.html` | Approve / Reject ration card type requests |
| Slot Management | `/admin/slots` | `admin_slots.html` | Create / view / delete time slots with booking lists |

---

### 7.10 AI Chatbot Assistant

**Routes:** `POST /chat` · `POST /chatbot` (alias)  
**Widget location:** Floating button on `user_dashboard.html` (bottom-right)

#### Architecture

```
User types message
      ↓
[Frontend JS] sends POST /chatbot { "message": "..." }
      ↓
[detect_intent()] → classifies message → route_key
      ↓
[gemini_reply()] → calls Gemini 2.5 Flash API
      ↓  (if Gemini unavailable or times out)
[_STATIC_REPLIES[route_key]] → fallback text
      ↓
Returns JSON { reply, route_key, actions[] }
      ↓
[Frontend] renders chat bubble + chip navigation buttons
```

#### Intent Classification (`detect_intent`)

The function uses **keyword matching** to classify the user's message:

| Keywords Detected | route_key |
|-------------------|-----------|
| hi, hello, thanks, bye, good morning | `none` |
| complaint, problem, issue, report | `complaint` |
| slot, book, booking, time, schedule | `slot_booking` |
| member, family, add/delete member | `members` |
| quota, balance, rice, wheat, sugar | `quota` |
| history, transaction, previous, record | `history` |
| nearest shop, location, map, nearby | `nearest_shop` |
| *(anything else)* | `dashboard` |

#### JSON Response Format

```json
{
  "reply": "You can raise or track your complaint on the Complaint page.",
  "route_key": "complaint",
  "actions": [
    { "label": "Raise a Complaint", "route_key": "complaint" },
    { "label": "Open Dashboard",    "route_key": "dashboard" }
  ]
}
```

#### Frontend Route Map (`ROUTE_MAP` in JS)

```javascript
const ROUTE_MAP = {
  dashboard:    "/user/dashboard",
  complaint:    "/complaint",
  members:      "/manage-members",
  quota:        "/user/dashboard",
  history:      "/user/transactions",
  nearest_shop: "/user/dashboard",
  slot_booking: "/slots",
  none:         null
};
```

#### Chip Button Rendering Rules
- If `route_key = "none"` → **no buttons** shown (greetings/thanks)
- Otherwise → 1–2 pill-shaped chip buttons are shown below the bot bubble
- Each chip has a Bootstrap Icon + label
- On click → `window.location.href = ROUTE_MAP[route_key]`
- Unknown route_key → falls back to `/user/dashboard`

#### Gemini AI Integration
- Model: **Gemini 2.5 Flash** (fast, cost-efficient)
- API Key loaded from `chat.env` → `GENAI_API_KEY`
- If key is missing → Gemini is skipped; static fallback reply is used
- Prompt instructs Gemini to:
  - Reply in 2–4 sentences max
  - Never fabricate personal quota/account data
  - Never say "Click here" (navigation handled by chip buttons)
  - Only discuss ration-related topics
- Post-processing regex strips any accidental "Click here..." text

---

## 8. API Endpoints Reference

### Public Routes
| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/` or `/register` | Registration page |
| GET/POST | `/login` | Login page |
| GET | `/logout` | Clear session and logout |

### User Routes (role = "user")
| Method | Path | Description |
|--------|------|-------------|
| GET | `/user/dashboard` | User home dashboard |
| GET/POST | `/manage-members` | Family member management |
| POST | `/members/request-delete/<mid>` | Request member deletion |
| GET | `/user/transactions` | Transaction history |
| GET/POST | `/complaint` | File/view complaints |
| GET | `/slots` | View available booking slots |
| POST | `/slots/book` | Book a slot (form body) |
| POST | `/slots/book/<slot_id>` | Book a slot (URL param) |
| POST | `/slots/cancel/<booking_id>` | Cancel a booking |

### Dealer Routes (role = "dealer")
| Method | Path | Description |
|--------|------|-------------|
| GET | `/dealer_dashboard` | Dealer home dashboard |
| POST | `/dealer/update_stock` | Set new stock quantity |
| POST | `/dealer/purchase` | Process ration collection |
| POST | `/dealer/resolve_complaint/<cid>` | Resolve a complaint |

### Admin Routes (role = "admin")
| Method | Path | Description |
|--------|------|-------------|
| GET | `/admin/dashboard` | Admin main dashboard |
| GET | `/admin/dealers` | Dealer list |
| POST | `/admin/dealers/approve/<did>` | Approve dealer |
| POST | `/admin/dealers/reject/<did>` | Reject dealer |
| GET | `/admin/members` | Pending member requests |
| POST | `/admin/members/approve/<mid>` | Approve member |
| POST | `/admin/members/reject/<mid>` | Reject member |
| POST | `/admin/members/approve-delete/<mid>` | Approve member deletion |
| GET | `/admin/stocks` | Stock monitoring |
| GET | `/admin/transactions` | All transactions |
| POST | `/admin/resolve_complaint/<cid>` | Resolve & add note |
| GET | `/admin/card-requests` | Card type requests |
| POST | `/admin/card-requests/<id>/action` | Approve/reject card |
| GET | `/admin/slots` | Slot management |
| POST | `/admin/slots/create` | Create a new slot |
| POST | `/admin/slots/delete/<id>` | Delete a slot |

### Chatbot Routes
| Method | Path | Description |
|--------|------|-------------|
| POST | `/chat` | Main chatbot endpoint (JSON) |
| POST | `/chatbot` | Alias for `/chat` (used by frontend) |

---

## 9. Multilingual Support

The app supports **English** and **Malayalam (മലയാളം)**.

- Language is stored in `session["lang"]` (`"en"` or `"ml"`)
- A `LANGUAGES` dict in `app.py` stores all UI string translations for both languages
- A Flask `context_processor` injects `t` (translation dict) and `lang_code` into every template
- Templates use syntax like: `{{ t.dashboard if t and t.dashboard else "Dashboard" }}`
- The AI chatbot's `detect_intent()` also handles Malayalam Unicode characters and romanised Malayalam keywords (namaskaram, entha, etc.)
- Language preference is preserved across login/logout

---

## 10. Security Measures

| Security Feature | Implementation |
|-----------------|---------------|
| **Password Hashing** | `werkzeug.security.generate_password_hash` (PBKDF2-SHA256) — passwords never stored as plain text |
| **Session-based Auth** | Flask server-side sessions with a strong secret key |
| **Role-based Access** | Every route checks `session.get("role")` before serving content |
| **Dealer Approval** | Dealers cannot log in until Admin approves their account |
| **Input Validation** | Roll number prefix checked on registration; quantity validated as numeric |
| **SQL Injection** | All queries use parameterised statements (`%s` placeholders with `mysql-connector`) |
| **Stock/Quota Checks** | Purchase route validates both user quota balance AND dealer stock before any deduction |
| **Session Isolation** | `session.clear()` on logout ensures no stale session data |

---

## 11. Setup & Deployment Guide

### Prerequisites
- Python 3.9+ installed
- MySQL Server running locally
- Google Gemini API key (optional — chatbot works without it with static replies)

### Step 1 — Clone / Set up project
```bash
cd e_ration_project
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install flask mysql-connector-python werkzeug python-dotenv google-genai
```

### Step 2 — Database setup
```sql
-- Run in MySQL Workbench or CLI
CREATE DATABASE IF NOT EXISTS e_ration_db;
USE e_ration_db;
-- Then create all tables as per Section 5
```
> The `database.sql` file in the project contains the initial schema reference.

### Step 3 — Configure DB credentials
In `app.py`, update the `get_db_connection()` function:
```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="e_ration_db"
    )
```

### Step 4 — Configure Gemini AI (optional)
Create or edit `chat.env` in the project root:
```
GENAI_API_KEY=your_google_gemini_api_key_here
```

### Step 5 — Run the server
```bash
venv\Scripts\python app.py
```
Open browser: **http://127.0.0.1:5000**

### Step 6 — Create first Admin
Register with a code starting with `AD` (e.g., `AD001`) via `/register`.

### Step 7 — Register a Dealer
Register with `DL` prefix → login as Admin → approve the dealer account.

---

## 12. Key Business Rules

1. **Roll number format is mandatory** — Users must start with `US`, Dealers with `DL`, Admins with `AD`.
2. **Dealer approval required** — A dealer can only log in after Admin approval.
3. **Quota is auto-computed** — Manually editing quota is not allowed; it is always recalculated from approved member count.
4. **Balance cannot go negative** — The purchase route blocks any transaction that would make quota or stock go negative.
5. **Member deletion is a 2-step process** — User requests deletion → Admin approves deletion → member record is removed → quota is recalculated.
6. **Slot capacity is enforced** — Booking is blocked if `booked_count >= max_bookings`.
7. **Duplicate card request prevention** — A second card request cannot be submitted while one is still `Pending`.
8. **Only one quota row per user** — `ration_quota` has unique `user_code`; updates use `UPDATE` not `INSERT`.
9. **Nearest shop matched by area** — The user's area field matches the `shops.area` field to find their assigned ration shop.
10. **AI chatbot is non-destructive** — The chatbot reads no personal data and writes nothing to the database.

---

*This documentation covers the complete E-Ration System as of February 2026.*
