-- ============================================================
-- DSWOPS Database DDL Script
-- Project : Document Scanner & Work Order Processing System
-- Author  : Muhammad Muizz
-- Milestone: 4
-- ============================================================

CREATE DATABASE IF NOT EXISTS dswops_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dswops_db;

-- 1. Employee
CREATE TABLE Employee (
    EmployeeID   INT          NOT NULL AUTO_INCREMENT,
    Name         VARCHAR(100) NOT NULL,
    Role         VARCHAR(50)  NOT NULL,
    Email        VARCHAR(150) NOT NULL,
    CONSTRAINT pk_employee   PRIMARY KEY (EmployeeID),
    CONSTRAINT uq_emp_email  UNIQUE (Email),
    CONSTRAINT chk_emp_role  CHECK (Role IN ('Admin','Manager','Staff','Supervisor'))
);

-- 2. Supplier
CREATE TABLE Supplier (
    SupplierID   INT          NOT NULL AUTO_INCREMENT,
    Name         VARCHAR(150) NOT NULL,
    Contact      VARCHAR(20)  NOT NULL,
    Address      VARCHAR(255) NOT NULL,
    CONSTRAINT pk_supplier PRIMARY KEY (SupplierID)
);

-- 3. Document
CREATE TABLE Document (
    DocumentID   INT          NOT NULL AUTO_INCREMENT,
    FilePath     VARCHAR(500) NOT NULL,
    UploadDate   DATE         NOT NULL,
    Status       VARCHAR(20)  NOT NULL DEFAULT 'uploaded',
    DocumentType VARCHAR(50)  NOT NULL,
    EmployeeID   INT          NOT NULL,
    CONSTRAINT pk_document     PRIMARY KEY (DocumentID),
    CONSTRAINT fk_doc_employee FOREIGN KEY (EmployeeID)
        REFERENCES Employee(EmployeeID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_doc_status CHECK (Status IN
        ('uploaded','processed','verified','rejected')),
    CONSTRAINT chk_doc_type   CHECK (DocumentType IN
        ('OfficeOrder','Letter','WorkOrder','Invoice','Report'))
);
CREATE INDEX idx_doc_employee ON Document(EmployeeID);
CREATE INDEX idx_doc_status   ON Document(Status);

-- 4. ExtractedData
CREATE TABLE ExtractedData (
    ExtractID       INT          NOT NULL AUTO_INCREMENT,
    DocumentID      INT          NOT NULL,
    FieldName       VARCHAR(100) NOT NULL,
    FieldValue      TEXT         NOT NULL,
    ConfidenceScore DECIMAL(5,2) NOT NULL,
    CONSTRAINT pk_extracted    PRIMARY KEY (ExtractID),
    CONSTRAINT fk_ext_document FOREIGN KEY (DocumentID)
        REFERENCES Document(DocumentID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_confidence  CHECK (
        ConfidenceScore >= 0.00 AND ConfidenceScore <= 100.00)
);
CREATE INDEX idx_ext_document ON ExtractedData(DocumentID);

-- 5. WorkOrder
CREATE TABLE WorkOrder (
    WorkOrderID  INT          NOT NULL AUTO_INCREMENT,
    Description  TEXT         NOT NULL,
    Status       VARCHAR(20)  NOT NULL DEFAULT 'pending',
    CreatedDate  DATE         NOT NULL,
    SupplierID   INT          NOT NULL,
    EmployeeID   INT          NOT NULL,
    DocumentID   INT          NOT NULL,
    CONSTRAINT pk_workorder   PRIMARY KEY (WorkOrderID),
    CONSTRAINT fk_wo_supplier FOREIGN KEY (SupplierID)
        REFERENCES Supplier(SupplierID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_wo_employee FOREIGN KEY (EmployeeID)
        REFERENCES Employee(EmployeeID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_wo_document FOREIGN KEY (DocumentID)
        REFERENCES Document(DocumentID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_wo_status  CHECK (Status IN
        ('pending','in_progress','completed','cancelled'))
);
CREATE INDEX idx_wo_supplier ON WorkOrder(SupplierID);
CREATE INDEX idx_wo_employee ON WorkOrder(EmployeeID);
CREATE INDEX idx_wo_document ON WorkOrder(DocumentID);

-- 6. AuditLog
CREATE TABLE AuditLog (
    LogID        INT          NOT NULL AUTO_INCREMENT,
    Action       VARCHAR(100) NOT NULL,
    Timestamp    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    EmployeeID   INT          NOT NULL,
    WorkOrderID  INT          NOT NULL,
    CONSTRAINT pk_auditlog      PRIMARY KEY (LogID),
    CONSTRAINT fk_log_employee  FOREIGN KEY (EmployeeID)
        REFERENCES Employee(EmployeeID)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_log_workorder FOREIGN KEY (WorkOrderID)
        REFERENCES WorkOrder(WorkOrderID)
        ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE INDEX idx_log_employee  ON AuditLog(EmployeeID);
CREATE INDEX idx_log_workorder ON AuditLog(WorkOrderID);