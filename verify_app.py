from app import create_app

app = create_app()
print('APP_IMPORT_OK')
print('ROUTES:', sorted(str(rule) for rule in app.url_map.iter_rules())[:10])
