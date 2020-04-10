from app import create_app

app=create_app()
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'],threaded=True)#开启调试模式