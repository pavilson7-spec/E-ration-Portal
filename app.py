from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change_this_to_a_strong_secret"

# -----------------------------
# ✅ Preferred Language (EN / ML) - applies to ALL templates
# (No UI structure change; templates can use {{ t.key }} )
# -----------------------------
LANGUAGES = {
    "en": {
        "login_title": "E-Ration Login",
        "preferred_language": "Preferred Language",
        "login": "Login",
        "logout": "Logout",
        "welcome": "Welcome",
        "back": "Back",

        # Common
        "e_ration_system": "E-Ration System",
        "dashboard": "Dashboard",
        "transaction_history": "Transaction History",
        "complaints": "Complaints",
        "view_all": "View All",
        "view": "View",
        "total": "Total",

        # User dashboard
        "user_dashboard": "User Dashboard",
        "user_label": "User",
        "manage_members": "Manage Members",
        "ration_availability": "Ration Availability",
        "view_monthly_quota": "View Monthly Quota",
        "rice": "Rice",
        "wheat": "Wheat",
        "sugar": "Sugar",
        "available": "Available",
        "balance": "Balance",
        "date": "Date",
        "shop": "Shop",
        "item": "Item",
        "qty": "Qty",
        "no_transactions_yet": "No transactions yet",
        "id": "ID",
        "complaint": "Complaint",
        "status": "Status",
        "resolved": "Resolved",
        "pending": "Pending",
        "no_complaints_yet": "No complaints yet",
        "file_new_complaint": "File New Complaint",
        "nearest_ration_shop": "Nearest Ration Shop",
        "dealer": "Dealer",
        "open_in_google_maps": "Open in Google Maps",

        # Dealer dashboard
        "dealer_dashboard": "Dealer Dashboard",
        "dealer_dashboard_functions": "Dealer Dashboard Functions",
        "stock_overview": "Stock Overview",
        "update_stock": "Update Stock",
        "live_stock": "Live Stock",
        "view_stock_availability": "View stock availability (Rice / Wheat / Sugar)",
        "current_stock": "Current stock",
        "update_stock_quantities": "Update Stock Quantities",
        "select_item_set_qty": "Select item and set new stock quantity (kg)",
        "new_quantity_kg": "New Quantity (kg)",
        "pending_resolved": "Pending / Resolved",
        "view_and_resolve": "View and resolve user complaints",
        "user": "User",
        "action": "Action",
        "mark_resolved": "Mark Resolved",
        "no_complaints_assigned": "No complaints assigned to you",

        # Admin dashboard
        "admin_dashboard": "Admin Dashboard",
        "admin_panel": "Admin Panel",
        "admin": "ADMIN",
        "user_management": "User Management",
        "stock_monitoring": "Stock Monitoring",
        "complaint_handling": "Complaint Handling",
        "total_users": "Total Users",
        "total_dealers": "Total Dealers",
        "pending_complaints": "Pending Complaints",
        "active_pending": "Active & Pending",
        "need_action": "Need action",
        "dealer_management": "Dealer Management",
        "approve_modify_deactivate": "Approve, modify or deactivate accounts",
        "code": "Code",
        "name": "Name",
        "role": "Role",
        "active": "Active",
        "approve": "Approve",
        "deactivate": "Deactivate",
        "no_pending_accounts": "No pending accounts",
        "review_verify_resolution": "Review complaints, verify dealer response, mark final resolution",
        "in_review": "In Review",
        "final_resolution_placeholder": "Final resolution..."
    },

    "ml": {
        "login_title": "ഇ-റേഷൻ ലോഗിൻ",
        "preferred_language": "ഭാഷ തിരഞ്ഞെടുക്കുക",
        "login": "ലോഗിൻ",
        "logout": "ലോഗൗട്ട്",
        "welcome": "സ്വാഗതം",
        "back": "തിരികെ",

        # Common
        "e_ration_system": "ഇ-റേഷൻ സിസ്റ്റം",
        "dashboard": "ഡാഷ്ബോർഡ്",
        "transaction_history": "ഇടപാട് ചരിത്രം",
        "complaints": "പരാതികൾ",
        "view_all": "എല്ലാം കാണുക",
        "view": "കാണുക",
        "total": "ആകെ",

        # User dashboard
        "user_dashboard": "ഉപയോക്തൃ ഡാഷ്ബോർഡ്",
        "user_label": "ഉപയോക്താവ്",
        "manage_members": "അംഗങ്ങളെ നിയന്ത്രിക്കുക",
        "ration_availability": "റേഷൻ ലഭ്യത",
        "view_monthly_quota": "മാസ ക്വോട്ട കാണുക",
        "rice": "അരി",
        "wheat": "ഗോതമ്പ്",
        "sugar": "പഞ്ചസാര",
        "available": "ലഭ്യം",
        "balance": "ബാലൻസ്",
        "date": "തീയതി",
        "shop": "കട",
        "item": "ഇനം",
        "qty": "അളവ്",
        "no_transactions_yet": "ഇതുവരെ ഇടപാടുകളില്ല",
        "id": "ഐഡി",
        "complaint": "പരാതി",
        "status": "സ്ഥിതി",
        "resolved": "പരിഹരിച്ചു",
        "pending": "ബാക്കി",
        "no_complaints_yet": "ഇതുവരെ പരാതികളില്ല",
        "file_new_complaint": "പുതിയ പരാതി നൽകുക",
        "nearest_ration_shop": "ഏറ്റവും അടുത്ത റേഷൻ കട",
        "dealer": "ഡീലർ",
        "open_in_google_maps": "ഗൂഗിൾ മാപ്സിൽ തുറക്കുക",

        # Dealer dashboard
        "dealer_dashboard": "ഡീലർ ഡാഷ്ബോർഡ്",
        "dealer_dashboard_functions": "ഡീലർ ഡാഷ്ബോർഡ് പ്രവർത്തനങ്ങൾ",
        "stock_overview": "സ്റ്റോക്ക് അവലോകനം",
        "update_stock": "സ്റ്റോക്ക് പുതുക്കുക",
        "live_stock": "ലൈവ് സ്റ്റോക്ക്",
        "view_stock_availability": "സ്റ്റോക്ക് ലഭ്യത കാണുക (അരി / ഗോതമ്പ് / പഞ്ചസാര)",
        "current_stock": "നിലവിലെ സ്റ്റോക്ക്",
        "update_stock_quantities": "സ്റ്റോക്ക് അളവുകൾ പുതുക്കുക",
        "select_item_set_qty": "ഇനം തിരഞ്ഞെടുക്കുക, പുതിയ സ്റ്റോക്ക് അളവ് (കിലോ) നൽകുക",
        "new_quantity_kg": "പുതിയ അളവ് (കിലോ)",
        "pending_resolved": "ബാക്കി / പരിഹരിച്ചു",
        "view_and_resolve": "ഉപയോക്തൃ പരാതികൾ കാണുകയും പരിഹരിക്കുകയും ചെയ്യുക",
        "user": "ഉപയോക്താവ്",
        "action": "നടപടി",
        "mark_resolved": "പരിഹരിച്ചു എന്ന് അടയാളപ്പെടുത്തുക",
        "no_complaints_assigned": "നിങ്ങൾക്ക് നൽകപ്പെട്ട പരാതികളില്ല",

        # Admin dashboard
        "admin_dashboard": "അഡ്മിൻ ഡാഷ്ബോർഡ്",
        "admin_panel": "അഡ്മിൻ പാനൽ",
        "admin": "അഡ്മിൻ",
        "user_management": "ഉപയോക്തൃ മാനേജ്മെന്റ്",
        "stock_monitoring": "സ്റ്റോക്ക് നിരീക്ഷണം",
        "complaint_handling": "പരാതി കൈകാര്യം ചെയ്യൽ",
        "total_users": "ആകെ ഉപയോക്താക്കൾ",
        "total_dealers": "ആകെ ഡീലർമാർ",
        "pending_complaints": "ബാക്കി പരാതികൾ",
        "active_pending": "സജീവം & ബാക്കി",
        "need_action": "നടപടി ആവശ്യമാണ്",
        "dealer_management": "ഡീലർ മാനേജ്മെന്റ്",
        "approve_modify_deactivate": "അക്കൗണ്ടുകൾ അംഗീകരിക്കുക / മാറ്റം വരുത്തുക / നിർജീവമാക്കുക",
        "code": "കോഡ്",
        "name": "പേര്",
        "role": "റോൾ",
        "active": "സജീവം",
        "approve": "അംഗീകരിക്കുക",
        "deactivate": "നിർജീവമാക്കുക",
        "no_pending_accounts": "ബാക്കി അക്കൗണ്ടുകളില്ല",
        "review_verify_resolution": "പരാതികൾ പരിശോധിക്കുക, ഡീലർ മറുപടി പരിശോധിക്കുക, അന്തിമ പരിഹാരം രേഖപ്പെടുത്തുക",
        "in_review": "പരിശോധനയിൽ",
        "final_resolution_placeholder": "അന്തിമ പരിഹാരം..."
        "member_approval" "അംഗ അംഗീകാരം",
        "member_approval_sub": "പുതിയ അംഗങ്ങളെ അംഗീകരിക്കുക / നിരസിക്കുക, ഡിലീറ്റ് അഭ്യർത്ഥനകൾ അംഗീകരിക്കുക",
        "back_to_dashboard": "ഡാഷ്ബോർഡിലേക്ക് തിരികെ",
        "pending_member_requests": "ബാക്കി അംഗ അഭ്യർത്ഥനകൾ",
        "user_code": "ഉപയോക്തൃ കോഡ്",
        "member_name": "അംഗത്തിന്റെ പേര്",
        "relation": "ബന്ധം",
        "age": "വയസ്",
        "reject": "നിരസിക്കുക",
        "delete_requests_approved": "ഡിലീറ്റ് അഭ്യർത്ഥനകൾ (അംഗീകരിച്ച അംഗങ്ങൾ)",
        "requests": "അഭ്യർത്ഥനകൾ",
        "no_pending_members": "ബാക്കി അംഗങ്ങളില്ല",
        "no_delete_requests": "ഡിലീറ്റ് അഭ്യർത്ഥനകളില്ല",
        "approve_delete": "ഡിലീറ്റ് അംഗീകരിക്കുക",
        
        "e_ration_admin": "E-Ration Admin",
        "dealer_stock_updates_history": "Dealer stock updates history (latest first)",
        "no_dealer_stock_data_found": "No dealer stock data found.",
        "dealer_code": "Dealer Code",
        "rice_kg": "Rice (Kg)",
        "wheat_kg": "Wheat (Kg)",
        "sugar_kg": "Sugar (Kg)",
        "e_ration_admin": "ഇ-റേഷൻ അഡ്മിൻ",
        "dealer_stock_updates_history": "ഡീലർ സ്റ്റോക്ക് അപ്ഡേറ്റുകളുടെ ചരിത്രം (പുതിയത് ആദ്യം)",
        "no_dealer_stock_data_found": "ഡീലർ സ്റ്റോക്ക് ഡാറ്റ കണ്ടെത്തിയില്ല.",
        "dealer_code": "ഡീലർ കോഡ്",
        "rice_kg": "അരി (കിലോ)",
        "wheat_kg": "ഗോതമ്പ് (കിലോ)",
        "sugar_kg": "പഞ്ചസാര (കിലോ)",
        "manage_family_members": "Manage Family Members",
        "manage_family_members_sub": "Add and view your family members for ration management.",
        "add_new_member": "Add New Member",
"member_name": "Member Name",
"member_name_ph": "e.g., Kumar",
"relation": "Relation",
"relation_ph": "e.g., Father / Mother",
"age": "Age",
"age_ph": "e.g., 45",
"add": "Add",
"note_new_members_pending_1": "Note: New members will be",
"note_new_members_pending_2": "until Admin approval.",
"members_list": "Members List",
"approved": "Approved",
"rejected": "Rejected",
"delete_requested": "Delete Requested",
"request_delete": "Request Delete",
"no_members_added_yet": "No members added yet.",

"manage_family_members": "കുടുംബാംഗങ്ങളെ നിയന്ത്രിക്കുക",
"manage_family_members_sub": "റേഷൻ മാനേജ്മെന്റിനായി നിങ്ങളുടെ കുടുംബാംഗങ്ങളെ ചേർക്കുകയും കാണുകയും ചെയ്യുക.",
"add_new_member": "പുതിയ അംഗത്തെ ചേർക്കുക",
"member_name": "അംഗത്തിന്റെ പേര്",
"member_name_ph": "ഉദാ: കുമാർ",
"relation": "ബന്ധം",
"relation_ph": "ഉദാ: അച്ഛൻ / അമ്മ",
"age": "വയസ്",
"age_ph": "ഉദാ: 45",
"add": "ചേർക്കുക",
"note_new_members_pending_1": "കുറിപ്പ്: പുതിയ അംഗങ്ങൾ",
"note_new_members_pending_2": "അഡ്മിൻ അംഗീകാരം വരുമ്ബോളം ബാക്കി (Pending) ആയിരിക്കും.",
"members_list": "അംഗങ്ങളുടെ പട്ടിക",
"approved": "അംഗീകരിച്ചു",
"rejected": "നിരസിച്ചു",
"delete_requested": "ഡിലീറ്റ് അഭ്യർത്ഥിച്ചു",
"request_delete": "ഡിലീറ്റ് അഭ്യർത്ഥിക്കുക",
"no_members_added_yet": "ഇതുവരെ അംഗങ്ങളെ ചേർത്തിട്ടില്ല.",

"transaction_history": "Transaction History",
"no_transactions_found": "No transactions found",
"id": "ID",
"shop": "Shop",
"item": "Item",
"quantity": "Quantity",
"date": "Date",

"transaction_history": "ഇടപാട് ചരിത്രം",
"no_transactions_found": "ഇടപാടുകൾ ഒന്നും കണ്ടെത്തിയില്ല",
"id": "ഐഡി",
"shop": "കട",
"item": "സാധനം",
"quantity": "അളവ്",
"date": "തീയതി",

"complaint_title": "E-Ration | Complaint",
"e_ration_system": "E-Ration System",
"complaint_module": "Complaint Module",
"file_new_complaint": "File a New Complaint",
"complaint_intro": "Please explain your issue clearly. Our team will review and update the status.",
"secure": "Secure",
"complaint_details": "Complaint Details",
"complaint_placeholder": "Example: Ration quantity mismatch / Dealer not available / Transaction issue...",
"tip_add_details": "Tip: Add date, shop name, and what went wrong.",
"submit_complaint": "Submit Complaint",
"cancel": "Cancel",
"guidelines": "Guidelines",
"be_specific": "Be Specific",
"be_specific_desc": "Mention item, month, shop name, and issue.",
"status_updates": "Status Updates",
"status_updates_desc_1": "Default status:",
"status_updates_desc_2": "Admin will update later.",
"need_help": "Need Help?",
"need_help_desc": "If urgent, contact your nearest ration shop.",
"note": "Note:",
"after_submit_redirect": "After submitting, you’ll be redirected back to the dashboard.",

"complaint_title": "ഇ-റേഷൻ | പരാതി",
"e_ration_system": "ഇ-റേഷൻ സിസ്റ്റം",
"complaint_module": "പരാതി മോഡ്യൂൾ",
"file_new_complaint": "പുതിയ പരാതി നൽകുക",
"complaint_intro": "ദയവായി നിങ്ങളുടെ പ്രശ്നം വ്യക്തമായി വിവരിക്കുക. ഞങ്ങളുടെ ടീം പരിശോധിച്ച് സ്ഥിതി അപ്ഡേറ്റ് ചെയ്യും.",
"secure": "സുരക്ഷിതം",
"complaint_details": "പരാതിയുടെ വിശദാംശങ്ങൾ",
"complaint_placeholder": "ഉദാ: റേഷൻ അളവ് പൊരുത്തക്കേട് / ഡീലർ ലഭ്യമല്ല / ഇടപാട് പ്രശ്നം...",
"tip_add_details": "ടിപ്പ്: തീയതി, കടയുടെ പേര്, എന്താണ് തെറ്റായി സംഭവിച്ചതെന്ന് ചേർക്കുക.",
"submit_complaint": "പരാതി സമർപ്പിക്കുക",
"cancel": "റദ്ദാക്കുക",
"guidelines": "നിർദ്ദേശങ്ങൾ",
"be_specific": "വ്യക്തമായി എഴുതുക",
"be_specific_desc": "സാധനം, മാസം, കടയുടെ പേര്, പ്രശ്നം എന്നിവ പറയുക.",
"status_updates": "സ്റ്റാറ്റസ് അപ്ഡേറ്റുകൾ",
"status_updates_desc_1": "ഡീഫോൾട്ട് സ്റ്റാറ്റസ്:",
"status_updates_desc_2": "അഡ്മിൻ പിന്നീട് അപ്ഡേറ്റ് ചെയ്യും.",
"need_help": "സഹాయం വേണമോ?",
"need_help_desc": "അത്യാവശ്യമാണ് എങ്കിൽ അടുത്ത റേഷൻ കടയെ ബന്ധപ്പെടുക.",
"note": "കുറിപ്പ്:",
"after_submit_redirect": "സമർപ്പിച്ച ശേഷം, നിങ്ങൾ ഡാഷ്ബോർഡിലേക്ക് തിരികെ കൊണ്ടുപോകപ്പെടും.",
"date_time": "Date & Time",
"date_time": "തീയതി & സമയം",

    }
}


