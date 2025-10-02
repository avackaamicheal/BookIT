# BookIt

A production-ready REST API for a simple bookings platform called BookIt. Users can browse services, make bookings, and leave reviews. Admins manage users, services, and bookings.

## Architectural Decisions

- **Framework:** FastAPI was chosen for its high performance, asynchronous capabilities, and automatic generation of interactive API documentation (Swagger UI and ReDoc).
- **Database:** PostgreSQL is used as the database for this project. It is a powerful, open-source object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.
- **ORM:** SQLAlchemy is used as the Object-Relational Mapper (ORM). It provides a powerful and flexible way to interact with the database using Python objects, abstracting away the need to write raw SQL queries.

## How to Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add the necessary environment variables. See the Environment Variables table below for details.

3. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the application:**
   The application will be running at `https://bookit-yk47.onrender.com/docs`.

## API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

- **Swagger UI:** `https://bookit-yk47.onrender.com/docs`
- **ReDoc:** `https://bookit-yk47.onrender.com/redoc`

## Environment Variables

| Variable                  | Description                                       | Example Value                                   |
| ------------------------- | ------------------------------------------------- | ----------------------------------------------- |
| `DATABASE_URL`            | The connection string for the PostgreSQL database.  | `postgresql://book_it_3ygm_user:9EfpE8o7vT8TIjVZnU7q2AYDih32PkIz@dpg-d3f6h3vfte5s73bnl7m0-a/book_it_3ygm`  |
| `SECRET_KEY`              | The secret key for signing JWTs.                  | `kjadnvakjdsbvvadfvdfvlkfdv` |
| `ALGORITHM`               | The algorithm used for signing JWTs.              | `HS256`                                         |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | The expiration time for access tokens in minutes. | `30`                                            |

## Deployment Notes

This application is hosted on [Render](https://render.com/).

### Configuration

Render can deploy this application directly from the GitHub repository. You can configure the service using a `render.yaml` file in the root of your project, or directly in the Render dashboard.

- **Service Type:** Web Service
- **Environment:** Python
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Environment Variables

You will need to configure the environment variables listed above in the Render dashboard for your service. Render provides a managed PostgreSQL database, and you can get the `DATABASE_URL` from the database service's settings.

### Base URL

`(https://bookit-yk47.onrender.com)`).
