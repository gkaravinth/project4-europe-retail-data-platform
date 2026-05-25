# Business Rules - Project 4 Europe Retail Data Platform

## 1. Product Rules

- ProductID is mandatory.
- SKU is mandatory and must be unique.
- SupplierID must exist in the supplier master.
- UnitCost must be greater than or equal to 0.
- RetailPrice must be greater than UnitCost.
- Currency must be EUR.
- Inactive products should not be used for new sales transactions.
- Products with missing category or brand should be flagged for review.

## 2. Store Rules

- StoreID is mandatory.
- StoreID must be unique.
- StoreType must be one of:
  - Physical Store
  - Online Store
  - Warehouse
- Store country and city are mandatory.
- Inactive stores should not receive new stock transfers or new inventory snapshots.
- Warehouse location should be used as the main replenishment source.

## 3. Supplier Rules

- SupplierID is mandatory.
- SupplierID must be unique.
- LeadTimeDays must be greater than 0.
- ReliabilityScore must be between 0 and 100.
- Inactive suppliers should not be used for new purchase orders.

## 4. Sales Transaction Rules

- TransactionID is mandatory and must be unique.
- TransactionDate cannot be in the future.
- StoreID must exist in the store master.
- ProductID must exist in the product master.
- Quantity must be greater than 0.
- UnitPrice must be greater than or equal to 0.
- DiscountAmount cannot be negative.
- DiscountAmount cannot be greater than GrossSales.
- GrossSales = Quantity * UnitPrice.
- NetSales = GrossSales - DiscountAmount.
- SalesChannel must be Store or Online.
- Duplicate transactions should be removed during Silver processing.

## 5. Inventory Rules

- SnapshotDate is mandatory.
- StoreID must exist in the store master.
- ProductID must exist in the product master.
- StockOnHand cannot be null.
- ReservedQty cannot be negative.
- AvailableQty = StockOnHand - ReservedQty.
- Negative AvailableQty should be flagged as inventory risk.
- If AvailableQty is below ReorderPoint, StockoutRiskFlag should be set to 1.
- If AvailableQty is greater than 3 times ReorderPoint, OverstockFlag should be set to 1.

## 6. Purchase Order Rules

- POID is mandatory and must be unique.
- SupplierID must exist in the supplier master.
- ProductID must exist in the product master.
- WarehouseID must be a valid warehouse location.
- OrderDate cannot be in the future.
- ExpectedDeliveryDate must be greater than or equal to OrderDate.
- ActualDeliveryDate cannot be earlier than OrderDate.
- OrderedQty must be greater than 0.
- ReceivedQty cannot be negative.
- ReceivedQty cannot be greater than OrderedQty unless approved as excess receipt.
- POStatus must be one of:
  - Open
  - Partially Received
  - Closed
  - Delayed
- If ActualDeliveryDate is greater than ExpectedDeliveryDate, PO should be flagged as delayed.

## 7. Stock Transfer Rules

- TransferID is mandatory and must be unique.
- FromLocationID and ToLocationID must exist in the store/location master.
- FromLocationID cannot be the same as ToLocationID.
- ProductID must exist in the product master.
- TransferQty must be greater than 0.
- ReceivedQty cannot be negative.
- ReceivedQty cannot be greater than TransferQty unless approved.
- ExpectedArrivalDate must be greater than or equal to TransferDate.
- ActualArrivalDate cannot be earlier than TransferDate.
- TransferStatus must be one of:
  - Created
  - In Transit
  - Received
  - Delayed
  - Cancelled
- If ActualArrivalDate is missing and ExpectedArrivalDate is older than current date, the transfer should be flagged as delayed.
- If ReceivedQty is less than TransferQty, the transfer should be flagged as short received.

## 8. Returns Rules

- ReturnID is mandatory and must be unique.
- TransactionID should match an existing sales transaction where possible.
- StoreID must exist in the store master.
- ProductID must exist in the product master.
- ReturnQty must be greater than 0.
- RefundAmount cannot be negative.
- RefundAmount cannot be greater than original NetSales for the returned item.
- ReturnReason must not be blank.
- High return-rate products should be flagged for review.

## 9. Online Order Rules

- order_id is mandatory and must be unique.
- order_date cannot be in the future.
- Customer ID should not be null.
- Each online order must contain at least one item.
- Each item must have ProductID, Quantity, and UnitPrice.
- Item quantity must be greater than 0.
- Payment status must be one of:
  - Paid
  - Pending
  - Failed
  - Refunded
- Delivery events should be flattened into a separate Silver structure.
- Cancelled or failed-payment orders should not be counted as valid sales.

## 10. Data Quality Rules

- Mandatory master files must exist before processing starts.
- Mandatory transaction files must exist before processing starts.
- Invalid records should be written to the rejected zone.
- Valid records should continue to Bronze, Silver, and Gold layers.
- All Bronze tables must include ingestion_timestamp and source_file_name.
- All Silver tables must apply correct data types and deduplication.
- All Gold tables must be business-ready and suitable for reporting.
- Pipeline should fail if mandatory source files are missing.
- Pipeline should log validation failures for investigation.

## 11. Replenishment Risk Rules

- Average daily sales should be calculated by product and store.
- DaysOfSupply = AvailableQty / AverageDailySales.
- If DaysOfSupply is below supplier lead time, replenishment risk should be flagged.
- If AvailableQty is below SafetyStock, urgent replenishment should be flagged.
- ReorderQty should be calculated based on reorder point, safety stock, and recent sales velocity.

## 12. Reporting Rules

- Sales reports should use NetSales, not GrossSales.
- Profit = NetSales - TotalCost.
- ProfitMarginPercent = Profit / NetSales.
- ReturnRate = ReturnedQty / SoldQty.
- Inventory reports should use AvailableQty for stock availability.
- Warehouse and store inventory should be reported separately.
- Online and physical store sales should be separated by SalesChannel.