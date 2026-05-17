# Normalization Walkthrough — DSWOPS
**Project:** Document Scanner & Work Order Processing System — Peshawar Zoo  
**Author:** Muhammad Muizz  
**Milestone:** 2

---

## First Normal Form (1NF)
A table is in 1NF if all columns hold atomic values, every row is unique, and there are no repeating groups.

**Employee** — EmployeeID, Name, Role, Email are all atomic single-valued fields. EmployeeID is a unique surrogate key. Already in 1NF. No change required.

**Document** — DocumentID, FilePath, UploadDate, Status, EmployeeID are all atomic. Status stores a single string value. Already in 1NF. No change required.

**ExtractedData** — Each OCR result is stored as one row per field-value pair. No arrays or lists embedded. Already in 1NF by design.

**Supplier** — SupplierID, Name, Contact, Address are all atomic scalars. Already in 1NF. No change required.

**WorkOrder** — All seven columns are atomic. Status is a single string. Already in 1NF. No change required.

**AuditLog** — LogID, Action, Timestamp, EmployeeID, WorkOrderID are all atomic. Already in 1NF. No change required.

---

## Second Normal Form (2NF)
A table is in 2NF if it is in 1NF and every non-key attribute is fully dependent on the entire primary key. Partial dependencies only occur with composite keys.

**Employee** — Single-column PK (EmployeeID). Name, Role, Email all depend fully on EmployeeID. No composite key so partial dependency is impossible. Already in 2NF.

**Document** — Single-column PK (DocumentID). All attributes depend fully on DocumentID. Already in 2NF.

**ExtractedData** — Single-column PK (ExtractID). All attributes depend fully on ExtractID. Already in 2NF.

**Supplier** — Single-column PK (SupplierID). Name, Contact, Address all depend solely on SupplierID. Already in 2NF.

**WorkOrder** — Single-column PK (WorkOrderID). All attributes depend fully on WorkOrderID. Already in 2NF.

**AuditLog** — Single-column PK (LogID). Action, Timestamp, EmployeeID, WorkOrderID all depend fully on LogID. Already in 2NF.

---

## Third Normal Form (3NF)
A table is in 3NF if it is in 2NF and no non-key attribute is transitively dependent on the primary key.

**Employee** — Role is a descriptive label only and does not determine any other stored attribute. Name and Email are personal to the individual, not derived from Role. No transitive dependency. Already in 3NF.

**Document** — Status is determined by DocumentID directly, not by FilePath or UploadDate. EmployeeID is an FK reference and does not cause a transitive dependency since no employee attribute is stored here. Already in 3NF.

**ExtractedData** — ConfidenceScore is per extraction record, not per FieldName. All attributes depend directly on ExtractID. No transitive dependency. Already in 3NF.

**Supplier** — Contact is a direct supplier attribute, not derived from Address. No transitive dependency. Already in 3NF.

**WorkOrder** — Supplier details live in the Supplier table; WorkOrder only stores SupplierID as an FK. No supplier attribute is repeated here. No transitive dependency. Already in 3NF.

**AuditLog** — Action and Timestamp are independent facts about the log event. EmployeeID and WorkOrderID are FK references only — no attributes of those entities are stored inside AuditLog. Already in 3NF.

---

## Schema Changes After Normalization Review
1. Added `DocumentType` column (VARCHAR 50, NOT NULL) to the Document table to explicitly distinguish document categories (OfficeOrder, Letter, WorkOrder, Invoice, Report).
2. Formalized a CHECK constraint on Document.Status restricting values to: uploaded, processed, verified, rejected.