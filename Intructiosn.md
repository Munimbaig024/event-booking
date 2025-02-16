
## 1. Events Service (runs on `localhost:8001`)

**Endpoints**

| Method | Path                                | Description                         |
| ------ | ----------------------------------- | ----------------------------------- |
| POST   | `/events`                           | Create a new event                  |
| GET    | `/events`                           | List all events                     |
| GET    | `/events/{event_id}`                | Get one event by its ID             |
| PUT    | `/events/{event_id}`                | Update all fields of an event       |
| PUT    | `/events/{event_id}/update_tickets` | Update only the `available_tickets` |
| DELETE | `/events/{event_id}`                | Delete an event                     |

### Sample Postman Calls

**1. Create Event**

* **URL:** `http://localhost:8001/events`
* **Method:** `POST`
* **Headers:**

  ```
  Content-Type: application/json
  ```

* **Body (raw JSON):**

  ```json
  {
    "title": "Open-Air Concert",
    "description": "Live music in the park",
    "date": "2025-08-01T19:00:00Z",
    "location": "Central Park",
    "available_tickets": 500
  }
  ```

**2. List All Events**

* **URL:** `http://localhost:8001/events`
* **Method:** `GET`

**3. Get One Event**

* **URL:** `http://localhost:8001/events/67e750577966a36738122d9a`
* **Method:** `GET`

**4. Update Entire Event**

* **URL:** `http://localhost:8001/events/67e750577966a36738122d9a`
* **Method:** `PUT`
* **Headers:**

  ```
  Content-Type: application/json
  ```
* **Body:**

  ```json
  {
    "title": "Open-Air Concert (Updated)",
    "description": "Doors open at 6 PM",
    "date": "2025-08-01T18:00:00Z",
    "location": "Central Park",
    "available_tickets": 450
  }
  ```

**5. Update Tickets Only**

* **URL:** `http://localhost:8001/events/67e750577966a36738122d9a/update_tickets`
* **Method:** `PUT`
* **Headers:**

  ```
  Content-Type: application/json
  ```
* **Body:**

  ```json
  {
    "available_tickets": 300
  }
  ```

**6. Delete Event**

* **URL:** `http://localhost:8001/events/67e750577966a36738122d9a`
* **Method:** `DELETE`

---

## 2. User Service (runs on `localhost:8000`)

**Endpoints**

| Method | Path               | Description                              |
| ------ | ------------------ | ---------------------------------------- |
| POST   | `/register`        | Create a new user account                |
| POST   | `/login`           | Log in and receive a JWT token           |
| GET    | `/users`           | (Admin) List all users                   |
| GET    | `/users/{user_id}` | Get one user by their ID                 |
| GET    | `/events`          | (Protected) Fetch events via gateway     |
| POST   | `/bookings`        | (Protected) Create a booking via gateway |

### Sample Postman Calls

**1. Register**

* **URL:** `http://localhost:8000/register`
* **Method:** `POST`
* **Headers:**

  ```
  Content-Type: application/json
  ```
* **Body:**

  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securePassword123"
  }
  ```

**2. Login**

* **URL:** `http://localhost:8000/login`
* **Method:** `POST`
* **Headers:**

  ```
  Content-Type: application/json
  ```
* **Body:**

  ```json
  {
    "email": "john@example.com",
    "password": "securePassword123"
  }
  ```
* **Response example:**

  ```json
  {
    "access_token": "...JWT_TOKEN...",
    "token_type": "bearer"
  }
  ```

**3. List All Users**

* **URL:** `http://localhost:8000/users`
* **Method:** `GET`

**4. Get One User**

* **URL:** `http://localhost:8000/users/5`
* **Method:** `GET`

**5. Fetch Events (protected)**

* **URL:** `http://localhost:8000/events`
* **Method:** `GET`
* **Headers:**

  ```
  Authorization: Bearer <JWT_TOKEN>
  ```

**6. Create Booking (protected)**

* **URL:** `http://localhost:8000/bookings`
* **Method:** `POST`
* **Headers:**

  ```
  Authorization: Bearer <JWT_TOKEN>
  Content-Type: application/json
  ```
* **Body:**

  ```json
  {
    "event_id": "67e750577966a36738122d9a",
    "num_tickets": 2
  }
  ```

---

## 3. Booking Service (runs on `localhost:8002`)

**Endpoints**

| Method | Path        | Description                 |
| ------ | ----------- | --------------------------- |
| POST   | `/bookings` | Create a booking (internal) |

### Sample Postman Call

> Usually called via the gateway, but here’s the direct payload:

* **URL:** `http://localhost:8002/bookings`
* **Method:** `POST`
* **Headers:**

  ```
  Content-Type: application/json
  ```
* **Body:**

  ```json
  {
    "user_id": 5,
    "event_id": "67e750577966a36738122d9a",
    "num_tickets": 2
  }
  ```
