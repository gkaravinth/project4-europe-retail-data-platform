catalog_name = "supplyspark"
bronze_database = f"{catalog_name}.project4_bronze"
silver_database = f"{catalog_name}.project4_silver"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {silver_database}")

print(f"Bronze database: {bronze_database}")
print(f"Silver database ready: {silver_database}")

from pyspark.sql.functions import (
    col,
    current_timestamp,
    trim,
    when,
    to_date,
    explode
)

# ============================================================
# 2. Source Bronze tables
# ============================================================

bronze_products_table = f"{bronze_database}.bronze_products"
bronze_stores_table = f"{bronze_database}.bronze_stores"
bronze_suppliers_table = f"{bronze_database}.bronze_suppliers"
bronze_calendar_table = f"{bronze_database}.bronze_calendar"
bronze_sales_table = f"{bronze_database}.bronze_sales_transactions"
bronze_inventory_table = f"{bronze_database}.bronze_inventory_snapshot"
bronze_purchase_orders_table = f"{bronze_database}.bronze_purchase_orders"
bronze_stock_transfers_table = f"{bronze_database}.bronze_stock_transfers"
bronze_returns_table = f"{bronze_database}.bronze_returns"
bronze_online_orders_table = f"{bronze_database}.bronze_online_orders_raw"

# ============================================================
# 3. Target Silver tables
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

# ============================================================
# 4. Helper function
# ============================================================

def write_silver_table(df, table_name):
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

# ============================================================
# 5. Products
# ============================================================

