from app import initialize_app

app = initialize_app()
if __name__=='__main__':
    # app.run(debug=True) # Do not use debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=True)