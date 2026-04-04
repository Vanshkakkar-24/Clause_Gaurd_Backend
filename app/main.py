import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.file_parser import extract_text
from app.clause_splitter import split_into_clauses
from app.n8n_client import send_to_n8n
from app.schemas import ContractAnalysisResponse
from app.n8n_client import send_comparison_to_n8n
from app.schemas import ContractComparisonResponse
from app.n8n_client import generate_negotiation_email
from app.schemas import NegotiationEmail

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="AI Contract IQ API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "API working"}


@app.post("/analyze/text", response_model=ContractAnalysisResponse)
def analyze_contract_text(contract_text: str):

    clauses = split_into_clauses(contract_text)

    n8n_response = send_to_n8n(contract_text)

    return {
        **n8n_response,
        "clauses": clauses
    }


@app.post("/analyze/file", response_model=ContractAnalysisResponse)
async def analyze_contract_file(file: UploadFile = File(...)):

    extension = file.filename.split(".")[-1]

    if extension not in ["pdf", "docx", "txt"]:
        raise HTTPException(
            status_code=400,
            detail="Only pdf, docx, txt allowed"
        )

    file_id = str(uuid.uuid4())

    file_path = f"{UPLOAD_DIR}/{file_id}.{extension}"

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    text = extract_text(file_path)

    clauses = split_into_clauses(text)

    n8n_response = send_to_n8n(text)

    return {
        **n8n_response,
        "clauses": clauses
    }


@app.post("/compare/files",
response_model=ContractComparisonResponse)

async def compare_contract_files(

 file1: UploadFile = File(...),
 file2: UploadFile = File(...)
):


    ext1 = file1.filename.split(".")[-1]
    ext2 = file2.filename.split(".")[-1]

    allowed = ["pdf","docx","txt"]

    if ext1 not in allowed or ext2 not in allowed:

        raise HTTPException(
            status_code=400,
            detail="Only pdf, docx, txt supported"
        )


    id1 = str(uuid.uuid4())
    id2 = str(uuid.uuid4())

    path1 = f"{UPLOAD_DIR}/{id1}.{ext1}"
    path2 = f"{UPLOAD_DIR}/{id2}.{ext2}"


    with open(path1,"wb") as f:
        f.write(await file1.read())

    with open(path2,"wb") as f:
        f.write(await file2.read())


    text1 = extract_text(path1)
    text2 = extract_text(path2)


    result = send_comparison_to_n8n(text1, text2)


    return result


@app.post(
"/generate-email",

response_model = NegotiationEmail
)

def generate_email_endpoint(
 party_1: str,
 party_2: str,
 risky_clauses: list,
 key_concerns: list,
 improvement_recommendations: list
):


    email = generate_negotiation_email(

        party_1 = party_1,

        party_2 = party_2,

        risky_clauses = risky_clauses,

        key_concerns = key_concerns,

        improvement_recommendations = improvement_recommendations
    )

    return email