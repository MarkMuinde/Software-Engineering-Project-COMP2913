from app import app
if __name__ =="__main__":
    context = ('local.crt', 'local.key')#certificate and key files
    app.run(debug=True,ssl_context=('cert.pem', 'key.pem'))