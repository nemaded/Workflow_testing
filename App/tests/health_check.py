
import httpx

def test_database_connection():
    try:
        with httpx.Client() as client:
            response = client.get("http://localhost:8000/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
          # Update a file or environment variable if the connection is successful
        with open("database_connected.txt", "w") as file:
            file.write("Connected to the database")

    except Exception as e:
        # Handle the exception (e.g., update a file or environment variable accordingly)
        with open("database_connected.txt", "w") as file:
            file.write("Failed to connect to the database")