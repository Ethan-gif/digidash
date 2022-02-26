from digi import create_app, db

if __name__ == "__main__":
    napp = create_app()
    db.create_all(app=create_app())
    napp.run(debug=False, host='0.0.0.0')
