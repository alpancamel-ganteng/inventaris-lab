# Access Control Security Tests

## Project
Inventaris Lab - Secure Inventory Management System

## Test Results

| No | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| 1 | Access inventory without login | HTTP 401 | HTTP 401 | PASS |
| 2 | Admin login | Login successful | Login successful | PASS |
| 3 | Admin access inventory | HTTP 200 | HTTP 200 | PASS |
| 4 | Viewer login | Login successful | Login successful | PASS |
| 5 | Viewer access inventory | HTTP 200 | HTTP 200 | PASS |
| 6 | Viewer creates inventory item | HTTP 403 | HTTP 403 | PASS |
| 7 | Staff login | Login successful | Login successful | PASS |
| 8 | Staff creates inventory item | HTTP 201 | HTTP 201 | PASS |
| 9 | Staff deletes inventory item | HTTP 403 | HTTP 403 | PASS |

## Conclusion

The access control mechanism works as expected.
Users must authenticate before accessing protected endpoints.
Each role has different permissions:
- Admin can manage inventory and users.
- Staff can view, add, and update inventory.
- Viewer can only view inventory.

Unauthorized actions are rejected by the application.
