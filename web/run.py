from app import create_app

if __name__ == "__main__":
    app = create_app()
    print("=" * 50)
    print("🚀 Flask application starting...")
    print("📍 URL: http://localhost:8000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=8000, debug=True)
