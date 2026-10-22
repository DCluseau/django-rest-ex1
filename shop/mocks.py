import requests

# Constante pour réutiliser l'écoscore
ECOSCORE_GRADE = 'd'

def mock_openfoodfact_success(self, method, url):
    def monkey_json():
        return {
            'products': {
                'ecoscore_grade': ECOSCORE_GRADE
            }
        }

    response = requests.Response()
    response.status_code = 200
    response.json = monkey_json
    return response