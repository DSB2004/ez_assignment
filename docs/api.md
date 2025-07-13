# API Documentation

This document outlines the available API endpoints, expected request/response structures, and authentication requirements

---

## API Status Codes Reference

This section explains common HTTP status codes used across the backend.

| Status Code          | Meaning              | Description                                                                   |
| -------------------- | -------------------- | ----------------------------------------------------------------------------- |
| **200 OK**           | Success              | The request was processed successfully and a valid response is returned.      |
| **201 Created**      | Resource Created     | The request was successful and a new resource has been created.               |
| **400 Bad Request**  | Invalid Input        | The request is malformed or required fields are missing/invalid.              |
| **401 Unauthorized** | Access Token Expired | Authentication failed due to missing or expired access token.                 |
| **403 Forbidden**    | Access Denied        | The request is understood but not allowed. The user lacks proper permissions. |

### Tips

- Use `401` when the **user needs to re-authenticate**.
- Use `403` when the user is **authenticated but not allowed** to perform the action.

## Base URL

For local development: http://localhost:8000

### Authentication API

#### `POST /user/signup/`

Allow client user signup

- **Note**: For Operation user account, use [Create Operation User Script](../scripts/create_operation_user.py)
  **Request Body:**

```json
{
  "email": "janedoe123@ex.com",
  "password": "janedoe@1990",
  "client_callback_url": "http://lccalhost:3000"
}
```

**Response Body:**

```json
{
  "message": "Signup Successful!! Please verify your account",
  "role": "client",
  "email": "janedoe@ex.com",
  "url": "verification url"
}
```

#### `POST /user/login/`

Allow client and operation user login

- **Note**: Will return 403 even for correct credentials if user has not verified their email

**Request Body:**

```json
{
  "email": "janedoe@ex.com",
  "password": "hehehe",
  "client_callback_url": "http://lccalhost:3000"
}
```

**Response Body:**

```json
{
  "message": "Login successful",
  "role": "client",
  "email": "janedoe@ex.com",
  "access_token": "Bearer access token",
  "refresh_token": "Bearer refresh token"
}
```

#### `GET /user/verify/`

Allow client and operation to verify their account using verification link sent to their registered email

- **Note**: Operation user account can be verified using the [Create Operation User Script](../scripts/create_operation_user.py)

**Request Params:**

```bash
access_token: <access_token>
email: <email>
```

**Response Body:**

```json
{
  "message": "Your account has been verified",
  "role": "client",
  "email": "janedoe@ex.com",
  "access_token": "Bearer access token",
  "refresh_token": "Bearer refresh token"
}
```

#### `POST /user/forget/`

Allow client and operation to request for password change

**Request Body:**

```json
{
  "email": "janedoe@ex.com",
  "client_callback_url": "http://lccalhost:3000"
}
```

**Response Body:**

```json
{
  "message": "Password reset email has been sent to janedoe@ex.com",
  "url": "verification url"
}
```

#### `POST /user/reset/`

Allow client and operation to request for password change

**Request Params:**

```bash
access_token: <access_token>
```

**Request Body:**

```json
{
    "email":"janedoe@ex.com"
    ,"password":"hehehe"
}
```

**Response Body:**

```json
{
    "message": "Password reset"
}
```

#### `POST /user/refresh/`

Allow client and operation to request for token refresh

**Request Body:**

```json
{
  "refresh_token": "Bearer refresh token"
}
```

**Response Body:**

```json
{
  "message": "Session refreshed",
  "access_token": "Bearer access token",
  "refresh_token": "Bearer refresh token"
}
```

#### `POST /user/request-verification/`

Allow client and operation to request for new verification sessions

**Request Body:**

```json
{
  "email": "janedoe@ex.com",
  "client_callback_url": "http://lccalhost:3000"
}
```

**Response Body:**

```json
{
  "message": "Session refreshed",
  "access_token": "Bearer access token",
  "refresh_token": "Bearer refresh token"
}
```

### File Endpoint

#### `GET /files`

Allow client user to list all the available files details

**Response Body:**

```json
{
  "data": [
    {
      "id": "f22c7423-3ccd-4267-9c94-9c941ffeb5b7",
      "name": "file-sample_100kB.doc",
      "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus blandit magna vel lectus egestas, id faucibus nunc finibus. Suspendisse vel bibendum leo.",
      "extension": "doc",
      "size": "100352", # in bytes
      "uploaded_at": "2025-07-13T19:38:17.125045Z"
    }
  ]
}
```

#### `POST /files`

Allow operational user to upload new files to cloud storage

- **Note**: add content-type of request as multiple/form-data

**Request Body:**

```json
{
  "description":"sample description content",
  "file":<FILE>
}
```

**Response Body:**

```json
{
  "data": [
    {
      "id": "f22c7423-3ccd-4267-9c94-9c941ffeb5b7",
      "name": "file-sample_100kB.doc",
      "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus blandit magna vel lectus egestas, id faucibus nunc finibus. Suspendisse vel bibendum leo.",
      "extension": "doc",
      "size": "100352", # in bytes
      "uploaded_at": "2025-07-13T19:38:17.125045Z"
    }
  ]
}
```

#### `GET /files/download`

Allow client user to download files uploaded on cloud

- **Note**: This provided a signed url only accessible for 5 minutes
  **Request Query Params:**

```bash
file_id: <file_id>
```

**Response Body:**

```json
{
  "message": "Your download link will be accessible for next 5 minutes",
  "download": "https://ik.imagekit.io/vccxrahnr/file-sample_100kB_AU2J4jkMu.doc?ik-t=1752438915&ik-s=85a3d1551a9616cacad7110c32976bd8be5e5b46"
}
```
