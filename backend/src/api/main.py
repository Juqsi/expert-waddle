import base64
import binascii
import os
import uuid
import time
from io import BytesIO

from PIL import Image, UnidentifiedImageError
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse

from starlette.middleware.cors import CORSMiddleware

from plantai.plant_ai import PlantClassifier
from plantapi.plant_api import PlantGetter

from jwt import verify_jwt_sha256
import pymysql
from jwt import create_jwt_sha256

# Create image upload folder
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "classify")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load maximum image size from .env file (default: 5 MB)
MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", "5242880"))

# Load Host domain
HOST = os.getenv("HOST", "")
MIN_ACC = float(os.getenv("MIN_ACC", "40"))
app = FastAPI()

origins = [
    "https://localhost",
    "http://localhost",
    HOST
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = PlantClassifier()
getter = PlantGetter()

def notify_admin(message: str):
    print(f"[ADMIN NOTIFICATION]: {message}")

def get_db_connection(retries=3, delay=5):
    DB_HOST     = os.getenv("DATABASE_HOST", "localhost")
    DB_USER     = os.getenv("DATABASE_USER", "root")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DB_NAME     = os.getenv("DATABASE_NAME", "ctf")

    for attempt in range(1, retries + 1):
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                autocommit=True,
                cursorclass=pymysql.cursors.Cursor
            )
            print(f"[INFO] Datenbankverbindung erfolgreich (Versuch {attempt}/{retries})")
            return conn

        except pymysql.OperationalError as e:
            print(f"[ERROR] Verbindung fehlgeschlagen (Versuch {attempt}/{retries}): {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                notify_admin(f"Datenbankverbindung nach {retries} Versuchen fehlgeschlagen: {e}")
                raise

db_conn = get_db_connection()


def decode_and_save_image(image_base64: str) -> str:
    """
    Decodes a Base64-encoded image and saves it as a JPG file in the upload folder.

    Args:
        image_base64 (str): The Base64-encoded image string (can include data URL prefix).

    Returns:
        str: The absolute file path of the saved JPG image.

    Raises:
        HTTPException (413): If the image size exceeds the configured limit.
        HTTPException (400): If the Base64 format is invalid or the image format is unsupported.
        HTTPException (500): If an unknown error occurs during processing.
    """
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]

    if len(image_base64) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=413, detail="The image exceeds the maximum file size of 5 MB."
        )

    try:
        image_data = base64.b64decode(image_base64)

    except binascii.Error:
        raise HTTPException(status_code=400, detail="Invalid Base64 format.")

    try:
        image = Image.open(BytesIO(image_data))
        unique_filename = f"{uuid.uuid4().hex}.jpg"
        save_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        image.convert("RGB").save(save_path, "JPEG")

        return save_path

    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="The image format is not supported.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown error: {str(e)}")


def run_plant_classifier(image_path: str) -> list:
    """
    Executes the plant classifier model using the provided image path.

    Args:
        image_path (str): The absolute path to the saved image file.

    Returns:
        list: A list of predicted plant classifications, each containing plant details and probabilities.

    Raises:
        HTTPException (500): If an error occurs during model prediction.
    """
    try:
        predictions = classifier.predict_from_image_path(image_path, num_of_results=5)

        return predictions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in AI script: {e}")


def run_plant_getter(plant_names: list) -> list:
    """
    Fetches detailed plant information for the given list of plant names.

    Args:
        plant_names (list): A list of plant names obtained from the classifier.

    Returns:
        list: A list containing detailed plant information, including Wikipedia links.

    Raises:
        HTTPException (500): If an error occurs while fetching the plant data.
    """
    try:
        return getter.get_plant_list_data(plant_names)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plant data: {e}")


