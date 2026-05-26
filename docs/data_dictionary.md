# Data Dictionary - Project 4 Europe Retail Data Platform

## 1. products.csv

| Column Name | Data Type | Description |
|---|---|---|
| ProductID | String | Unique product/SKU identifier |
| SKU | String | Stock keeping unit code |
| ProductName | String | Product description |
| Category | String | Product category such as Jerseys, Caps, Hoodies, Footwear |
| SubCategory | String | More detailed product grouping |
| Brand | String | Product brand |
| SupplierID | String | Supplier linked to the product |
| UnitCost | Decimal | Cost price of the product |
| RetailPrice | Decimal | Selling price of the product |
| Currency | String | Currency code, mainly EUR |
| IsActive | Boolean | Product active/inactive flag |

## 2. stores.csv

| Column Name | Data Type | Description |
|---|---|---|
| StoreID | String | Unique store identifier |
| StoreName | String | Store name |
| StoreType | String | Physical Store, Online Store, or Warehouse |
| Country | String | Store country |
| City | String | Store city |
| Region | String | Business region |
| OpenDate | Date | Store opening date |
| IsActive | Boolean | Store active/inactive flag |

## 3. suppliers.csv

| Column Name | Data Type | Description |
|---|---|---|
| SupplierID | String | Unique supplier identifier |
| SupplierName | String | Supplier company name |
| Country | String | Supplier country |
| LeadTimeDays | Integer | Average supplier lead time in days |
| ReliabilityScore | Decimal | Supplier reliability score from 0 to 100 |
| IsActive | Boolean | Supplier active/inactive flag |

## 4. calendar.csv

| Column Name | Data Type | Description |
|---|---|---|
| DateKey | Integer | Date key in YYYYMMDD format |
| CalendarDate | Date | Calendar date |
| Year | Integer | Year |
| Quarter | Integer | Quarter number |
| Month | Integer | Month number |
| MonthName | String | Month name |
| WeekOfYear | Integer | Week number |
| DayName | String | Day name |
| IsWeekend | Boolean | Weekend flag |

## 5. sales_transactions.csv

| Column Name | Data Type | Description |
|---|---|---|
| TransactionID | String | Unique sales transaction ID |
| TransactionDate | DateTime | Sales transaction timestamp |
| StoreID | String | Store where the sale happened |
| ProductID | String | Product sold |
| Quantity | Integer | Quantity sold |
| UnitPrice | Decimal | Selling price per unit |
| DiscountAmount | Decimal | Discount amount applied |
| GrossSales | Decimal | Quantity multiplied by unit price |
| NetSales | Decimal | Gross sales minus discount |
| PaymentMethod | String | Cash, Card, Online, Wallet |
| SalesChannel | String | Store or Online |

## 6. inventory_snapshot.csv

| Column Name | Data Type | Description |
|---|---|---|
| SnapshotDate | Date | Inventory snapshot date |
| StoreID | String | Store or warehouse ID |
| ProductID | String | Product ID |
| StockOnHand | Integer | Current available stock |
| ReservedQty | Integer | Reserved stock quantity |
| AvailableQty | Integer | Available stock after reservation |
| ReorderPoint | Integer | Minimum stock level |
| SafetyStock | Integer | Buffer stock level |

## 7. purchase_orders.csv

| Column Name | Data Type | Description |
|---|---|---|
| POID | String | Purchase order ID |
| SupplierID | String | Supplier ID |
| ProductID | String | Product ID |
| WarehouseID | String | Receiving warehouse |
| OrderDate | Date | Purchase order creation date |
| ExpectedDeliveryDate | Date | Expected delivery date |
| ActualDeliveryDate | Date | Actual received date |
| OrderedQty | Integer | Ordered quantity |
| ReceivedQty | Integer | Received quantity |
| POStatus | String | Open, Partially Received, Closed, Delayed |

## 8. stock_transfers.csv

| Column Name | Data Type | Description |
|---|---|---|
| TransferID | String | Unique transfer ID |
| ProductID | String | Product transferred |
| FromLocationID | String | Source store or warehouse |
| ToLocationID | String | Destination store |
| TransferDate | Date | Transfer creation date |
| ExpectedArrivalDate | Date | Expected arrival date |
| ActualArrivalDate | Date | Actual received date |
| TransferQty | Integer | Quantity transferred |
| ReceivedQty | Integer | Quantity received |
| TransferStatus | String | Created, In Transit, Received, Delayed, Cancelled |

## 9. returns.csv

| Column Name | Data Type | Description |
|---|---|---|
| ReturnID | String | Unique return ID |
| TransactionID | String | Original sales transaction ID |
| ReturnDate | Date | Date of return |
| StoreID | String | Store or online channel where return was processed |
| ProductID | String | Returned product |
| ReturnQty | Integer | Returned quantity |
| ReturnReason | String | Reason for return |
| RefundAmount | Decimal | Refund value |

## 10. online_orders.json

| Field Name | Data Type | Description |
|---|---|---|
| order_id | String | Online order ID |
| order_date | DateTime | Online order timestamp |
| customer.customer_id | String | Customer ID |
| customer.customer_name | String | Customer name |
| customer.country | String | Customer country |
| payment.payment_method | String | Payment method |
| payment.payment_status | String | Payment status |
| shipping.address.city | String | Shipping city |
| shipping.address.country | String | Shipping country |
| items | Array | List of ordered items |
| items.product_id | String | Product ID inside order item |
| items.quantity | Integer | Ordered item quantity |
| items.unit_price | Decimal | Item unit price |
| discounts | Array | Discount details |
| delivery_events | Array | Delivery tracking events |

## Source File Profiling Summary

The generated Project 4 source files were profiled before Azure upload.

| File Name | Record Count | Notes |
|---|---:|---|
| products.csv | 101 | Includes 100 valid product records and 1 intentional bad record |
| stores.csv | 12 | Includes 10 physical stores, 1 online store, and 1 warehouse |
| suppliers.csv | 8 | Includes 8 active suppliers |
| calendar.csv | 25 | Covers the date range from 2026-05-01 to 2026-05-25 |
| sales_transactions.csv | 1202 | Includes 1200 valid sales records, 1 bad record, and 1 duplicate |
| inventory_snapshot.csv | 1201 | Includes inventory for 12 locations and 100 products, plus 1 bad record |
| purchase_orders.csv | 301 | Includes 300 purchase orders and 1 bad record |
| stock_transfers.csv | 401 | Includes 400 stock transfers and 1 bad record |
| returns.csv | 251 | Includes 250 return records and 1 bad record |
| online_orders.json | 301 | Includes 300 online orders and 1 bad nested JSON record |

## Intentional Data Quality Issues

The source files include controlled bad records for data engineering validation practice.

Examples of intentional issues:

- Missing ProductID
- Invalid SupplierID
- Negative UnitCost
- Wrong Currency
- Future TransactionDate
- Invalid StoreID
- Invalid ProductID
- Negative Quantity
- Duplicate TransactionID
- Negative ReservedQty
- Invalid PO dates
- ReceivedQty greater than OrderedQty
- Invalid TransferStatus
- FromLocationID same as ToLocationID
- Missing online order ID
- Invalid payment status
- Empty online order items array

These issues will be handled during Silver layer validation and rejected-zone processing.