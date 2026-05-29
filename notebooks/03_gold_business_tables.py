# Databricks notebook source
# Project 4 - Europe Retail Data Platform
# Notebook: 03_gold_business_tables
# Purpose: Build Gold business-ready tables from Silver Delta tables

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    current_timestamp,
    sum as spark_sum,
    count,
    countDistinct,
    avg,
    round,
    when,
    datediff,
    coalesce,
    lit
)

# COMMAND ----------

# ============================================================
# 1. Database configuration
# ============================================================

catalog_name = "supplyspark"

silver_database = f"{catalog_name}.project4_silver"
gold_database = f"{catalog_name}.project4_gold"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {gold_database}")

print(f"Silver database: {silver_database}")
print(f"Gold database ready: {gold_database}")

# COMMAND ----------

# ============================================================
# 2. Source Silver tables
# ============================================================

silver_products_table = f"{silver_database}.silver_products"
silver_stores_table = f"{silver_database}.silver_stores"
silver_suppliers_table = f"{silver_database}.silver_suppliers"
silver_calendar_table = f"{silver_database}.silver_calendar"
silver_sales_table = f"{silver_database}.silver_sales_transactions"
silver_inventory_table = f"{silver_database}.silver_inventory_snapshot"
silver_purchase_orders_table = f"{silver_database}.silver_purchase_orders"
silver_stock_transfers_table = f"{silver_database}.silver_stock_transfers"
silver_returns_table = f"{silver_database}.silver_returns"
silver_online_orders_table = f"{silver_database}.silver_online_orders"
silver_online_order_items_table = f"{silver_database}.silver_online_order_items"

# COMMAND ----------

# ============================================================
# 3. Target Gold tables
# ============================================================

gold_dim_products_table = f"{gold_database}.gold_dim_products"
gold_dim_stores_table = f"{gold_database}.gold_dim_stores"
gold_dim_suppliers_table = f"{gold_database}.gold_dim_suppliers"

gold_fact_sales_table = f"{gold_database}.gold_fact_sales"
gold_store_sales_summary_table = f"{gold_database}.gold_store_sales_summary"
gold_product_performance_table = f"{gold_database}.gold_product_performance"
gold_inventory_risk_table = f"{gold_database}.gold_inventory_risk"
gold_supplier_delivery_table = f"{gold_database}.gold_supplier_delivery_performance"
gold_returns_analysis_table = f"{gold_database}.gold_returns_analysis"
gold_online_order_summary_table = f"{gold_database}.gold_online_order_summary"

# COMMAND ----------

# ============================================================
# 4. Helper write function
# ============================================================

def write_gold_table(df, table_name):
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )

    row_count = df.count()
    print(f"Written table: {table_name} | Rows: {row_count}")
    return row_count

# COMMAND ----------

# ============================================================
# 5. Load Silver tables
# ============================================================

df_products = spark.table(silver_products_table)
df_stores = spark.table(silver_stores_table)
df_suppliers = spark.table(silver_suppliers_table)
df_sales = spark.table(silver_sales_table)
df_inventory = spark.table(silver_inventory_table)
df_purchase_orders = spark.table(silver_purchase_orders_table)
df_stock_transfers = spark.table(silver_stock_transfers_table)
df_returns = spark.table(silver_returns_table)
df_online_orders = spark.table(silver_online_orders_table)
df_online_order_items = spark.table(silver_online_order_items_table)

print("All Silver tables loaded successfully.")

# COMMAND ----------

# ============================================================
# 6. Gold dimension tables
# ============================================================

gold_dim_products = (
    df_products
    .select(
        "ProductID",
        "SKU",
        "ProductName",
        "Category",
        "SubCategory",
        "Brand",
        "SupplierID",
        "UnitCost",
        "RetailPrice",
        "Currency",
        "IsActive"
    )
    .dropDuplicates(["ProductID"])
    .withColumn("gold_processed_timestamp", current_timestamp())
)

