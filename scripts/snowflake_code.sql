/*
create database called Kafka_DB and SCHEMA AND TABLES 
*/
CREATE DATABASE Kafka_DB;
CREATE SCHEMA Kafka_DB.STREAMING;
CREATE TABLE Kafka_events_Silver (
event_id STRING,
customer_id STRING,
event_type STRING,
amount NUMBER(10,2),
CURRENCY STRING,
event_timestamp TIMESTAMP_NTZ,
Kafka_ingest_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
