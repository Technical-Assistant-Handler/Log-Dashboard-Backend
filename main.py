from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv
from authentication import append_logout_time, user_authentication
from backend import config
from update_password import update_password
from send_otp_mail import generate_otp_code, mail_design, send_email
from get_user_data import get_user_log_data, verify_tpnumber

# Load environment variables from .env file in the backend folder
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGINS", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Configure logger properly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ip_address = config.IP_ADDRESS

@app.post("/authenticate")
async def authenticate(request: Request):
    data = await request.json()
    logger.info(f"Received authentication request: {data}")
    input_tpnumber = data.get("tpnumber")
    input_password = data.get("password")

    if not input_tpnumber or not input_password:
        logger.error("Missing tpnumber or password")
        raise HTTPException(status_code=400, detail="Missing tpnumber or password")

    result = user_authentication(input_tpnumber, input_password)
    return result



@app.post("/logout")
async def logout(request: Request):
    data = await request.json()
    logger.info(f"Received logout request: {data}")
    tpnumber = data.get("tpnumber")

    if not tpnumber:
        logger.error("Missing tpnumber")
        raise HTTPException(status_code=400, detail="Missing tpnumber")

    try:
        append_logout_time(tpnumber)
        return {"message": "Logout successful"}
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
   

 
@app.get("/user_log_data")
def read_user_log_data():
    try:
        return get_user_log_data()
    except HTTPException as e:
        logger.error(f"Error handling request: {e.detail}")  # ✅ Use `logger.error`
        raise e
    except Exception as e:
        logger.error(f"Unexpected error handling request: {e}")  # ✅ Use `logger.error`
        raise HTTPException(status_code=500, detail="Internal server error")
 
@app.post("/generate_otp")
async def generate_otp(request: Request):

    data = await request.json()
    tpnumber = data.get("tpnumber")
    RECEIVER_EMAIL = f"{tpnumber}@mail.apu.edu.my"
    if not verify_tpnumber(tpnumber):
        logger.error(f"Invalid tpnumber: {tpnumber}")
        raise HTTPException(status_code=400, detail="Invalid tpnumber")
    if not tpnumber:
        logger.error("Missing tpnumber")
        raise HTTPException(status_code=400, detail="Missing tpnumber")
    
    # Here you can add logic to validate the tpnumber if needed
    verification_code = generate_otp_code()
    email_body = mail_design(verification_code)
    send_email(RECEIVER_EMAIL, "Your Verification Code", email_body)
    return {"message": "Verification code sent to your email.", "otp": str(verification_code)}
 
@app.post("/update_password")
async def update_password_endpoint(request: Request):
    data = await request.json()
    tpnumber = data.get("tpnumber")
    new_password = data.get("password")

    if not tpnumber or not new_password:
        logger.error("Missing tpnumber or password")
        raise HTTPException(status_code=400, detail="Missing tpnumber or password")

    try:
        result = update_password(tpnumber, new_password)
        return result
    except Exception as e:
        logger.error(f"Error updating password: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/")
def read_root():
    return {"message": "Welcome to backend!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ip_address, port=8000)
