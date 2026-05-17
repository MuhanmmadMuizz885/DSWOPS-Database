-- ============================================================
-- DSWOPS DML Script
-- Project  : Document Scanner & Work Order Processing System
-- Author   : Muhammad Muizz
-- Milestone: 5
-- ============================================================

-- ── LOAD DATA (in FK-safe order) ─────────────────────────────

LOAD DATA INFILE '/var/lib/mysql-files/employees.csv'
INTO TABLE Employee
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(EmployeeID, Name, Role, Email);

LOAD DATA INFILE '/var/lib/mysql-files/suppliers.csv'
INTO TABLE Supplier
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(SupplierID, Name, Contact, Address);

LOAD DATA INFILE '/var/lib/mysql-files/documents.csv'
INTO TABLE Document
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(DocumentID, FilePath, UploadDate, Status, DocumentType, EmployeeID);

LOAD DATA INFILE '/var/lib/mysql-files/extracted_data.csv'
INTO TABLE ExtractedData
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(ExtractID, DocumentID, FieldName, FieldValue, ConfidenceScore);

LOAD DATA INFILE '/var/lib/mysql-files/work_orders.csv'
INTO TABLE WorkOrder
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(WorkOrderID, Description, Status, CreatedDate, SupplierID, EmployeeID, DocumentID);

LOAD DATA INFILE '/var/lib/mysql-files/audit_logs.csv'
INTO TABLE AuditLog
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(LogID, Action, Timestamp, EmployeeID, WorkOrderID);

-- ── UPDATE examples ───────────────────────────────────────────

UPDATE WorkOrder
SET Status = 'completed'
WHERE WorkOrderID = 12;

UPDATE Employee
SET Role = 'Manager'
WHERE Email = 'admin@zoo.gov.pk';

-- ── DELETE example ────────────────────────────────────────────

DELETE FROM Document
WHERE Status = 'rejected'
  AND UploadDate < DATE_SUB(CURDATE(), INTERVAL 6 MONTH);

-- ── VALIDATION QUERIES ────────────────────────────────────────

-- 1. Row counts
SELECT 'Employee'      AS TableName, COUNT(*) AS RowCount FROM Employee      UNION ALL
SELECT 'Supplier',                   COUNT(*)             FROM Supplier       UNION ALL
SELECT 'Document',                   COUNT(*)             FROM Document       UNION ALL
SELECT 'ExtractedData',              COUNT(*)             FROM ExtractedData  UNION ALL
SELECT 'WorkOrder',                  COUNT(*)             FROM WorkOrder      UNION ALL
SELECT 'AuditLog',                   COUNT(*)             FROM AuditLog;

-- 2. NULL checks
SELECT COUNT(*) AS null_emp_email       FROM Employee      WHERE Email IS NULL;
SELECT COUNT(*) AS null_doc_filepath    FROM Document      WHERE FilePath IS NULL;
SELECT COUNT(*) AS null_wo_status       FROM WorkOrder     WHERE Status IS NULL;
SELECT COUNT(*) AS null_ext_confidence  FROM ExtractedData WHERE ConfidenceScore IS NULL;

-- 3. FK integrity — WorkOrder
SELECT wo.WorkOrderID
FROM WorkOrder wo
LEFT JOIN Employee e ON wo.EmployeeID = e.EmployeeID
LEFT JOIN Document d ON wo.DocumentID = d.DocumentID
LEFT JOIN Supplier s ON wo.SupplierID = s.SupplierID
WHERE e.EmployeeID IS NULL
   OR d.DocumentID IS NULL
   OR s.SupplierID IS NULL;

-- 4. FK integrity — AuditLog
SELECT al.LogID
FROM AuditLog al
LEFT JOIN Employee  e ON al.EmployeeID  = e.EmployeeID
LEFT JOIN WorkOrder w ON al.WorkOrderID = w.WorkOrderID
WHERE e.EmployeeID IS NULL OR w.WorkOrderID IS NULL;