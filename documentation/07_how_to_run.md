# How to Run the Project from Scratch

This document describes the steps required to implement the Data Management System from scratch, including database creation, data loading, and execution of data use queries.

The instructions assume the use of a MySQL or MariaDB environment with support for `LOAD DATA LOCAL INFILE`.

---

## Prerequisites

- MySQL or MariaDB installed  
- Access to a SQL client such as MySQL CLI, DBeaver, or MySQL Workbench  
- Project directory available locally, preserving the original folder structure  
- Permission to use `LOCAL INFILE` enabled in the database client  

---

## Step 1 – Create the database schema

Execute the SQL script responsible for creating the database and all relational tables.

```sql
SOURCE sql_scripts/create_tables.sql;
```
This step creates the database if it does not exist, defines all tables, and enforces primary keys, foreign keys, and referential integrity constraints.

---

## Step 2 – Load all data into the database

After the schema is created, load all original and processed data into the database.

```sql
SOURCE sql_scripts/load_data.sql;
```
This step imports structural data, climate observations, vegetation indices, and irrigation records, and performs basic validation checks using record counts.

---

## Step 3 – Run data exploration queries

Execute the SQL script containing the data use and analysis queries.

```sql
SOURCE data_use_scripts/data_use.sql;
```
This step retrieves and aggregates data across multiple tables to support exploratory analysis of vegetation, climate, and irrigation data.

---

## Expected outcome

After executing the steps above, all tables should be created and populated, data use queries should return non empty result sets, and no referential integrity errors should occur.

---

## Notes

- File paths in `LOAD DATA LOCAL INFILE` statements may need adjustment depending on the operating system  
- Scripts must be executed in the order presented above  
- The system is intended for analytical and educational purposes  



