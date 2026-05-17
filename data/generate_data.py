# ============================================================
# DSWOPS Synthetic Data Generator
# Project  : Document Scanner & Work Order Processing System
# Author   : Muhammad Muizz
# Milestone: 3
# ============================================================

from faker import Faker
import csv, random, os

fake = Faker()
random.seed(42)
Faker.seed(42)

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── 1. Employees (20 rows) ────────────────────────────────────
roles = ["Admin", "Manager", "Staff", "Supervisor"]
employees = []
for i in range(1, 21):
    employees.append({
        "EmployeeID": i,
        "Name":       fake.name(),
        "Role":       random.choice(roles),
        "Email":      fake.unique.email()
    })

with open(f"{OUTPUT_DIR}/employees.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["EmployeeID","Name","Role","Email"])
    w.writeheader(); w.writerows(employees)

# ── 2. Suppliers (15 rows) ────────────────────────────────────
suppliers = []
for i in range(1, 16):
    suppliers.append({
        "SupplierID": i,
        "Name":       fake.company(),
        "Contact":    fake.numerify("03#########"),
        "Address":    fake.address().replace("\n", ", ")
    })

with open(f"{OUTPUT_DIR}/suppliers.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["SupplierID","Name","Contact","Address"])
    w.writeheader(); w.writerows(suppliers)

# ── 3. Documents (80 rows) ────────────────────────────────────
statuses   = ["uploaded","processed","verified","rejected"]
doc_types  = ["OfficeOrder","Letter","WorkOrder","Invoice","Report"]
documents  = []
for i in range(1, 81):
    documents.append({
        "DocumentID":   i,
        "FilePath":     f"/uploads/{fake.uuid4()}.pdf",
        "UploadDate":   fake.date_between("-1y","today").isoformat(),
        "Status":       random.choice(statuses),
        "DocumentType": random.choice(doc_types),
        "EmployeeID":   random.randint(1, 20)
    })

with open(f"{OUTPUT_DIR}/documents.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["DocumentID","FilePath","UploadDate","Status","DocumentType","EmployeeID"])
    w.writeheader(); w.writerows(documents)

# ── 4. ExtractedData (160 rows) ──────────────────────────────
field_names = ["RecipientName","OrderDate","ItemDescription","TotalAmount",
               "IssuerName","ReferenceNumber","DepartmentName","ContactNumber"]
extracted   = []
eid = 1
for doc in documents:
    for _ in range(2):
        extracted.append({
            "ExtractID":       eid,
            "DocumentID":      doc["DocumentID"],
            "FieldName":       random.choice(field_names),
            "FieldValue":      fake.sentence(nb_words=4),
            "ConfidenceScore": round(random.uniform(70.0, 99.9), 2)
        })
        eid += 1

with open(f"{OUTPUT_DIR}/extracted_data.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["ExtractID","DocumentID","FieldName","FieldValue","ConfidenceScore"])
    w.writeheader(); w.writerows(extracted)

# ── 5. WorkOrders (60 rows) ───────────────────────────────────
wo_statuses = ["pending","in_progress","completed","cancelled"]
workorders  = []
verified_docs = [d["DocumentID"] for d in documents if d["Status"] == "verified"]
if len(verified_docs) < 60:
    verified_docs = [d["DocumentID"] for d in documents]

for i in range(1, 61):
    workorders.append({
        "WorkOrderID": i,
        "Description": fake.sentence(nb_words=8),
        "Status":      random.choice(wo_statuses),
        "CreatedDate": fake.date_between("-6m","today").isoformat(),
        "SupplierID":  random.randint(1, 15),
        "EmployeeID":  random.randint(1, 20),
        "DocumentID":  random.choice(verified_docs)
    })

with open(f"{OUTPUT_DIR}/work_orders.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["WorkOrderID","Description","Status","CreatedDate","SupplierID","EmployeeID","DocumentID"])
    w.writeheader(); w.writerows(workorders)

# ── 6. AuditLogs (100 rows) ───────────────────────────────────
actions    = ["create_document","update_status","create_workorder",
              "verify_document","reject_document","complete_workorder"]
auditlogs  = []
for i in range(1, 101):
    auditlogs.append({
        "LogID":       i,
        "Action":      random.choice(actions),
        "Timestamp":   fake.date_time_between("-6m","now").strftime("%Y-%m-%d %H:%M:%S"),
        "EmployeeID":  random.randint(1, 20),
        "WorkOrderID": random.randint(1, 60)
    })

with open(f"{OUTPUT_DIR}/audit_logs.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["LogID","Action","Timestamp","EmployeeID","WorkOrderID"])
    w.writeheader(); w.writerows(auditlogs)

print("All 6 CSV files generated successfully.")