gold_dim_stores = (
    df_stores
    .select(
        "StoreID",
        "StoreName",
        "StoreType",
        "Country",
        "City",
        "Region",
        "OpenDate",
        "IsActive"
    )
    .dropDuplicates(["StoreID"])
    .withColumn("gold_processed_timestamp", current_timestamp())
)

gold_dim_suppliers = (
    df_suppliers
    .select(
        "SupplierID",
        "SupplierName",
        "Country",
        "LeadTimeDays",
        "ReliabilityScore",
        "IsActive"
    )
    .dropDuplicates(["SupplierID"])
    .withColumn("gold_processed_timestamp", current_timestamp())
)

# COMMAND ----------

# ============================================================
# 7. Gold fact sales table
# ============================================================

gold_fact_sales = (
    df_sales.alias("s")
    .join(df_products.alias("p"), col("s.ProductID") == col("p.ProductID"), "left")
    .join(df_stores.alias("st"), col("s.StoreID") == col("st.StoreID"), "left")
    .select(
        col("s.TransactionID"),
        col("s.TransactionDate"),
        col("s.StoreID"),
        col("st.StoreName"),
        col("st.Country").alias("StoreCountry"),
        col("st.Region").alias("StoreRegion"),
        col("s.ProductID"),
        col("p.SKU"),
        col("p.ProductName"),
        col("p.Category"),
        col("p.SubCategory"),
        col("p.Brand"),
        col("s.Quantity"),
        col("s.UnitPrice"),
        col("p.UnitCost"),
        col("s.GrossSales"),
        col("s.DiscountAmount"),
        col("s.NetSales"),
        (col("s.Quantity") * col("p.UnitCost")).alias("EstimatedCost"),
        (col("s.NetSales") - (col("s.Quantity") * col("p.UnitCost"))).alias("EstimatedProfit"),
        col("s.PaymentMethod"),
        col("s.SalesChannel")
    )
    .withColumn(
        "ProfitMarginPct",
        when(col("NetSales") > 0, round((col("EstimatedProfit") / col("NetSales")) * 100, 2))
        .otherwise(lit(0))
    )
    .withColumn("gold_processed_timestamp", current_timestamp())
)

# COMMAND ----------

# ============================================================
# 8. Store sales summary
# ============================================================

gold_store_sales_summary = (
    gold_fact_sales
    .groupBy(
        "StoreID",
        "StoreName",
        "StoreCountry",
        "StoreRegion"
    )
    .agg(
        countDistinct("TransactionID").alias("TotalTransactions"),
        spark_sum("Quantity").alias("TotalUnitsSold"),
        round(spark_sum("GrossSales"), 2).alias("TotalGrossSales"),
        round(spark_sum("DiscountAmount"), 2).alias("TotalDiscount"),
        round(spark_sum("NetSales"), 2).alias("TotalNetSales"),
        round(spark_sum("EstimatedCost"), 2).alias("TotalEstimatedCost"),
        round(spark_sum("EstimatedProfit"), 2).alias("TotalEstimatedProfit"),
        round(avg("ProfitMarginPct"), 2).alias("AvgProfitMarginPct")
    )
    .withColumn("gold_processed_timestamp", current_timestamp())
)

# COMMAND ----------

# ============================================================
# 9. Product performance summary
# ============================================================

gold_product_performance = (
    gold_fact_sales
    .groupBy(
        "ProductID",
        "SKU",
        "ProductName",
        "Category",
        "SubCategory",
        "Brand"
    )
    .agg(
        countDistinct("TransactionID").alias("TotalTransactions"),
        spark_sum("Quantity").alias("TotalUnitsSold"),
        round(spark_sum("NetSales"), 2).alias("TotalNetSales"),
        round(spark_sum("EstimatedProfit"), 2).alias("TotalEstimatedProfit"),
        round(avg("ProfitMarginPct"), 2).alias("AvgProfitMarginPct")
    )
    .withColumn("gold_processed_timestamp", current_timestamp())
)

