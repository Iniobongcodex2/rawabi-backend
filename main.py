from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import datetime
import models, schemas
from database import SessionLocal, engine

# Create the tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rawabi Mobile Backend")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROOT ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Rawabi Backend API!"}


# --- AUTHENTICATION ---
@app.post("/login")
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful", "user_email": user.email, "full_name": user.full_name}


# --- DASHBOARD STATS ---
@app.get("/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_requests = db.query(models.ServiceRequest).count()
    pending_requests = db.query(models.ServiceRequest).filter(models.ServiceRequest.status == "Pending").count()
    total_documents = db.query(models.Document).count()
    expiring_documents = db.query(models.Document).filter(models.Document.status.in_(["Expiring Soon", "Expired"])).count()

    return {
        "active_services": total_requests,
        "pending_requests": pending_requests,
        "expiring_documents": expiring_documents,
        "total_documents": total_documents
    }


# --- SERVICE REQUESTS ---
@app.get("/requests", response_model=list[schemas.ServiceRequestResponse])
def get_requests(db: Session = Depends(get_db)):
    return db.query(models.ServiceRequest).order_by(models.ServiceRequest.id.desc()).all()

@app.post("/requests", response_model=schemas.ServiceRequestResponse)
def create_request(request: schemas.ServiceRequestCreate, db: Session = Depends(get_db)):
    new_request = models.ServiceRequest(
        service_name=request.service_name,
        applicant_name=request.applicant_name,
        contact_number=request.contact_number
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


# --- FAMILY & STAFF ---
@app.get("/family", response_model=list[schemas.FamilyMemberResponse])
def get_family(db: Session = Depends(get_db)):
    return db.query(models.FamilyMember).order_by(models.FamilyMember.id.desc()).all()

@app.post("/family", response_model=schemas.FamilyMemberResponse)
def create_family_member(member: schemas.FamilyMemberCreate, db: Session = Depends(get_db)):
    new_member = models.FamilyMember(
        full_name=member.full_name,
        role=member.role,
        emirates_id=member.emirates_id,
        contact_number=member.contact_number,
        has_app_access=member.has_app_access
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


# --- DOCUMENTS ---
@app.get("/documents", response_model=list[schemas.DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    return db.query(models.Document).order_by(models.Document.id.desc()).all()

@app.post("/documents", response_model=schemas.DocumentResponse)
def create_document(doc: schemas.DocumentCreate, db: Session = Depends(get_db)):
    new_doc = models.Document(
        doc_type=doc.doc_type,
        owner_name=doc.owner_name,
        expiry_date=doc.expiry_date,
        status=doc.status
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


# --- WALLET & BILLING ---
@app.get("/wallet/balance/{email}", response_model=schemas.WalletResponse)
def get_balance(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"balance": user.balance}

@app.post("/wallet/add-funds", response_model=schemas.WalletResponse)
def add_funds(request: schemas.AddFundsRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 1. Update the balance
    user.balance += request.amount
    
    # 2. Create a transaction record
    new_transaction = models.Transaction(
        user_email=request.email,
        amount=request.amount,
        transaction_type="Credit",
        description="Added funds to wallet",
        reference_id=f"TXN-{datetime.datetime.now().strftime('%Y%M%d%H%M%S')}",
        date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    
    db.add(new_transaction)
    db.commit()
    db.refresh(user)
    
    return {"balance": user.balance}

@app.get("/wallet/transactions/{email}", response_model=list[schemas.TransactionResponse])
def get_transactions(email: str, db: Session = Depends(get_db)):
    return db.query(models.Transaction).filter(models.Transaction.user_email == email).order_by(models.Transaction.id.desc()).all()