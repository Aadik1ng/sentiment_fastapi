# Content from D:\fastapi_sentiment_analysis\app\main.py
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utils import get_hashed_password, verify_password, create_access_token
from app.schemas import User, Token, SentimentAnalysisResult
from app.deps import get_current_user
from app.sentiment import process_and_generate_report 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

 # Import the function from sentiment.py
# Add CORS middleware

# Initialize FastAPI app
app = FastAPI()

# In-memory database for simplicity
fake_db = {}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this to specific origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (you can restrict this to specific methods like ["GET", "POST"])
    allow_headers=["*"],  # Allow all headers
)
# OAuth2 password bearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Sign-up endpoint
@app.post("/signup", response_model=User)
async def signup(user: User):
    if user.email in fake_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_db[user.email] = {"email": user.email, "password": get_hashed_password(user.password)}
    return user

# Login endpoint to authenticate and return a token
@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/analyze_sentiment", response_model=SentimentAnalysisResult)
async def analyze_sentiment_endpoint(
    file: UploadFile = File(...),  # To accept the file upload
    current_user: User = Depends(get_current_user)  # To authenticate the user
):
    try:
        # Process the uploaded CSV file
        contents = await file.read()

        # Call sentiment.py to process and generate the sentiment report
        report = process_and_generate_report(contents)

        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Serve static files from the "static" directory
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="D:/fastapi_sentiment_analysis/static"), name="static")
