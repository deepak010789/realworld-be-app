# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from conduit.app import create_app
from conduit.settings import DevConfig, ProdConfig
from elasticapm.contrib.flask import ElasticAPM

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'FlaskApp',
    'SERVER_URL': 'http://10.1.1.180:8200'
}

apm = ElasticAPM(app)