@app.post("/uploads")
async def classify_plant(image_data: dict):
    """
    Endpoint for classifying multiple Base64-encoded images of plants.

    Args:
        image_data (dict): JSON data containing a list of Base64-encoded image strings.

    Returns:
        dict: A dictionary containing results for each processed image, including recognized plant names,
              additional data, and probabilities.

    Raises:
        HTTPException (400): If the 'images' field is missing in the request.
        HTTPException (500): For unexpected errors in processing or classification.

    Example request:

    .. code-block:: json

        {
            "images": [
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD/2wBDAP8A/wD/...",
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD/2wBDAP8A/wD/..."
            ]
        }

    Example response:

    .. code-block:: json

        {
            "results": [
                {
                    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD/2wBDAP8A/wD/...",
                    "recognitions": [
                        {
                            "name": "Rosa indica",
                            "plant": { ... },
                            "wikipedia": "https://en.wikipedia.org/wiki/Rosa_indica",
                            "probability": 0.98
                        },
                        {
                            "name": "Rosa rugosa",
                            "plant": { ... },
                            "wikipedia": "https://en.wikipedia.org/wiki/Rosa_rugosa",
                            "probability": 0.85
                        }
                    ]
                }
            ]
        }
    """
    if "images" not in image_data:
        raise HTTPException(status_code=400, detail="Missing image data.")

    results = []
    for image_base64 in image_data["images"]:
        image_path = decode_and_save_image(image_base64)

        try:
            predictions = run_plant_classifier(image_path)
            predictions = [prediction for prediction in predictions if prediction["probability"] >= MIN_ACC]
            plant_names = [prediction["plant_name"] for prediction in predictions]
            plant_info = run_plant_getter(plant_names)

            image_results = {
                "image": image_base64,
                "recognitions": []
            }

            for i, prediction in enumerate(predictions):
                plant_name = prediction["plant_name"]
                plant_data = plant_info[i] if i < len(plant_info) else None

                recognition = {
                    "name": plant_name,
                    "plant": plant_data["plant"] if plant_data else None,
                    "wikipedia": plant_data["wikipedia"] if plant_data else None,
                    "probability": prediction["probability"]
                }
                image_results["recognitions"].append(recognition)

            results.append(image_results)

        finally:
            if os.path.exists(image_path):
                os.remove(image_path)

    return {"results": results}


@app.post("/search")
async def search_plant(plant_data: dict):
    """
    Endpoint for searching plants by their names and retrieving additional data.

    Args:
        plant_data (dict): A dictionary containing the plant name(s) under the "name" key.
            The "name" key can contain a single plant name (string) or a list of plant names.

    Returns:
        dict: A dictionary containing the results of the search with additional plant information.
            The results include the plant name, its associated data, and a link to the Wikipedia page.

    Raises:
        HTTPException (400): If the 'name' field is missing in the request or if it's an invalid input.

    Example request:

    .. code-block:: json

        {
            "name": "Rosa indica"
        }

    Example response:

    .. code-block:: json

        {
            "results": [
                {
                    "name": "Rosa indica",
                    "plant": { ... },
                    "wikipedia": "https://en.wikipedia.org/wiki/Rosa_indica"
                }
            ]
        }
    """
    if "name" not in plant_data:
        raise HTTPException(status_code=400, detail="Missing plant name.")

    plant_names = plant_data["name"] if isinstance(plant_data["name"], list) else [plant_data["name"]]
    results = run_plant_getter(plant_names)

    return {"results": results}

@app.get("/backups/backup.zip")
async def download_backup(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    scheme, sep, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not sep or not token:
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    payload = verify_jwt_sha256(token)

    if not payload.get("admin", False):
        raise HTTPException(status_code=401, detail="You have to be an Admin")

    backup_path = os.path.join(os.getcwd(), "backup.zip")
    if not os.path.exists(backup_path):
        raise HTTPException(status_code=404, detail="Backup not found")

    return FileResponse(
        path=backup_path,
        filename="backup.zip",
        media_type="application/zip"
    )
@app.post("/login")
async def login(credentials: dict):
    """
    UNSAFE login endpoint: erlaubt SQL-Injection, um das Passwort zu umgehen.
    Erwartet JSON { "username": "...", "password": "..." }
    Gibt zurück: { "admin": "true"|"false", "token": "<jwt>" }
    """
    input_user = credentials.get("username", "")
    input_pass = credentials.get("password", "")

    # VULNERABLE: direkte String-Konkatenation
    sql = (
        f"SELECT username, admin "
        f"FROM user "
        f"WHERE username = '{input_user}' AND password = '{input_pass}'"
    )
    try:
        with db_conn.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    if row is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db_username, is_admin_flag = row

    payload = {
        "username": db_username,
        "admin": bool(is_admin_flag)
    }
    token = create_jwt_sha256(payload)

    return {
        "admin": bool(is_admin_flag),
        "token": token
    }



@app.get("/")
async def hello_world():
    """
    A simple endpoint to verify that the API is online.

    Returns:
        dict: A greeting message confirming the API is active.
    """
    return {"message": "Hello World 🌍"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
