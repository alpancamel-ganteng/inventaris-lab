# Access Control Security Tests

## Project
Inventaris Lab - Secure Inventory Management System

## Access Control Matrix

| Hak Akses | Admin | Staff | Viewer |
|---|---|---|---|
| Melihat inventaris | Allow | Allow | Allow |
| Menambah inventaris | Allow | Allow | Deny |
| Mengubah inventaris | Allow | Allow | Deny |
| Menghapus inventaris | Allow | Deny | Deny |
| Mengelola pengguna | Allow | Deny | Deny |

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

## Risk Mapping

| Security Control | Risk ID |
|---|---|
| Password hashing dan autentikasi | R-01 |
| Role-Based Access Control (RBAC) | R-02 |
| Session cookie security | R-03 |
| Database dan backup permissions | R-04 |
| Container hardening | R-05 |
| SQL injection prevention | R-06 |
| Rate limiting | R-07 |
| Secret key protection | R-08 |