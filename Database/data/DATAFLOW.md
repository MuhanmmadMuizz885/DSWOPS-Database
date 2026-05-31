# Dataflow Description — DSWOPS
**Project:** Document Scanner & Work Order Processing System — Peshawar Zoo  
**Author:** Muhammad Muizz  
**Milestone:** 3

---

## Step 1 — Data Entry
An authenticated Employee logs into the DSWOPS web interface and uploads a scanned
document (image or PDF). This creates a new row in the Document table with:
DocumentID (auto), FilePath, UploadDate (today), Status = 'uploaded',
DocumentType (selected by user), and EmployeeID (logged-in user).

## Step 2 — OCR Processing
The OCR pipeline (EasyOCR / PaddleOCR) processes the stored file. For every field
it detects — such as RecipientName, OrderDate, ItemDescription — one new row is
inserted into ExtractedData with DocumentID (FK), FieldName, FieldValue, and
ConfidenceScore. Document.Status is then updated to 'processed'.

## Step 3 — Verification
The responsible Employee reviews the extracted fields on screen. If correct,
Document.Status is set to 'verified'. If wrong, Status is set to 'rejected'
and the document can be re-uploaded. Every status change is written to AuditLog
with Action = 'update_status', current Timestamp, and EmployeeID.

## Step 4 — Work Order Creation
For verified documents that require action, the Employee creates a WorkOrder linked
to the Document (FK), assigns a Supplier from the Supplier table (FK), and sets
Status = 'pending'. The creation event is recorded in AuditLog with
Action = 'create_workorder'.

## Step 5 — Work Order Lifecycle
As the work progresses, WorkOrder.Status moves through:
pending → in_progress → completed.
Each status change creates a new AuditLog entry. Supplier details are always
looked up via SupplierID FK — never duplicated inside WorkOrder.

## Step 6 — Output
Staff can query:
- All pending work orders grouped by supplier
- OCR confidence scores by document type
- Full audit trail for any document or work order
Results are shown in the frontend or exported as CSV/PDF reports.

---

## Data Load Order (FK dependency)
| Order | Table         | Depends On                    |
|-------|---------------|-------------------------------|
| 1     | Employee      | None                          |
| 2     | Supplier      | None                          |
| 3     | Document      | Employee                      |
| 4     | ExtractedData | Document                      |
| 5     | WorkOrder     | Employee, Supplier, Document  |
| 6     | AuditLog      | Employee, WorkOrder           |