# COMMAND ----------

# ============================================================
# 10. Inventory risk table
# ============================================================

gold_inventory_risk = (
    df_inventory.alias("i")
    .join(df_products.alias("p"), col("i.ProductID") == col("p.ProductID"), "left")
    .join(df_stores.alias("s"), col("i.StoreID") == col("s.StoreID"), "left")
    .select(
        col("i.SnapshotDate"),
        col("i.StoreID"),
        col("s.StoreName"),
        col("s.Country").alias("StoreCountry"),
        col("s.Region").alias("StoreRegion"),
        col("i.ProductID"),
        col("p.SKU"),
        col("p.ProductName"),
        col("p.Category"),
        col("p.Brand"),
        col("i.StockOnHand"),
        col("i.ReservedQty"),
        col("i.AvailableQty"),
        col("i.ReorderPoint"),
        col("i.SafetyStock"),
        col("i.StockStatus")
    )
    .withColumn(
        "RiskPriority",
        when(col("StockStatus") == "Stockout", "High")
        .when(col("StockStatus") == "Reorder Risk", "Medium")
        .otherwise("Low")
    )
    .withColumn("gold_processed_timestamp", current_timestamp())
)

# COMMAND ----------

# ============================================================
# 11. Supplier delivery performance
# ============================================================

gold_supplier_delivery = (
    df_purchase_orders.alias("po")
    .join(df_suppliers.alias("s"), col("po.SupplierID") == col("s.SupplierID"), "left")
    .join(df_products.alias("p"), col("po.ProductID") == col("p.ProductID"), "left")
    .select(
        col("po.POID"),
        col("po.SupplierID"),
        col("s.SupplierName"),
        col("s.Country").alias("SupplierCountry"),
        col("s.ReliabilityScore"),
        col("po.ProductID"),
        col("p.ProductName"),
        col("p.Category"),
        col("po.WarehouseID"),
        col("po.OrderDate"),
        col("po.ExpectedDeliveryDate"),
        col("po.ActualDeliveryDate"),
        col("po.OrderedQty"),
        col("po.ReceivedQty"),
        col("po.POStatus"),
        col("po.DeliveryStatus"),
        col("po.ReceiptStatus")
    )
    .withColumn(
        "DeliveryDelayDays",
        when(
            col("ActualDeliveryDate").isNotNull(),
            datediff(col("ActualDeliveryDate"), col("ExpectedDeliveryDate"))
        ).otherwise(lit(None))
    )
    .withColumn("gold_processed_timestamp", current_timestamp())
)

# COMMAND ----------

# ============================================================
# 12. Returns analysis
# ============================================================

gold_returns_analysis = (
    df_returns.alias("r")
    .join(df_products.alias("p"), col("r.ProductID") == col("p.ProductID"), "left")
    .join(df_stores.alias("s"), col("r.StoreID") == col("s.StoreID"), "left")
    .select(
        col("r.ReturnID"),
        col("r.TransactionID"),
        col("r.ReturnDate"),
        col("r.StoreID"),
        col("s.StoreName"),
        col("s.Country").alias("StoreCountry"),
        col("s.Region").alias("StoreRegion"),
        col("r.ProductID"),
        col("p.SKU"),
        col("p.ProductName"),
        col("p.Category"),
        col("p.Brand"),
        col("r.ReturnQty"),
        col("r.ReturnReason"),
        col("r.RefundAmount")
    )
    .withColumn("gold_processed_timestamp", current_timestamp())
)

# COMMAND ----------

# ============================================================
# 13. Online order summary
# ============================================================

online_items_summary = (
    df_online_order_items
    .groupBy("OrderID")
    .agg(
        spark_sum("Quantity").alias("TotalOnlineUnits"),
        round(spark_sum("LineTotal"), 2).alias("TotalItemLineAmount")
    )
)