def get_lang_dict():
    code = session.get("lang", "en")
    return LANGUAGES.get(code, LANGUAGES["en"])

@app.context_processor
def inject_lang():
    return {"t": get_lang_dict(), "lang_code": session.get("lang", "en")}

# -----------------------------
# DB Connection
# -----------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pavilson@123",
        database="e_ration_db"
    )

# -----------------------------
# ✅ QUOTA CALCULATION
# Per member: Rice 5kg, Wheat 3kg, Sugar 1kg
# COUNT ONLY APPROVED MEMBERS (and not delete_request)
# -----------------------------
def recompute_quota_for_user(user_code: str):
    PER_RICE = 5
    PER_WHEAT = 3
    PER_SUGAR = 1

    db = None
    cur = None
    try:
        db = get_db_connection()
        cur = db.cursor(dictionary=True)

        cur.execute("""
            SELECT COUNT(*) AS c
            FROM family_members
            WHERE user_code=%s AND status='Approved' AND delete_request=0
        """, (user_code,))
        member_count = (cur.fetchone() or {}).get("c", 0)

        rice_total = PER_RICE * member_count
        wheat_total = PER_WHEAT * member_count
        sugar_total = PER_SUGAR * member_count

        cur.execute("SELECT * FROM ration_quota WHERE user_code=%s LIMIT 1", (user_code,))
        existing = cur.fetchone()

        cur2 = db.cursor()
        if existing is None:
            cur2.execute(
                """
                INSERT INTO ration_quota
                  (user_code, member_count,
                   rice_total, rice_available,
                   wheat_total, wheat_balance,
                   sugar_total, sugar_balance)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (user_code, member_count,
                 rice_total, rice_total,
                 wheat_total, wheat_total,
                 sugar_total, sugar_total)
            )
        else:
            old_rice_total = existing.get("rice_total", 0)
            old_rice_avail = existing.get("rice_available", 0)

            old_wheat_total = existing.get("wheat_total", 0)
            old_wheat_bal = existing.get("wheat_balance", 0)

            old_sugar_total = existing.get("sugar_total", 0)
            old_sugar_bal = existing.get("sugar_balance", 0)

            new_rice_avail = max(0, old_rice_avail + (rice_total - old_rice_total))
            new_wheat_bal = max(0, old_wheat_bal + (wheat_total - old_wheat_total))
            new_sugar_bal = max(0, old_sugar_bal + (sugar_total - old_sugar_total))

            cur2.execute(
                """
                UPDATE ration_quota
                SET member_count=%s,
                    rice_total=%s,  rice_available=%s,
                    wheat_total=%s, wheat_balance=%s,
                    sugar_total=%s, sugar_balance=%s
                WHERE user_code=%s
                """,
                (member_count,
                 rice_total, new_rice_avail,
                 wheat_total, new_wheat_bal,
                 sugar_total, new_sugar_bal,
                 user_code)
            )

        db.commit()
        cur2.close()

    except Error as e:
        print("Quota recompute DB Error:", e)

    finally:
        if cur:
            cur.close()
        if db:
            db.close()

# -----------------------------
# Register
# -----------------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # ✅ keep language if submitted (optional)
        lang = (request.form.get("language") or "").strip().lower()
        if lang in ["en", "ml"]:
            session["lang"] = lang
        else:
            session.setdefault("lang", "en")

        role = request.form.get("role", "").strip().lower()
        code = request.form.get("code", "").strip().upper()
        password = request.form.get("password", "").strip()

        username = (request.form.get("username") or "").strip()
        admin_username = (request.form.get("admin_username") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        shop_name = (request.form.get("shop_name") or "").strip()
        area = (request.form.get("area") or "").strip()

        if role not in ["user", "dealer", "admin"]:
            return "invalid role selected"
        if not code or not password:
            return "Roll number and password are required"

        prefix_map = {"user": "US", "dealer": "DL", "admin": "AD"}
        if not code.startswith(prefix_map[role]):
            return f"{role.title()} roll number must start with {prefix_map[role]} (Example: {prefix_map[role]}001)"

        if role == "user" and not username:
            return "Username is required"
        if role == "admin" and not admin_username:
            return "Admin username is required"
        if role == "dealer" and not shop_name:
            return "Shop name is required"

        hashed_password = generate_password_hash(password)

        db = get_db_connection()
        cur = db.cursor(dictionary=True)

        try:
            if role == "user":
                cur.execute("SELECT id FROM users WHERE code=%s", (code,))
                if cur.fetchone():
                    return "This user code already registered"

                cur2 = db.cursor()
                cur2.execute(
                    "INSERT INTO users (code, username, email, password) VALUES (%s,%s,%s,%s)",
                    (code, username, email if email else None, hashed_password)
                )
                db.commit()
                cur2.close()

                recompute_quota_for_user(code)

            elif role == "dealer":
                cur.execute("SELECT id FROM dealers WHERE code=%s", (code,))
                if cur.fetchone():
                    return "This dealer code already registered"

                cur2 = db.cursor()
                cur2.execute(
                    "INSERT INTO dealers (code, shop_name, area, password, status) VALUES (%s,%s,%s,%s,%s)",
                    (code, shop_name, area if area else None, hashed_password, "Pending")
                )
                db.commit()
                cur2.close()

            elif role == "admin":
                cur.execute("SELECT id FROM admins WHERE code=%s", (code,))
                if cur.fetchone():
                    return "This admin code already registered"

                cur2 = db.cursor()
                cur2.execute(
                    "INSERT INTO admins (code, username, password) VALUES (%s,%s,%s)",
                    (code, admin_username, hashed_password)
                )
                db.commit()
                cur2.close()

            return redirect(url_for("login"))

        except mysql.connector.Error as e:
            return f"DB Error: {e}"

        finally:
            cur.close()
            db.close()

    return render_template("register.html")

# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = None

    if request.method == "POST":
        # ✅ store preferred language (if dropdown exists)
        lang = (request.form.get("language") or "").strip().lower()
        if lang in ["en", "ml"]:
            session["lang"] = lang
        else:
            session.setdefault("lang", "en")

        identifier = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not identifier or not password:
            error_msg = "Enter username/code and password"
            return render_template("login.html", error=error_msg)

        db = get_db_connection()
        cur = db.cursor(dictionary=True)

        try:
            code_try = identifier.strip().upper()

            if code_try.startswith("US"):
                cur.execute("SELECT code, username, password FROM users WHERE code=%s LIMIT 1", (code_try,))
                user = cur.fetchone()

                if user and check_password_hash(user["password"], password):
                    keep_lang = session.get("lang", "en")
                    session.clear()
                    session["lang"] = keep_lang

                    session["role"] = "user"
                    session["code"] = user["code"]
                    session["name"] = user["username"]
                    recompute_quota_for_user(user["code"])
                    return redirect(url_for("user_dashboard"))
                return render_template("login.html", error="Invalid User roll number/password")

            # ✅ Dealer login: ONLY APPROVED
            if code_try.startswith("DL"):
                cur.execute("""
                    SELECT
                        code,
                        shop_name,
                        password,
                        COALESCE(status,'Pending') AS status
                    FROM dealers
                    WHERE code=%s
                    LIMIT 1
                """, (code_try,))

                dealer = cur.fetchone()

                if dealer is None:
                    return render_template("login.html", error="Invalid Dealer roll number/password")

                if dealer["status"] != "Approved":
                    return render_template("login.html", error="Dealer account not approved by admin")

                if check_password_hash(dealer["password"], password):
                    keep_lang = session.get("lang", "en")
                    session.clear()
                    session["lang"] = keep_lang

                    session["role"] = "dealer"
                    session["code"] = dealer["code"]
                    session["name"] = dealer["shop_name"]
                    return redirect(url_for("dealer_dashboard"))

                return render_template("login.html", error="Invalid Dealer roll number/password")

            if code_try.startswith("AD"):
                cur.execute("SELECT code, username, password FROM admins WHERE code=%s LIMIT 1", (code_try,))
                admin = cur.fetchone()

                if admin and check_password_hash(admin["password"], password):
                    keep_lang = session.get("lang", "en")
                    session.clear()
                    session["lang"] = keep_lang

                    session["role"] = "admin"
                    session["code"] = admin["code"]
                    session["name"] = admin["username"]
                    return redirect(url_for("admin_dashboard"))
                return render_template("login.html", error="Invalid Admin roll number/password")

            # fallback: username/email/shop_name login
            cur.execute(
                "SELECT code, username, password FROM users WHERE username=%s OR email=%s LIMIT 2",
                (identifier, identifier)
            )
            user_match = cur.fetchall()

            cur.execute("""
                SELECT code, shop_name, password
                FROM dealers
                WHERE shop_name=%s AND COALESCE(status,'Pending')='Approved'
                LIMIT 2
            """, (identifier,))
            dealer_match = cur.fetchall()

            cur.execute("SELECT code, username, password FROM admins WHERE username=%s LIMIT 2", (identifier,))
            admin_match = cur.fetchall()

            total = len(user_match) + len(dealer_match) + len(admin_match)

            if total == 0:
                return render_template("login.html", error="No account found. Use correct username/shop name OR roll number (US/DL/AD).")

            if total > 1:
                return render_template("login.html", error="Multiple accounts found with this name. Please login using roll number (USxxx/DLxxx/ADxxx).")

            if len(user_match) == 1:
                user = user_match[0]
                if check_password_hash(user["password"], password):
                    keep_lang = session.get("lang", "en")
                    session.clear()
                    session["lang"] = keep_lang

                    session["role"] = "user"
                    session["code"] = user["code"]
                    session["name"] = user["username"]
                    recompute_quota_for_user(user["code"])
                    return redirect(url_for("user_dashboard"))
                return render_template("login.html", error="Invalid password")

            if len(dealer_match) == 1:
                dealer = dealer_match[0]
                if check_password_hash(dealer["password"], password):
                    keep_lang = session.get("lang", "en")
                    session.clear()
                    session["lang"] = keep_lang

                    session["role"] = "dealer"
                    session["code"] = dealer["code"]
                    session["name"] = dealer["shop_name"]
                    return redirect(url_for("dealer_dashboard"))
                return render_template("login.html", error="Invalid password")

            if len(admin_match) == 1:
                admin = admin_match[0]
                if check_password_hash(admin["password"], password):
                    keep_lang = session.get("lang", "en")
                    session.clear()
                    session["lang"] = keep_lang

                    session["role"] = "admin"
                    session["code"] = admin["code"]
                    session["name"] = admin["username"]
                    return redirect(url_for("admin_dashboard"))
                return render_template("login.html", error="Invalid password")

            return render_template("login.html", error="Login failed")

        except Error as e:
            return render_template("login.html", error=f"Database error: {e}")

        finally:
            cur.close()
            db.close()

    return render_template("login.html", error=error_msg)

# -----------------------------
# Complaint (user)
# -----------------------------
@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    if session.get("role") != "user":
        return redirect(url_for("login"))

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if not text:
            return "Complaint text required"

        db = get_db_connection()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO complaints (user_code, complaint_text, status) VALUES (%s, %s, %s)",
            (session.get("code"), text, "Pending")
        )
        db.commit()
        cur.close()
        db.close()
        return redirect(url_for("user_dashboard"))

    return render_template("complaint.html")

# -----------------------------
# User Dashboard
# -----------------------------
@app.route("/user/dashboard")
def user_dashboard():
    if session.get("role") != "user":
        return redirect(url_for("login"))

    user_code = session.get("code")
    user_name = session.get("name")

    rice_total, rice_available = 0, 0
    wheat_total, wheat_balance = 0, 0
    sugar_total, sugar_balance = 0, 0

    transactions = []
    complaints = []

    shop_name = "Not Assigned"
    dealer_name = "-"
    shop_address = "-"
    shop_lat = "13.0827"
    shop_lng = "80.2707"

    db = get_db_connection()
    cur = db.cursor(dictionary=True)

    try:
        recompute_quota_for_user(user_code)

        cur.execute("""
            SELECT rice_total, rice_available, wheat_total, wheat_balance, sugar_total, sugar_balance
            FROM ration_quota
            WHERE user_code=%s
            LIMIT 1
        """, (user_code,))
        q = cur.fetchone()
        if q:
            rice_total = q.get("rice_total", 0)
            rice_available = q.get("rice_available", 0)
            wheat_total = q.get("wheat_total", 0)
            wheat_balance = q.get("wheat_balance", 0)
            sugar_total = q.get("sugar_total", 0)
            sugar_balance = q.get("sugar_balance", 0)

        cur.execute("""
            SELECT txn_date AS date, shop_name AS shop, item, quantity AS qty
            FROM transactions
            WHERE user_code=%s
            ORDER BY txn_date DESC
            LIMIT 5
        """, (user_code,))
        transactions = cur.fetchall() or []

        cur.execute("""
            SELECT id, complaint_text AS text, status
            FROM complaints
            WHERE user_code=%s
            ORDER BY created_at DESC
            LIMIT 5
        """, (user_code,))
        complaints = cur.fetchall() or []

        cur.execute("""
            SELECT shop_name, dealer_name, address, lat, lng
            FROM shops
            WHERE area = (SELECT area FROM users WHERE code=%s LIMIT 1)
            LIMIT 1
        """, (user_code,))
        s = cur.fetchone()
        if s:
            shop_name = s.get("shop_name", shop_name)
            dealer_name = s.get("dealer_name", dealer_name)
            shop_address = s.get("address", shop_address)
            shop_lat = str(s.get("lat", shop_lat))
            shop_lng = str(s.get("lng", shop_lng))

    finally:
        cur.close()
        db.close()

    return render_template(
        "user_dashboard.html",
        user_name=user_name,
        user_roll=user_code,
        rice_total=rice_total,
        rice_available=rice_available,
        wheat_total=wheat_total,
        wheat_balance=wheat_balance,
        sugar_total=sugar_total,
        sugar_balance=sugar_balance,
        transactions=transactions,
        complaints=complaints,
        shop_name=shop_name,
        dealer_name=dealer_name,
        shop_address=shop_address,
        shop_lat=shop_lat,
        shop_lng=shop_lng
    )

# -----------------------------
# Manage Family Members (USER)
# -----------------------------
@app.route("/manage-members", methods=["GET", "POST"])
def manage_members():
    if session.get("role") != "user":
        return redirect(url_for("login"))

    user_code = session.get("code")

    db = get_db_connection()
    cur = db.cursor(dictionary=True)

    try:
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            relation = request.form.get("relation", "").strip()
            age = request.form.get("age", "").strip()

            if name and relation and age.isdigit():
                cur.execute(
                    """
                    INSERT INTO family_members (user_code, member_name, relation, age, status, delete_request)
                    VALUES (%s, %s, %s, %s, 'Pending', 0)
                    """,
                    (user_code, name, relation, int(age))
                )
                db.commit()

        cur.execute(
            "SELECT id, member_name, relation, age, status, delete_request FROM family_members WHERE user_code=%s ORDER BY id DESC",
            (user_code,)
        )
        members = cur.fetchall() or []

    finally:
        cur.close()
        db.close()

    return render_template("manage_members.html", members=members)

@app.route("/member/request-delete/<int:mid>", methods=["POST"])
def request_delete_member(mid):
    if session.get("role") != "user":
        return redirect(url_for("login"))

    user_code = session.get("code")

    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute("""
            UPDATE family_members
            SET delete_request=1
            WHERE id=%s AND user_code=%s AND status='Approved'
            LIMIT 1
        """, (mid, user_code))
        db.commit()
    finally:
        cur.close()
        db.close()

    return redirect(url_for("manage_members"))

# -----------------------------
# Dealer Dashboard
# -----------------------------
@app.route("/dealer_dashboard")
def dealer_dashboard():
    if session.get("role") != "dealer":
        return redirect(url_for("login"))

    dealer_code = session.get("code")
    dealer_name = session.get("name")

    stock = {"Rice": 0, "Wheat": 0, "Sugar": 0}
    complaints = []

    db = get_db_connection()
    cur = db.cursor(dictionary=True)

    try:
        cur.execute("""
            INSERT IGNORE INTO dealer_stock (dealer_code, rice, wheat, sugar)
            VALUES (%s, 0, 0, 0)
        """, (dealer_code,))
        db.commit()

        cur.execute("SELECT rice, wheat, sugar FROM dealer_stock WHERE dealer_code=%s", (dealer_code,))
        s = cur.fetchone() or {}
        stock = {"Rice": s.get("rice", 0), "Wheat": s.get("wheat", 0), "Sugar": s.get("sugar", 0)}

        cur.execute("""
            SELECT id, user_code, complaint_text, status
            FROM complaints
            ORDER BY id DESC
            LIMIT 20
        """)
        complaints = cur.fetchall() or []

    finally:
        cur.close()
        db.close()

    return render_template("dealer.html", dealer_name=dealer_name, dealer_code=dealer_code, stock=stock, complaints=complaints)

# ✅ IMPORTANT FIX: explicit endpoint name (prevents overwrite error)
@app.route("/dealer/update_stock", methods=["POST"], endpoint="dealer_update_stock")
def dealer_update_stock():
    if session.get("role") != "dealer":
        return redirect(url_for("login"))

    dealer_code = session.get("code")
    item = request.form.get("item", "").strip()
    new_qty = request.form.get("new_qty", "").strip()

    if not new_qty.isdigit():
        return "Invalid quantity"

    column_map = {"Rice": "rice", "Wheat": "wheat", "Sugar": "sugar"}
    if item not in column_map:
        return "Invalid item selected"

    column = column_map[item]
    new_qty = int(new_qty)

    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute("""
            INSERT IGNORE INTO dealer_stock (dealer_code, rice, wheat, sugar)
            VALUES (%s, 0, 0, 0)
        """, (dealer_code,))
        cur.execute(f"UPDATE dealer_stock SET {column}=%s WHERE dealer_code=%s", (new_qty, dealer_code))
        db.commit()
    finally:
        cur.close()
        db.close()

    return redirect(url_for("dealer_dashboard"))

@app.route("/dealer/resolve_complaint/<int:cid>", methods=["POST"])
def dealer_resolve_complaint(cid):
    if session.get("role") != "dealer":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute("UPDATE complaints SET status='Resolved' WHERE id=%s", (cid,))
        db.commit()
    finally:
        cur.close()
        db.close()

    return redirect(url_for("dealer_dashboard"))

# -----------------------------
# Admin Dashboard
# -----------------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    admin_code = session.get("code")
    admin_name = session.get("name")

    total_users = 0
    total_dealers = 0
    pending_complaints = 0

    pending_accounts = []
    stocks = []
    complaints = []

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute("SELECT COUNT(*) AS c FROM users")
        total_users = (cur.fetchone() or {}).get("c", 0)

        cur.execute("SELECT COUNT(*) AS c FROM dealers")
        total_dealers = (cur.fetchone() or {}).get("c", 0)

        cur.execute("SELECT COUNT(*) AS c FROM complaints WHERE status='Pending'")
        pending_complaints = (cur.fetchone() or {}).get("c", 0)

        try:
            cur.execute("""
                SELECT id, user_code, complaint_text, status, resolution
                FROM complaints
                ORDER BY id DESC
                LIMIT 50
            """)
            complaints = cur.fetchall() or []
        except Exception:
            cur.execute("""
                SELECT id, user_code, complaint_text, status, NULL AS resolution
                FROM complaints
                ORDER BY id DESC
                LIMIT 50
            """)
            complaints = cur.fetchall() or []

    finally:
        cur.close()
        db.close()

    return render_template(
        "admin.html",
        admin_name=admin_name,
        admin_code=admin_code,
        total_users=total_users,
        total_dealers=total_dealers,
        pending_complaints=pending_complaints,
        pending_accounts=pending_accounts,
        stocks=stocks,
        complaints=complaints,
        report_year=datetime.now().year
    )

# -----------------------------
# ✅ ADMIN: Member Approvals page
# -----------------------------
@app.route("/admin/members")
def admin_members():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT id, user_code, member_name, relation, age, status, delete_request
            FROM family_members
            WHERE status='Pending'
            ORDER BY id DESC
        """)
        pending_members = cur.fetchall() or []

        cur.execute("""
            SELECT id, user_code, member_name, relation, age, status, delete_request
            FROM family_members
            WHERE delete_request=1 AND status='Approved'
            ORDER BY id DESC
        """)
        delete_requests = cur.fetchall() or []

    finally:
        cur.close()
        db.close()

    return render_template("admin_members.html", pending=pending_members, delete_requests=delete_requests)

