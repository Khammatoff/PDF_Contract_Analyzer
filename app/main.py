import os
import shutil
import json
from fastapi import FastAPI, UploadFile, File, Depends, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Contract
from .pdf_utils import extract_text
from .openai_client import analyze_contract

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def filter_conditions(conditions: dict, max_items: int = 5) -> dict:
    filtered = {}
    count = 0
    for k, v in conditions.items():
        if v and isinstance(v, str) and len(v.strip()) > 0:
            filtered[k] = v
            count += 1
        if count >= max_items:
            break
    return filtered


@app.get("/", response_class=HTMLResponse)
async def read_upload(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith('.pdf'):
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": "Неверный формат файла. Поддерживается только PDF."},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text(file_path)
    if len(text) > 12000:
        text = text[:12000]

    try:
        result = analyze_contract(text)
    except ValueError as e:
        return templates.TemplateResponse(
            "raw.html", {"request": request, "raw_content": str(e)},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    filtered_conditions = filter_conditions(result.get("условия", {}), max_items=5)

    contract = Contract(
        filename=file.filename,
        file_path=file_path,
        subject=result.get("предмет", ""),
        conditions=result.get("условия", {}),
        parties=result.get("стороны", [])
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)

    setattr(contract, 'conditions_dict', filtered_conditions)
    return templates.TemplateResponse("result.html", {"request": request, "contract": contract})


@app.get("/contracts", response_class=HTMLResponse)
async def list_contracts(request: Request, db: Session = Depends(get_db)):
    contracts = db.query(Contract).all()
    return templates.TemplateResponse("contracts.html", {"request": request, "contracts": contracts})


@app.get("/contracts/{contract_id}", response_class=HTMLResponse)
async def view_contract(contract_id: int, request: Request, db: Session = Depends(get_db)):
    contract = db.get(Contract, contract_id)
    if not contract:
        return templates.TemplateResponse(
            "error.html", {"request": request, "message": "Договор не найден."},
            status_code=status.HTTP_404_NOT_FOUND
        )
    conditions = contract.conditions
    if not isinstance(conditions, dict):
        try:
            conditions = json.loads(conditions)
        except Exception:
            conditions = {}
    setattr(contract, 'conditions_dict', conditions)
    return templates.TemplateResponse("result.html", {"request": request, "contract": contract})


@app.post("/contracts/{contract_id}/delete")
async def delete_contract_form(contract_id: int, db: Session = Depends(get_db)):
    contract = db.get(Contract, contract_id)
    if contract:
        if os.path.exists(contract.file_path):
            os.remove(contract.file_path)
        db.delete(contract)
        db.commit()
    return RedirectResponse(url="/contracts", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/contracts/{contract_id}/download")
async def download_contract(contract_id: int, request: Request, db: Session = Depends(get_db)):
    contract = db.get(Contract, contract_id)
    if not contract:
        return templates.TemplateResponse(
            "error.html", {"request": request, "message": "Договор не найден."},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return FileResponse(path=contract.file_path, filename=contract.filename)
