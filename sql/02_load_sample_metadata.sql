--==================================================
-- Reusable Data Quality Framework
-- Load Sample Metadata
-- Version : v0
--==================================================

USE CATALOG dq_framework;
USE SCHEMA framework;

DELETE FROM dq_execution_master;
DELETE FROM dq_rule_master;

INSERT INTO dq_execution_master
(source_catalog,source_schema,source_table,target_catalog,target_schema,target_table,rule_set,write_mode,active,created_timestamp,updated_timestamp)
VALUES
('dq_framework','bronze','customer_master','dq_framework','silver','customer_master','CUSTOMER','OVERWRITE','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('dq_framework','bronze','employee_master','dq_framework','silver','employee_master','EMPLOYEE','OVERWRITE','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('dq_framework','bronze','sales_orders','dq_framework','silver','sales_orders','SALES','OVERWRITE','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('dq_framework','bronze','product_master','dq_framework','silver','product_master','PRODUCT','OVERWRITE','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP());

INSERT INTO dq_rule_master
(rule_set,column_name,rule_type,rule_value,severity,active,created_timestamp,updated_timestamp)
VALUES

('CUSTOMER','customer_id','NOT_NULL','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('CUSTOMER','customer_id','UNIQUE','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('CUSTOMER','customer_name','NOT_NULL','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('CUSTOMER','age','RANGE','0,120','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('CUSTOMER','email','EMAIL','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('CUSTOMER','gender','SET','M,F','WARNING','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),

('EMPLOYEE','employee_id','NOT_NULL','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('EMPLOYEE','employee_id','UNIQUE','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('EMPLOYEE','employee_name','NOT_NULL','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('EMPLOYEE','age','RANGE','18,65','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('EMPLOYEE','email','EMAIL','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('EMPLOYEE','department','NOT_NULL','','WARNING','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),

('SALES','order_id','NOT_NULL','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('SALES','order_id','UNIQUE','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('SALES','order_amount','RANGE','0,100000','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('SALES','status','SET','COMPLETED,PENDING,CANCELLED','WARNING','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),

('PRODUCT','product_id','NOT_NULL','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('PRODUCT','product_id','UNIQUE','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('PRODUCT','product_name','NOT_NULL','','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('PRODUCT','price','RANGE','0,1000000','ERROR','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP()),
('PRODUCT','category','NOT_NULL','','WARNING','Y',CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP());

SELECT * FROM dq_execution_master ORDER BY execution_id;
SELECT * FROM dq_rule_master ORDER BY rule_set,rule_id;