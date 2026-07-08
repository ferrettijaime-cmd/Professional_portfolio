# MongoDB Lakehouse Pipeline with Azure Data Lake & PySpark

## Project Overview

This project demonstrates the implementation of a modern **Lakehouse Architecture** using **MongoDB Atlas**, **Azure Data Lake Storage Gen2**, **PySpark**, **Parquet**, and **Delta Lake**.

The objective is to ingest semi-structured transactional data stored in MongoDB Atlas, transform it through the **Medallion Architecture (Bronze, Silver, Gold)**, and prepare high-quality analytical datasets for downstream analytics and Business Intelligence solutions.

---

## Architecture

```text
                    MongoDB Atlas
                         │
                         ▼
              Bronze Layer (JSON)
           Azure Data Lake Storage
                         │
                         ▼
          PySpark Data Processing
                         │
                         ▼
            Silver Layer (Parquet)
                         │
                         ▼
        Business Transformations
                         │
                         ▼
            Gold Layer (Delta Lake)
                         │
                         ▼
      Analytics / SQL / Power BI / ML
```

---

# Technologies

- MongoDB Atlas
- Azure Data Lake Storage Gen2
- Python
- PySpark
- Delta Lake
- Parquet
- Azure Storage SDK
- VS Code
- Jupyter Notebook

---

# Project Workflow

## 1. Data Source

The project starts with a transactional banking dataset stored in **MongoDB Atlas**.

The dataset contains semi-structured JSON documents including:

- Transaction information
- Origin account
- Destination account
- Fraud indicators

### MongoDB Collection



![MongoDB Collection](Images/mongodb.png)


---

## 2. Bronze Layer

The first stage of the Lakehouse stores the raw documents exactly as they exist inside MongoDB.

Characteristics:

- Original JSON structure
- No transformations
- Historical storage
- Raw data preservation

The extraction process is implemented using:

- PyMongo
- Azure Storage SDK

Documents are exported from MongoDB Atlas and uploaded into Azure Data Lake Storage Gen2.

---

## 3. Azure Data Lake Storage

Azure Data Lake Storage Gen2 is organized following the Medallion Architecture.

Containers created:

- bronze
- silver
- gold

### Azure Storage



![Azure Storage](Images/azure.png)


---

## 4. Silver Layer

The Bronze JSON documents are processed using **PySpark**.

Main transformations:

- Read JSON documents
- Flatten nested objects
- Rename columns
- Clean dataset
- Preserve transactional information

Example:

Before

```json
{
    "transaction": {
        "amount": 11393,
        "type": "PAYMENT"
    }
}
```

After

| transaction_amount | transaction_type |
|-------------------:|-----------------|
| 11393 | PAYMENT |

The cleaned dataset is stored in **Parquet** format.

Advantages:

- Columnar storage
- Compression
- Fast analytical queries
- Optimized Spark performance

---

## 5. Gold Layer

The Silver dataset is transformed into analytical tables using **Delta Lake**.

The first analytical table created is:

- Fact_Transactions

Unlike Parquet, Delta Lake stores:

- Parquet files
- Transaction log (_delta_log)

Benefits:

- ACID transactions
- Version control
- Time Travel
- MERGE support
- UPDATE
- DELETE
- High-performance analytics

---

## Folder Structure

```text
MongoDB_DataLake/

│
├── Bronze_to_Silver.py
├── Silver_to_Gold.py
├── Upload_Bronze.py
├── Upload_Gold.py
├── Upload_Silver.py
│
├── notebooks/
│
├── temp/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
└── credentials.env
```

---

# Lakehouse Pipeline

```text
MongoDB Atlas
      │
      ▼
Raw JSON Documents
      │
      ▼
Azure Bronze
(JSON)
      │
      ▼
PySpark
      │
      ▼
Azure Silver
(Parquet)
      │
      ▼
PySpark
      │
      ▼
Azure Gold
(Delta Lake)
```

---

# Skills Demonstrated

- MongoDB Atlas
- Azure Data Lake Storage Gen2
- Cloud Data Engineering
- PySpark
- Delta Lake
- Parquet
- Medallion Architecture
- ETL Pipeline Design
- Semi-Structured Data Processing
- Lakehouse Architecture
- Azure Storage SDK
- Python

---

# Future Improvements

- Azure Databricks
- Azure Data Factory
- Delta Live Tables
- Azure Synapse Analytics
- Microsoft Fabric
- CI/CD deployment
- Automated orchestration with Apache Airflow