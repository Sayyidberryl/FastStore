# Product & Category API Documentation

## Authentication
Semua endpoint memerlukan JWT token dalam header:
```
Authorization: Bearer <your_jwt_token>
```

## Category API

### 1. GET /api/categories
**Description:** Mendapatkan semua kategori
**Authorization:** USER/ADMIN
**Response:**
```json
{
  "success": true,
  "message": "Categories retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Electronics",
      "created_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-01T10:00:00"
    }
  ]
}
```

### 2. GET /api/categories/{id}
**Description:** Mendapatkan kategori berdasarkan ID
**Authorization:** USER/ADMIN
**Response:**
```json
{
  "success": true,
  "message": "Category retrieved successfully",
  "data": {
    "id": 1,
    "name": "Electronics",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
}
```

### 3. POST /api/categories
**Description:** Membuat kategori baru
**Authorization:** ADMIN only
**Request Body:**
```json
{
  "name": "Electronics"
}
```
**Response (201):**
```json
{
  "success": true,
  "message": "Category created successfully",
  "data": {
    "id": 1,
    "name": "Electronics",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
}
```

### 4. PUT /api/categories/{id}
**Description:** Update kategori
**Authorization:** ADMIN only
**Request Body:**
```json
{
  "name": "Updated Electronics"
}
```
**Response (200):**
```json
{
  "success": true,
  "message": "Category updated successfully",
  "data": {
    "id": 1,
    "name": "Updated Electronics",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T11:00:00"
  }
}
```

### 5. DELETE /api/categories/{id}
**Description:** Hapus kategori
**Authorization:** ADMIN only
**Response (204):** No content
**Error (400) jika masih ada produk:**
```json
{
  "success": false,
  "message": "Cannot delete category that has products"
}
```

## Product API

### 1. GET /api/products
**Description:** Mendapatkan semua produk
**Authorization:** USER/ADMIN
**Response:**
```json
{
  "success": true,
  "message": "Products retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "iPhone 15",
      "description": "Latest iPhone model",
      "price": 999.99,
      "stock": 50,
      "category_id": 1,
      "created_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-01T10:00:00"
    }
  ]
}
```

### 2. GET /api/products/{id}
**Description:** Mendapatkan produk berdasarkan ID
**Authorization:** USER/ADMIN
**Response:**
```json
{
  "success": true,
  "message": "Product retrieved successfully",
  "data": {
    "id": 1,
    "name": "iPhone 15",
    "description": "Latest iPhone model",
    "price": 999.99,
    "stock": 50,
    "category_id": 1,
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
}
```

### 3. POST /api/products
**Description:** Membuat produk baru
**Authorization:** ADMIN only
**Request Body:**
```json
{
  "name": "iPhone 15",
  "description": "Latest iPhone model",
  "price": 999.99,
  "stock": 50,
  "category_id": 1
}
```
**Response (201):**
```json
{
  "success": true,
  "message": "Product created successfully",
  "data": {
    "id": 1,
    "name": "iPhone 15",
    "description": "Latest iPhone model",
    "price": 999.99,
    "stock": 50,
    "category_id": 1,
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
}
```

### 4. PUT /api/products/{id}
**Description:** Update produk
**Authorization:** ADMIN only
**Request Body:**
```json
{
  "name": "iPhone 15 Pro",
  "price": 1199.99,
  "stock": 30
}
```
**Response (200):**
```json
{
  "success": true,
  "message": "Product updated successfully",
  "data": {
    "id": 1,
    "name": "iPhone 15 Pro",
    "description": "Latest iPhone model",
    "price": 1199.99,
    "stock": 30,
    "category_id": 1,
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T11:00:00"
  }
}
```

### 5. DELETE /api/products/{id}
**Description:** Hapus produk
**Authorization:** ADMIN only
**Response (204):** No content

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Category not found"
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "message": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "message": "Admin access required"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Product not found"
}
```

### 422 Validation Error
```json
{
  "success": false,
  "message": "Validation error",
  "errors": [
    {
      "loc": ["body", "name"],
      "msg": "ensure this value has at least 3 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

## Validation Rules

### Category
- name: required, min 1 character, max 100 characters

### Product
- name: required, min 3 characters, max 200 characters
- description: optional
- price: required, must be >= 0
- stock: required, must be >= 0
- category_id: required, must be valid category ID