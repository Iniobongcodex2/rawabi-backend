from pydantic import BaseModel

class ServiceRequestCreate(BaseModel):
    service_name: str
    applicant_name: str
    contact_number: str

class ServiceRequestResponse(ServiceRequestCreate):
    id: int
    status: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

class FamilyMemberCreate(BaseModel):
    full_name: str
    role: str
    emirates_id: str
    contact_number: str
    has_app_access: bool = False

class FamilyMemberResponse(FamilyMemberCreate):
    id: int

    class Config:
        from_attributes = True

class DocumentCreate(BaseModel):
    doc_type: str
    owner_name: str
    expiry_date: str
    status: str = "Valid"

class DocumentResponse(DocumentCreate):
    id: int

    class Config:
        from_attributes = True

class WalletResponse(BaseModel):
    balance: float

class AddFundsRequest(BaseModel):
    email: str
    amount: float

class TransactionResponse(BaseModel):
    id: int
    user_email: str
    amount: float
    transaction_type: str
    description: str
    reference_id: str
    date: str

    class Config:
        from_attributes = True