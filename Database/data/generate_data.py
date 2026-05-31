# DSWOPS — Milestone 3: Synthetic Data Generator
# Author : Muhammad Muizz
# Course : Database Systems Lab | Mr. Ali Hassan
# Run    : python generate_data.py
# Output : 6 CSV files in the same folder
# Requires: pip install faker


from faker import Faker
import csv, random, os

fake = Faker()
random.seed(42)
Faker.seed(42)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Helper 
def write_csv(filename, fieldnames, rows):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {len(rows):>4} rows → {filename}")


# 1. employees.csv

ROLES = ["Admin", "Manager", "Staff", "Supervisor"]

employees = []
for i in range(1, 21):
    employees.append({
        "EmployeeID" : i,
        "Name"       : fake.name(),
        "Role"       : random.choice(ROLES),
        "Email"      : fake.unique.email(),
    })

write_csv("employees.csv",
          ["EmployeeID", "Name", "Role", "Email"],
          employees)


# 2. suppliers.csv   

pk_area_codes = ["021", "042", "051", "061", "081", "091"]

suppliers = []
for i in range(1, 16):
    area = random.choice(pk_area_codes)
    number = f"+92-{area}-{random.randint(1000000, 9999999)}"
    suppliers.append({
        "SupplierID" : i,
        "Name"       : fake.company(),
        "Contact"    : number,
        "Address"    : fake.address().replace("\n", ", "),
    })

write_csv("suppliers.csv",
          ["SupplierID", "Name", "Contact", "Address"],
          suppliers)


# 3. documents.csv   

DOC_STATUSES  = ["uploaded", "processed", "verified", "rejected"]
DOC_TYPES     = ["OfficeOrder", "Letter", "WorkOrder", "Invoice", "Report"]

documents = []
for i in range(1, 81):
    documents.append({
        "DocumentID"   : i,
        "FilePath"     : f"/uploads/{fake.uuid4()}.pdf",
        "UploadDate"   : fake.date_between(start_date="-1y", end_date="today").isoformat(),
        "Status"       : random.choice(DOC_STATUSES),
        "DocumentType" : random.choice(DOC_TYPES),
        "EmployeeID"   : random.randint(1, 20),
    })

write_csv("documents.csv",
          ["DocumentID", "FilePath", "UploadDate", "Status", "DocumentType", "EmployeeID"],
          documents)


# 4. extracted_data.csv   


FIELD_NAMES = [
    "RecipientName", "OrderDate", "ItemDescription",
    "Quantity", "UnitPrice", "TotalAmount",
    "ReferenceNumber", "IssueDate", "AuthorizedBy", "Department",
]

extracted_data = []
extract_id = 1
for doc in documents:
    # each document gets 1 or 2 extracted fields
    num_fields = random.randint(1, 3)
    chosen_fields = random.sample(FIELD_NAMES, min(num_fields, len(FIELD_NAMES)))
    for field in chosen_fields:
        extracted_data.append({
            "ExtractID"       : extract_id,
            "DocumentID"      : doc["DocumentID"],
            "FieldName"       : field,
            "FieldValue"      : fake.sentence(nb_words=4).rstrip("."),
            "ConfidenceScore" : round(random.uniform(60.00, 99.99), 2),
        })
        extract_id += 1

write_csv("extracted_data.csv",
          ["ExtractID", "DocumentID", "FieldName", "FieldValue", "ConfidenceScore"],
          extracted_data)


# 5. work_orders.csv


WO_STATUSES = ["pending", "in_progress", "completed", "cancelled"]

# Only use verified documents for work orders (realistic)
verified_doc_ids = [d["DocumentID"] for d in documents if d["Status"] == "verified"]
if len(verified_doc_ids) < 60:          # fallback if seed gives fewer verified docs
    verified_doc_ids = [d["DocumentID"] for d in documents]

work_orders = []
for i in range(1, 61):
    work_orders.append({
        "WorkOrderID" : i,
        "Description" : fake.sentence(nb_words=8).rstrip("."),
        "Status"      : random.choice(WO_STATUSES),
        "CreatedDate" : fake.date_between(start_date="-6m", end_date="today").isoformat(),
        "SupplierID"  : random.randint(1, 15),
        "EmployeeID"  : random.randint(1, 20),
        "DocumentID"  : random.choice(verified_doc_ids),
    })

write_csv("work_orders.csv",
          ["WorkOrderID", "Description", "Status", "CreatedDate",
           "SupplierID", "EmployeeID", "DocumentID"],
          work_orders)


# 6. audit_logs.csv   

ACTIONS = [
    "upload_document", "update_status", "create_workorder",
    "update_workorder", "complete_workorder", "reject_document",
]

audit_logs = []
for i in range(1, 101):
    audit_logs.append({
        "LogID"       : i,
        "Action"      : random.choice(ACTIONS),
        "Timestamp"   : fake.date_time_between(start_date="-6m", end_date="now").isoformat(sep=" "),
        "EmployeeID"  : random.randint(1, 20),
        "WorkOrderID" : random.randint(1, 60),
    })

write_csv("audit_logs.csv",
          ["LogID", "Action", "Timestamp", "EmployeeID", "WorkOrderID"],
          audit_logs)


print("\nDone! All 6 CSV files generated successfully.")
print("Load order for MySQL: employees → suppliers → documents → extracted_data → work_orders → audit_logs")
