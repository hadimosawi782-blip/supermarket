# debug_server.py - در root پروژه
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

# اضافه کردن route تست مستقیم
@app.route('/test')
def test_route():
    return "✅ TEST ROUTE WORKS!"

@app.route('/ping')
def ping():
    return "PONG - Server is running"

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 DEBUG FLASK SERVER STARTING")
    print("=" * 60)
    
    # نمایش همه routeها
    print("\n📋 REGISTERED ROUTES:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule}")
    
    print("\n🔗 TEST URLS:")
    print("  http://127.0.0.1:5000/test")
    print("  http://127.0.0.1:5000/ping")
    print("  http://127.0.0.1:5000/license")
    print("  http://127.0.0.1:5000/")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)