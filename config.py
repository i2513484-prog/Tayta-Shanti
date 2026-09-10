class Config:

    SECRET_KEY = 'supersecretkey'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://taytashanti_admin:tva_#JuwCP92_gZ@mysql-taytashanti.alwaysdata.net/taytashanti_admin'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {

        "pool_pre_ping": True,

        "pool_recycle": 280,

        "pool_timeout": 20,

        "max_overflow": 15

    }

    # ===== GMAIL =====

    MAIL_SERVER = "smtp.gmail.com"

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USERNAME = "johnsuasnabar23@gmail.com"

    MAIL_PASSWORD = "nzis ufig evcr uqxc"