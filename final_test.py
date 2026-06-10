import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🚀 FINAL TEST - Starting clean server")
print("=" * 60)

try:
    # حذف importهای قدیمی
    if 'app.routes' in sys.modules:
        del sys.modules['app.routes']
    
    from app import create_app
    app = create_app()
    
    print("\n🌐 ALL REGISTERED ROUTES:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule:30} -> {rule.endpoint}")
    
    print("\n🔗 TEST NOW:")
    print("  http://127.0.0.1:5000/")
    print("  http://127.0.0.1:5000/license")
    print("  http://127.0.0.1:5000/login")
    print("  http://127.0.0.1:5000/test")
    print("=" * 60)
    
    app.run(debug=True, port=5000, use_reloader=False)
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")