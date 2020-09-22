from center_app import create_app, models, db, forms

app=create_app()


@app.shell_context_processor
def shell_context():
    return {
        'models':models,
        'db':db,
        'forms': forms,
    }

if __name__=="__main__":
    app.run(debug=True)

