from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)
    applicant_name = Column(String)           
    contact_number = Column(String)           
    status = Column(String, default="Pending") 


class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    role = Column(String)                     
    emirates_id = Column(String)
    contact_number = Column(String)
    has_app_access = Column(Boolean, default=False) 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    balance = Column(Float, default=0.0) # <-- ADDED WALLET BALANCE


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_type = Column(String, index=True)    
    owner_name = Column(String)              
    expiry_date = Column(String)             
    status = Column(String, default="Valid") 


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    amount = Column(Float)
    transaction_type = Column(String) # "Credit" (add funds) or "Debit" (pay)
    description = Column(String)
    reference_id = Column(String)
    date = Column(String) # For simplicity, we'll store date as a string