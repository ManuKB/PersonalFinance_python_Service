class Config:
    # Sqllite3 db connection url
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # API Configs
    API_PATH = '/api/'
    API_VERSION = 'v1'
    BASE_URL = 'http://127.0.0.1:5000'

    # User API endpoint
    SIGN_IN = API_PATH+API_VERSION+'/sign_in'
    SIGN_UP = API_PATH+API_VERSION+'/sign_up'
    USER_PROFILE = API_PATH+API_VERSION+'/profile/<string:appname>'
    UPDATE_PROFILE = API_PATH+API_VERSION+'/update_profile/<string:appname>'
    CHANGE_PASSWORD = API_PATH+API_VERSION+'/change_password/<string:appname>'
    DELETE_ACCOUNT = API_PATH+API_VERSION+'/delete_account/<string:appname>'

    # Assets API endpoint
    FETCH_ASSETS = API_PATH+API_VERSION+'/fetch_assets/<string:appname>'
    ADD_ASSET = API_PATH+API_VERSION+'/add_asset/<string:appname>'
    SEARCH_ASSET = API_PATH+API_VERSION+'/search_asset/<string:id>/<string:appname>'
    DELETE_ASSET = API_PATH+API_VERSION+'/delete_asset/<string:id>/<string:appname>'
    UPDATE_ASSET = API_PATH+API_VERSION+'/delete_asset/<string:id>/<string:appname>'

    CIPHER_KEY = 'jf6mwvqA8b24Xn-mvFBGkHdZ_R4zdo7TXi6AD543GtE='