@app.route("/admin/members/approve/<int:mid>", methods=["POST"])
def admin_approve_member(mid):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute("SELECT user_code FROM family_members WHERE id=%s LIMIT 1", (mid,))
        row = cur.fetchone()
        if not row:
            return redirect(url_for("admin_members"))

        user_code = row["user_code"]

        cur2 = db.cursor()
        cur2.execute("UPDATE family_members SET status='Approved' WHERE id=%s", (mid,))
        db.commit()
        cur2.close()

        recompute_quota_for_user(user_code)

    finally:
        cur.close()
        db.close()

    return redirect(url_for("admin_members"))

@app.route("/admin/members/reject/<int:mid>", methods=["POST"])
def admin_reject_member(mid):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute("SELECT user_code FROM family_members WHERE id=%s LIMIT 1", (mid,))
        row = cur.fetchone()
        user_code = row["user_code"] if row else None

        cur2 = db.cursor()
        cur2.execute("UPDATE family_members SET status='Rejected' WHERE id=%s", (mid,))
        db.commit()
        cur2.close()

        if user_code:
            recompute_quota_for_user(user_code)

    finally:
        cur.close()
        db.close()

    return redirect(url_for("admin_members"))

@app.route("/admin/members/approve-delete/<int:mid>", methods=["POST"])
def admin_approve_delete_member(mid):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute("SELECT user_code FROM family_members WHERE id=%s LIMIT 1", (mid,))
        row = cur.fetchone()
        if not row:
            return redirect(url_for("admin_members"))

        user_code = row["user_code"]

        cur2 = db.cursor()
        cur2.execute("DELETE FROM family_members WHERE id=%s", (mid,))
        db.commit()
        cur2.close()

        recompute_quota_for_user(user_code)

    finally:
        cur.close()
        db.close()

    return redirect(url_for("admin_members"))

