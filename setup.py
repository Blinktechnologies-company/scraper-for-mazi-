"""
Setup script to initialize the project
"""
import os
import subprocess
import sys

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if os.path.exists('.env'):
        print("\n✓ .env file already exists")
        return
    
    print("\n📝 Creating .env file...")
    try:
        with open('.env.example', 'r') as src:
            content = src.read()
        
        with open('.env', 'w') as dst:
            dst.write(content)
        
        print("✓ .env file created")
        print("⚠ Please edit .env file with your settings")
    except Exception as e:
        print(f"❌ Failed to create .env: {e}")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    os.makedirs('scraped_data', exist_ok=True)
    print("✓ Directories created")

def initialize_database():
    """Initialize database"""
    print("\n🗄️ Initializing database...")
    try:
        from database import init_db
        init_db()
        print("✓ Database initialized")
    except Exception as e:
        print(f"⚠ Database initialization will happen on first run: {e}")

def main():
    print("="*60)
    print("Events & Deals API - Setup")
    print("="*60)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Create directories
    create_directories()
    
    # Initialize database
    initialize_database()
    
    print("\n" + "="*60)
    print("✅ Setup complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit .env file with your settings")
    print("2. Run: python run_api.py")
    print("3. Visit: http://localhost:8000/docs")
    print("\nFor deployment:")
    print("- Quick start: See QUICKSTART.md")
    print("- Full guide: See DEPLOYMENT.md")
    print("="*60)

if __name__ == "__main__":
    main()