df_products = (
    spark.table(bronze_products_table)
    .select(
        col("ProductID").cast("string"),
        trim(col("SKU")).alias("SKU"),
        trim(col("ProductName")).alias("ProductName"),
        trim(col("Category")).alias("Category"),
        trim(col("SubCategory")).alias("SubCategory"),
        trim(col("Brand")).alias("Brand"),
        col("SupplierID").cast("string"),
        col("UnitCost").cast("double"),
        col("RetailPrice").cast("double"),
        trim(col("Currency")).alias("Currency"),
        col("IsActive").cast("boolean"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .dropDuplicates(["ProductID"])
    .withColumn("silver_processed_timestamp", current_timestamp())
)

# ============================================================
# 6. Stores
# ============================================================

df_stores = (
    spark.table(bronze_stores_table)
    .select(
        col("StoreID").cast("string"),
        trim(col("StoreName")).alias("StoreName"),
        trim(col("StoreType")).alias("StoreType"),
        trim(col("Country")).alias("Country"),
        trim(col("City")).alias("City"),
        trim(col("Region")).alias("Region"),
        to_date(col("OpenDate")).alias("OpenDate"),
        col("IsActive").cast("boolean"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .dropDuplicates(["StoreID"])
    .withColumn("silver_processed_timestamp", current_timestamp())
)

# ============================================================
# 7. Suppliers
# ============================================================

df_suppliers = (
    spark.table(bronze_suppliers_table)
    .select(
        col("SupplierID").cast("string"),
        trim(col("SupplierName")).alias("SupplierName"),
        trim(col("Country")).alias("Country"),
        col("LeadTimeDays").cast("int"),
        col("ReliabilityScore").cast("double"),
        col("IsActive").cast("boolean"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .dropDuplicates(["SupplierID"])
    .withColumn("silver_processed_timestamp", current_timestamp())
)

# ============================================================
# 8. Calendar
# ============================================================

df_calendar = (
    spark.table(bronze_calendar_table)
    .select(
        col("DateKey").cast("int"),
        to_date(col("CalendarDate")).alias("CalendarDate"),
        col("Year").cast("int"),
        col("Quarter").cast("int"),
        col("Month").cast("int"),
        trim(col("MonthName")).alias("MonthName"),
        col("WeekOfYear").cast("int"),
        trim(col("DayName")).alias("DayName"),
        col("IsWeekend").cast("boolean"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .dropDuplicates(["DateKey"])
    .withColumn("silver_processed_timestamp", current_timestamp())
)

# ============================================================
# 9. Sales transactions
# ============================================================

df_sales = (
    spark.table(bronze_sales_table)
    .select(
        col("TransactionID").cast("string"),
        to_date(col("TransactionDate")).alias("TransactionDate"),
        col("StoreID").cast("string"),
        col("ProductID").cast("string"),
        col("Quantity").cast("int"),
        col("UnitPrice").cast("double"),
        col("DiscountAmount").cast("double"),
        col("GrossSales").cast("double"),
        col("NetSales").cast("double"),
        trim(col("PaymentMethod")).alias("PaymentMethod"),
        trim(col("SalesChannel")).alias("SalesChannel"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .filter(col("TransactionID").isNotNull())
    .filter(col("ProductID").isNotNull())
    .filter(col("StoreID").isNotNull())
    .filter(col("Quantity") > 0)
    .filter(col("NetSales") >= 0)
    .dropDuplicates(["TransactionID"])
    .withColumn("silver_processed_timestamp", current_timestamp())
)

# ============================================================
# 10. Inventory
# ============================================================

df_inventory = (
    spark.table(bronze_inventory_table)
    .select(
        to_date(col("SnapshotDate")).alias("SnapshotDate"),
        col("StoreID").cast("string"),
        col("ProductID").cast("string"),
        col("StockOnHand").cast("int"),
        col("ReservedQty").cast("int"),
        col("AvailableQty").cast("int"),
        col("ReorderPoint").cast("int"),
        col("SafetyStock").cast("int"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .filter(col("StoreID").isNotNull())
    .filter(col("ProductID").isNotNull())
    .withColumn(
        "StockStatus",
        when(col("AvailableQty") <= 0, "Stockout")
        .when(col("AvailableQty") <= col("ReorderPoint"), "Reorder Risk")
        .otherwise("Healthy")
    )
    .withColumn("silver_processed_timestamp", current_timestamp())
)

# ============================================================
# 11. Purchase orders
# ============================================================

df_purchase_orders = (
    spark.table(bronze_purchase_orders_table)
    .select(
        col("POID").cast("string"),
        col("SupplierID").cast("string"),
        col("ProductID").cast("string"),
        col("WarehouseID").cast("string"),
        to_date(col("OrderDate")).alias("OrderDate"),
        to_date(col("ExpectedDeliveryDate")).alias("ExpectedDeliveryDate"),
        to_date(col("ActualDeliveryDate")).alias("ActualDeliveryDate"),
        col("OrderedQty").cast("int"),
        col("ReceivedQty").cast("int"),
        trim(col("POStatus")).alias("POStatus"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .filter(col("POID").isNotNull())
    .withColumn(
        "DeliveryStatus",
        when(col("ActualDeliveryDate").isNull(), "Pending")
        .when(col("ActualDeliveryDate") > col("ExpectedDeliveryDate"), "Delayed")
        .otherwise("On Time")
    )
    .withColumn(
        "ReceiptStatus",
        when(col("ReceivedQty") < col("OrderedQty"), "Short Received")
        .when(col("ReceivedQty") > col("OrderedQty"), "Over Received")
        .otherwise("Fully Received")
    )
    .withColumn("silver_processed_timestamp", current_timestamp())
)

# ============================================================
# 12. Stock transfers
# ============================================================

df_stock_transfers = (
    spark.table(bronze_stock_transfers_table)
    .select(
        col("TransferID").cast("string"),
        col("ProductID").cast("string"),
        col("FromLocationID").cast("string"),
        col("ToLocationID").cast("string"),
        to_date(col("TransferDate")).alias("TransferDate"),
        to_date(col("ExpectedArrivalDate")).alias("ExpectedArrivalDate"),
        to_date(col("ActualArrivalDate")).alias("ActualArrivalDate"),
        col("TransferQty").cast("int"),
        col("ReceivedQty").cast("int"),
        trim(col("TransferStatus")).alias("TransferStatus"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .filter(col("TransferID").isNotNull())
    .withColumn(
        "TransferDeliveryStatus",
        when(col("ActualArrivalDate").isNull(), "In Transit")
        .when(col("ActualArrivalDate") > col("ExpectedArrivalDate"), "Delayed")
        .otherwise("On Time")
    )
    .withColumn(
        "TransferReceiptStatus",
        when(col("ReceivedQty") < col("TransferQty"), "Short Received")
        .when(col("ReceivedQty") > col("TransferQty"), "Over Received")
        .otherwise("Fully Received")
    )
    .withColumn("silver_processed_timestamp", current_timestamp())
)

# ============================================================
# 13. Returns
# ============================================================

df_returns = (
    spark.table(bronze_returns_table)
    .select(
        col("ReturnID").cast("string"),
        col("TransactionID").cast("string"),
        to_date(col("ReturnDate")).alias("ReturnDate"),
        col("StoreID").cast("string"),
        col("ProductID").cast("string"),
        col("ReturnQty").cast("int"),
        trim(col("ReturnReason")).alias("ReturnReason"),
        col("RefundAmount").cast("double"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .filter(col("ReturnID").isNotNull())
    .filter(col("ReturnQty") > 0)
    .withColumn("silver_processed_timestamp", current_timestamp())
)

# ============================================================
# 14. Online orders
# ============================================================

df_online_raw = spark.table(bronze_online_orders_table)

df_online_orders = (
    df_online_raw
    .select(
        col("order_id").cast("string").alias("OrderID"),
        to_date(col("order_date")).alias("OrderDate"),
        col("customer.customer_id").cast("string").alias("CustomerID"),
        col("customer.customer_name").cast("string").alias("CustomerName"),
        col("customer.country").cast("string").alias("CustomerCountry"),
        col("payment.payment_method").cast("string").alias("PaymentMethod"),
        col("payment.payment_status").cast("string").alias("PaymentStatus"),
        col("payment.gross_total").cast("double").alias("GrossTotal"),
        col("payment.discount_amount").cast("double").alias("DiscountAmount"),
        col("payment.net_total").cast("double").alias("NetTotal"),
        col("payment.currency").cast("string").alias("Currency"),
        col("shipping.shipping_method").cast("string").alias("ShippingMethod"),
        col("shipping.shipping_status").cast("string").alias("ShippingStatus"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .filter(col("OrderID").isNotNull())
    .dropDuplicates(["OrderID"])
    .withColumn("silver_processed_timestamp", current_timestamp())
)

df_online_order_items = (
    df_online_raw
    .select(
        col("order_id").cast("string").alias("OrderID"),
        explode(col("items")).alias("item"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .select(
        col("OrderID"),
        col("item.product_id").cast("string").alias("ProductID"),
        col("item.quantity").cast("int").alias("Quantity"),
        col("item.unit_price").cast("double").alias("UnitPrice"),
        col("item.line_total").cast("double").alias("LineTotal"),
        col("ingestion_timestamp"),
        col("source_file_name")
    )
    .filter(col("OrderID").isNotNull())
    .filter(col("ProductID").isNotNull())
    .filter(col("Quantity") > 0)
    .withColumn("silver_processed_timestamp", current_timestamp())
)

# ============================================================
# 15. Write Silver Delta tables
# ============================================================

silver_counts = {}

silver_counts["silver_products"] = write_silver_table(df_products, silver_products_table)
silver_counts["silver_stores"] = write_silver_table(df_stores, silver_stores_table)
silver_counts["silver_suppliers"] = write_silver_table(df_suppliers, silver_suppliers_table)
silver_counts["silver_calendar"] = write_silver_table(df_calendar, silver_calendar_table)
silver_counts["silver_sales_transactions"] = write_silver_table(df_sales, silver_sales_table)
silver_counts["silver_inventory_snapshot"] = write_silver_table(df_inventory, silver_inventory_table)
silver_counts["silver_purchase_orders"] = write_silver_table(df_purchase_orders, silver_purchase_orders_table)
silver_counts["silver_stock_transfers"] = write_silver_table(df_stock_transfers, silver_stock_transfers_table)
silver_counts["silver_returns"] = write_silver_table(df_returns, silver_returns_table)
silver_counts["silver_online_orders"] = write_silver_table(df_online_orders, silver_online_orders_table)
silver_counts["silver_online_order_items"] = write_silver_table(df_online_order_items, silver_online_order_items_table)

print("All Silver tables created successfully.")

# ============================================================
# 16. Validation summary
# ============================================================

print("Silver row count validation summary:")

for table_name, count_value in silver_counts.items():
    print(f"{table_name}: {count_value}")

spark.sql(f"SHOW TABLES IN {silver_database}").show(truncate=False)

print("Sample inventory stock status:")
spark.sql(f"""
SELECT ProductID, StoreID, AvailableQty, ReorderPoint, StockStatus
FROM {silver_inventory_table}
LIMIT 10
""").show(truncate=False)

print("Sample purchase order delivery status:")
spark.sql(f"""
SELECT POID, ExpectedDeliveryDate, ActualDeliveryDate, DeliveryStatus, ReceiptStatus
FROM {silver_purchase_orders_table}
LIMIT 10
""").show(truncate=False)

print("Project 4 Silver cleaning completed successfully.")