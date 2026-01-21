import sys
import importlib

def check_library(lib_name, import_name=None):
    if import_name is None:
        import_name = lib_name
    try:
        importlib.import_module(import_name)
        print(f"✅ {lib_name} installed successfully")
        return True
    except ImportError:
        print(f"❌ {lib_name} not found")
        return False

def verify_setup():
    print("🔍 Verifying Installation...\n")
    
    libraries = [
        ('PyTorch', 'torch'),
        ('Transformers', 'transformers'),
        ('Sentence Transformers', 'sentence_transformers'),
        ('spaCy', 'spacy'),
        ('Streamlit', 'streamlit'),
        ('Pandas', 'pandas'),
        ('NumPy', 'numpy'),
        ('Scikit-learn', 'sklearn'),
        ('PyMySQL', 'pymysql'),
        ('PDFPlumber', 'pdfplumber'),
        ('Plotly', 'plotly'),
        ('NLTK', 'nltk'),
    ]
    
    results = []
    for lib_name, import_name in libraries:
        results.append(check_library(lib_name, import_name))
    
    print(f"\n📊 Result: {sum(results)}/{len(results)} libraries installed")
    
    if all(results):
        print("\n🎉 All dependencies installed successfully!")
        print("\n📝 Next Steps:")
        print("1. Setup MySQL database (run the SQL schema)")
        print("2. Update config.py with your database credentials")
        print("3. Start collecting resume data for training")
    else:
        print("\n⚠️  Some dependencies are missing. Run: pip install -r requirements.txt")

if __name__ == "__main__":
    verify_setup()