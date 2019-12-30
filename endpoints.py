from flask_restplus import Resource
from serializers import api, guia_parser
from guia import Guia

@api.route('/gera')
@api.response(500, 'Internal server error.')
@api.response(400, 'Bad request.')
class GeraGuia(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super(GeraGuia, self).__init__(api, args, kwargs)
        self.bus = Guia()

    @api.expect(guia_parser)
    def post(self):
        data = guia_parser.parse_args()
        return self.bus.guia(data)