# -----------------------------
# Admin actions required by admin.html
# -----------------------------
@app.route("/admin/approve/<int:user_id>")
def approve_account(user_id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/deactivate/<int:user_id>")
def deactivate_account(user_id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/update_stock/<int:stock_id>", methods=["POST"])
def update_stock(stock_id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/resolve_complaint/<int:complaint_id>", methods=["POST"])
def resolve_complaint(complaint_id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    status = request.form.get("status", "Pending").strip()
    resolution = request.form.get("resolution", "").strip()

    db = get_db_connection()
    cur = db.cursor()
    try:
        try:
            cur.execute(
                "UPDATE complaints SET status=%s, resolution=%s WHERE id=%s",
                (status, resolution, complaint_id)
            )
        except Exception:
            cur.execute(
                "UPDATE complaints SET status=%s WHERE id=%s",
                (status, complaint_id)
            )
        db.commit()
    finally:
        cur.close()
        db.close()

    return redirect(url_for("admin_dashboard"))

@app.route("/user/transactions")
def user_transactions():
    if session.get("role") != "user" or "code" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)

    try:
        cur.execute("""
            SELECT id, txn_date, shop_name, item, quantity, dealer_code, price
            FROM transactions
            WHERE UPPER(user_code) = %s
            ORDER BY txn_date DESC, id DESC
        """, (session["code"].upper(),))

        transactions = cur.fetchall() or []

    finally:
        cur.close()
        db.close()

    return render_template("user_transactions.html", transactions=transactions)

# -----------------------------
# ✅ Transaction History (ADMIN - ALL USERS)
# -----------------------------
@app.route("/admin/transactions")
def admin_transactions():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT
              id,
              user_code,
              item,
              quantity,
              DATE_FORMAT(txn_date, '%Y-%m-%d %H:%i:%s') AS txn_datetime,
              COALESCE(dealer_code, '-') AS dealer_code
            FROM transactions
            ORDER BY txn_date DESC
        """)
        txns = cur.fetchall() or []
    finally:
        cur.close()
        db.close()

    return render_template("admin_transaction_history.html", txns=txns)

@app.route("/dealer/purchase", methods=["POST"])
def dealer_purchase():
    if session.get("role") != "dealer":
        return redirect(url_for("login"))

    user_code = (request.form.get("user_code") or "").strip().upper()
    item = (request.form.get("item") or "").strip().title()
    qty_str = (request.form.get("quantity") or "").strip()

    if not user_code or not item or not qty_str:
        return "Missing fields"

    try:
        qty = float(qty_str)
    except ValueError:
        return "Invalid quantity"

    if qty <= 0:
        return "Quantity must be > 0"

    if item not in ["Rice", "Wheat", "Sugar"]:
        return "Invalid item"

    dealer_code = session.get("code")
    shop_name = session.get("name")

    db = get_db_connection()
    cur = db.cursor(dictionary=True)

    try:
        cur.execute("SELECT code FROM users WHERE code=%s LIMIT 1", (user_code,))
        if not cur.fetchone():
            return "User not found"

        quota_col = {"Rice": "rice_available", "Wheat": "wheat_balance", "Sugar": "sugar_balance"}[item]
        cur.execute(f"SELECT {quota_col} AS bal FROM ration_quota WHERE user_code=%s LIMIT 1", (user_code,))
        q = cur.fetchone()
        if not q:
            return "Quota not found for this user"
        if float(q["bal"]) < qty:
            return f"Insufficient {item} quota. Balance: {q['bal']}"

        stock_col = {"Rice": "rice", "Wheat": "wheat", "Sugar": "sugar"}[item]
        cur.execute(f"SELECT {stock_col} AS s FROM dealer_stock WHERE dealer_code=%s LIMIT 1", (dealer_code,))
        s = cur.fetchone() or {"s": 0}
        if float(s["s"]) < qty:
            return f"Dealer stock insufficient for {item}. Stock: {s['s']}"

        cur2 = db.cursor()
        cur2.execute(f"UPDATE ration_quota SET {quota_col} = {quota_col} - %s WHERE user_code=%s", (qty, user_code))
        cur2.execute(f"UPDATE dealer_stock SET {stock_col} = {stock_col} - %s WHERE dealer_code=%s", (qty, dealer_code))

        cur2.execute("""
            INSERT INTO transactions (user_code, shop_name, dealer_code, item, quantity, txn_date)
            VALUES (%s,%s,%s,%s,%s,NOW())
        """, (user_code, shop_name, dealer_code, item, str(qty)))

        db.commit()
        cur2.close()

    except Exception as e:
        db.rollback()
        return f"Purchase failed: {e}"

    finally:
        cur.close()
        db.close()

    return redirect(url_for("dealer_dashboard"))

# -----------------------------
# ADMIN : Dealer Management
# -----------------------------
@app.route("/admin/dealers")
def admin_dealers():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT id, code, shop_name, area, COALESCE(status,'Pending') AS status
            FROM dealers
            ORDER BY id DESC
        """)
        dealers = cur.fetchall() or []

        cur.execute("""
            SELECT COUNT(*) AS c
            FROM dealers
            WHERE COALESCE(status,'Pending')='Pending'
        """)
        pending_count = (cur.fetchone() or {}).get("c", 0)

    finally:
        cur.close()
        db.close()

    return render_template("admin_dealers.html", dealers=dealers, pending_count=pending_count)

@app.route("/admin/dealers/approve/<int:did>", methods=["POST"])
def admin_approve_dealer(did):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute("UPDATE dealers SET status='Approved' WHERE id=%s", (did,))
        db.commit()
    finally:
        cur.close()
        db.close()

    return redirect(url_for("admin_dealers"))

@app.route("/admin/dealers/reject/<int:did>", methods=["POST"])
def admin_reject_dealer(did):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute("UPDATE dealers SET status='Rejected' WHERE id=%s", (did,))
        db.commit()
    finally:
        cur.close()
        db.close()

    return redirect(url_for("admin_dealers"))

# ===============================
# ADMIN – STOCK MONITORING
# ===============================
@app.route("/admin/stocks", methods=["GET"])
def admin_stocks():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT dealer_code, rice, wheat, sugar
        FROM dealer_stock
        ORDER BY dealer_code
    """)
    stocks = cur.fetchall() or []

    cur.close()
    db.close()
    return render_template("admin_stocks.html", stocks=stocks)

@app.route("/dealer/stock/update", methods=["POST"])
def dealer_stock_update():
    if session.get("role") != "dealer":
        return redirect(url_for("login"))

    dealer_code = session.get("code")  # ex: DL001
    item_name = request.form.get("item_name", "").strip()
    qty_change = float(request.form.get("qty_change", "0"))
    unit = request.form.get("unit", "Kg").strip()
    action_type = request.form.get("action_type", "ADD").strip().upper()
    note = request.form.get("note", "").strip()

    db = get_db_connection()
    cur = db.cursor(dictionary=True)

    # 1) Get current stock row (NOTE: this expects dealer_stock with columns dealer_code,item_name,qty,unit)
    cur.execute("""
        SELECT qty FROM dealer_stock
        WHERE dealer_code=%s AND item_name=%s
    """, (dealer_code, item_name))
    row = cur.fetchone()

    current_qty = float(row["qty"]) if row else 0.0

    if action_type == "ADD":
        new_qty = current_qty + qty_change
    elif action_type == "REMOVE":
        new_qty = current_qty - qty_change
        if new_qty < 0:
            cur.close()
            db.close()
            return "Stock cannot go below 0", 400
    elif action_type == "SET":
        new_qty = qty_change
    else:
        cur.close()
        db.close()
        return "Invalid action_type", 400

    # 2) Upsert dealer_stock
    cur.execute("""
        INSERT INTO dealer_stock (dealer_code, item_name, qty, unit)
        VALUES (%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE qty=%s, unit=%s
    """, (dealer_code, item_name, new_qty, unit, new_qty, unit))

    # 3) Insert log (admin monitoring)
    cur.execute("""
        INSERT INTO stock_logs (dealer_code, item_name, qty_change, unit, action_type, note)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (dealer_code, item_name, qty_change, unit, action_type, note))

    db.commit()
    cur.close()
    db.close()

    return redirect(url_for("dealer_dashboard"))

@app.route("/admin/slots", methods=["GET"])
def admin_slots():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("""
      SELECT s.*,
        (SELECT COUNT(*) FROM slot_bookings b
         WHERE b.slot_id=s.id AND b.status='BOOKED') AS booked_count
      FROM slots s
      ORDER BY s.slot_date DESC, s.start_time DESC
    """)
    slots = cur.fetchall() or []

    slot_ids = [s["id"] for s in slots]
    bookings_by_slot = {sid: [] for sid in slot_ids}

    if slot_ids:
        placeholders = ",".join(["%s"] * len(slot_ids))
        cur.execute(f"""
          SELECT
            b.id AS booking_id,
            b.slot_id,
            b.status,
            b.created_at,
            u.username AS user_name,
            u.code AS user_code
          FROM slot_bookings b
          LEFT JOIN users u ON u.id = b.user_id
          WHERE b.slot_id IN ({placeholders})
          ORDER BY b.created_at DESC
        """, slot_ids)
        for row in cur.fetchall() or []:
            # ensure JSON-serializable values
            if row.get("created_at") is not None:
                row["created_at"] = str(row["created_at"])
            bookings_by_slot.setdefault(row["slot_id"], []).append(row)

    for s in slots:
        s["bookings"] = bookings_by_slot.get(s["id"], [])

    cur.close(); db.close()
    return render_template("admin_slots.html", slots=slots)

@app.route("/admin/slots/create", methods=["POST"])
def admin_slots_create():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    slot_date = request.form.get("slot_date")      # YYYY-MM-DD
    start_time = request.form.get("start_time")    # HH:MM
    end_time = request.form.get("end_time")        # HH:MM
    max_bookings = int(request.form.get("max_bookings","1"))

    if not slot_date or not start_time or not end_time or max_bookings <= 0:
        return "Invalid input", 400

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
      INSERT INTO slots (slot_date, start_time, end_time, max_bookings, is_active)
      VALUES (%s,%s,%s,%s,1)
    """, (slot_date, start_time, end_time, max_bookings))
    db.commit()
    cur.close(); db.close()
    return redirect(url_for("admin_slots"))

@app.route("/slots", methods=["GET"])
def slots_list():
    if session.get("role") != "user":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("""
      SELECT s.*,
        (SELECT COUNT(*) FROM slot_bookings b
         WHERE b.slot_id=s.id AND b.status='BOOKED') AS booked_count
      FROM slots s
      WHERE s.is_active=1 AND s.slot_date >= CURDATE()
      ORDER BY s.slot_date, s.start_time
    """)
    slots = cur.fetchall() or []
    cur.close(); db.close()
    return render_template("user_slots.html", slots=slots)

def _book_slot(slot_id):
    if session.get("role") != "user":
        return redirect(url_for("login"))

    if not slot_id:
        return "Invalid slot", 400

    user_code = session.get("code")
    if not user_code:
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)

    # find numeric user id for bookings
    cur.execute("SELECT id FROM users WHERE code=%s LIMIT 1", (user_code,))
    user_row = cur.fetchone()
    if not user_row:
        cur.close(); db.close()
        return redirect(url_for("login"))
    user_id = user_row["id"]

    # capacity check
    cur.execute("SELECT max_bookings, is_active, slot_date FROM slots WHERE id=%s", (slot_id,))
    s = cur.fetchone()
    if not s or s["is_active"] != 1:
        cur.close(); db.close()
        return "Slot not available", 400

    cur.execute("""
      SELECT COUNT(*) AS c FROM slot_bookings
      WHERE slot_id=%s AND status='BOOKED'
    """, (slot_id,))
    booked = cur.fetchone()["c"]

    if booked >= s["max_bookings"]:
        cur.close(); db.close()
        return "Slot full", 400

    # book
    try:
        cur.execute("""
          INSERT INTO slot_bookings (slot_id, user_id, status)
          VALUES (%s,%s,'BOOKED')
        """, (slot_id, user_id))
        db.commit()
    except Exception:
        # already booked etc.
        db.rollback()

    cur.close(); db.close()
    return redirect(url_for("slots_list"))

@app.route("/slots/book", methods=["POST"], endpoint="slot_book")
def slot_book():
    slot_id = request.form.get("slot_id", type=int)
    return _book_slot(slot_id)

@app.route("/slots/book/<int:slot_id>", methods=["POST"])
def slots_book(slot_id):
    return _book_slot(slot_id)

@app.route("/admin/slots/create", methods=["POST"])
def admin_create_slot():
    # insert slot logic
    return redirect(url_for("admin_slots"))

@app.route("/admin/slots/toggle/<int:slot_id>", methods=["POST"])
def admin_toggle_slot(slot_id):
    # change active/inactive
    return redirect(url_for("admin_slots"))

@app.route("/admin/slots/delete/<int:slot_id>", methods=["POST"])
def admin_delete_slot(slot_id):
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    db = get_db_connection()
    cur = db.cursor()
    try:
        # delete dependent bookings first to avoid FK issues
        cur.execute("DELETE FROM slot_bookings WHERE slot_id=%s", (slot_id,))
        cur.execute("DELETE FROM slots WHERE id=%s", (slot_id,))
        db.commit()
    except Exception:
        db.rollback()
    finally:
        cur.close()
        db.close()
    return redirect(url_for("admin_slots"))


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
