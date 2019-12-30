from flask_restplus import Api

from endpoints import api as ns1

api = Api(
    title='Simple importing API XML/ZIP - Kintegra Desktop',
    version='0.1',
    description='API for importing xml and zip files using Kintegra Desktop',
    # All API metadatas
)

api.add_namespace(ns1, path='/v1/guia')
