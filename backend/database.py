from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Base, Product, Customer, Sale
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:LLThvcCgealCeWrcvjVZEtTyoDjAFKrG@shinkansen.proxy.rlwy.net:50765/railway")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=True  # Enable SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
def create_tables():
    try:
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

# Sample data generation
def generate_sample_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Product).count() > 0:
            print("Sample data already exists")
            return

        print("Generating sample data...")
        # Create sample products
        products = [
            Product(name="Laptop", category="Electronics", price=999.99),
            Product(name="Smartphone", category="Electronics", price=699.99),
            Product(name="Headphones", category="Electronics", price=199.99),
            Product(name="Desk Chair", category="Furniture", price=249.99),
            Product(name="Coffee Maker", category="Appliances", price=89.99)
        ]
        db.add_all(products)
        db.commit()

        # Create sample customers
        customers = [
            Customer(name="John Doe", email="john@example.com", location="New York"),
            Customer(name="Jane Smith", email="jane@example.com", location="Los Angeles"),
            Customer(name="Bob Johnson", email="bob@example.com", location="Chicago"),
            Customer(name="Alice Brown", email="alice@example.com", location="Miami"),
            Customer(name="Charlie Wilson", email="charlie@example.com", location="Seattle")
        ]
        db.add_all(customers)
        db.commit()

        # Create sample sales
        sales = []
        for _ in range(50):  # Generate 50 random sales
            product = random.choice(products)
            customer = random.choice(customers)
            quantity = random.randint(1, 5)
            sale_date = datetime.now() - timedelta(days=random.randint(0, 90))
            
            sale = Sale(
                product_id=product.id,
                customer_id=customer.id,
                quantity=quantity,
                total_amount=product.price * quantity,
                sale_date=sale_date
            )
            sales.append(sale)
        
        db.add_all(sales)
        db.commit()
        print("Sample data generated successfully")
        
    except Exception as e:
        print(f"Error generating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 