gold_online_order_summary = (
    df_online_orders.alias("o")
    .join(online_items_summary.alias("i"), col("o.OrderID") == col("i.OrderID"), "left")
    .select(
        col("o.OrderID"),
        col("o.OrderDate"),
        col("o.CustomerID"),
        col("o.CustomerName"),
        col("o.CustomerCountry"),
        col("o.PaymentMethod"),
        col("o.PaymentStatus"),
        col("o.GrossTotal"),
        col("o.DiscountAmount"),
        col("o.NetTotal"),
        col("o.Currency"),
        col("o.ShippingMethod"),
        col("o.ShippingStatus"),
        coalesce(col("i.TotalOnlineUnits"), lit(0)).alias("TotalOnlineUnits"),
        coalesce(col("i.TotalItemLineAmount"), lit(0)).alias("TotalItemLineAmount")
    )
    .withColumn("gold_processed_timestamp", current_timestamp())
)

# COMMAND ----------

# ============================================================
# 14. Write Gold tables
# ============================================================

gold_counts = {}

gold_counts["gold_dim_products"] = write_gold_table(gold_dim_products, gold_dim_products_table)
gold_counts["gold_dim_stores"] = write_gold_table(gold_dim_stores, gold_dim_stores_table)
gold_counts["gold_dim_suppliers"] = write_gold_table(gold_dim_suppliers, gold_dim_suppliers_table)
gold_counts["gold_fact_sales"] = write_gold_table(gold_fact_sales, gold_fact_sales_table)
gold_counts["gold_store_sales_summary"] = write_gold_table(gold_store_sales_summary, gold_store_sales_summary_table)
gold_counts["gold_product_performance"] = write_gold_table(gold_product_performance, gold_product_performance_table)
gold_counts["gold_inventory_risk"] = write_gold_table(gold_inventory_risk, gold_inventory_risk_table)
gold_counts["gold_supplier_delivery_performance"] = write_gold_table(gold_supplier_delivery, gold_supplier_delivery_table)
gold_counts["gold_returns_analysis"] = write_gold_table(gold_returns_analysis, gold_returns_analysis_table)
gold_counts["gold_online_order_summary"] = write_gold_table(gold_online_order_summary, gold_online_order_summary_table)

print("All Gold tables created successfully.")

# COMMAND ----------

# ============================================================
# 15. Gold validation summary
# ============================================================

print("Gold row count validation summary:")

for table_name, count_value in gold_counts.items():
    print(f"{table_name}: {count_value}")

spark.sql(f"SHOW TABLES IN {gold_database}").show(truncate=False)

# COMMAND ----------

# ============================================================
# 16. Business validation queries
# ============================================================

print("Top store sales summary:")
spark.sql(f"""
SELECT 
    StoreName,
    StoreCountry,
    StoreRegion,
    TotalTransactions,
    TotalUnitsSold,
    TotalNetSales,
    TotalEstimatedProfit,
    AvgProfitMarginPct
FROM {gold_store_sales_summary_table}
ORDER BY TotalNetSales DESC
LIMIT 10
""").show(truncate=False)

print("Inventory risk by status:")
spark.sql(f"""
SELECT 
    StockStatus,
    RiskPriority,
    COUNT(*) AS ProductStoreCount
FROM {gold_inventory_risk_table}
GROUP BY StockStatus, RiskPriority
ORDER BY ProductStoreCount DESC
""").show(truncate=False)

print("Supplier delivery performance:")
spark.sql(f"""
SELECT 
    SupplierName,
    DeliveryStatus,
    ReceiptStatus,
    COUNT(*) AS POCount
FROM {gold_supplier_delivery_table}
GROUP BY SupplierName, DeliveryStatus, ReceiptStatus
ORDER BY POCount DESC
LIMIT 10
""").show(truncate=False)

# COMMAND ----------

print("Project 4 Gold business tables completed successfully.")