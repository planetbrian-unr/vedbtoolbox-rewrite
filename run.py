# waitress usage: https://docs.pylonsproject.org/projects/waitress/en/latest/usage.html

from toolbox import create_app
#from waitress import serve

app = create_app()

if __name__ == "__main__":
    #serve(app)
    app.run()