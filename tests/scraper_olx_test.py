import unittest, re, requests, dotenv
# import geoservices as ctc
import plot
from repository import getAds, toGeojson, makeFeatures
from geoservices import parseCoords, toGeocode, batchGeocodeAddress
from scraper_olx import extractAdsFromPages, getAddressAdOLX, searchOLX
from utils import normalizeCep

@unittest.skip('Teste não aplicável')        
class CepToCoordsTests(unittest.TestCase):
    
    def test_coordinates_retrieval(self):
        # self.assertEqual(ctc.getCoordsFromCep('50810000'), {'lat': '1', 'lng': '2'})
        pass
    def test_batch_geocode(self):
        # res = ctc.batchGeocode(['54330-075','54000-000','55000-000'])
        # print(res)
        pass
    
@unittest.skip('Teste não aplicável')
class PlottingTests(unittest.TestCase):
    
    def test_saving_plot(self):
        plot.plotMap()
        err_str = None
        try:
            with open('./plot.json') as fd:
                # print('plot.json found successfully')
                pass
        except Exception as e:
            print(f'Actual Exception: {e.strerror}')
            err_str = e.strerror
        self.assertEqual(err_str, None,'plot.json not found')
    
    # def test_geojson_export(self):
    #     print('\nBeginning toGeojson function test\n')
    #     ads = getAds()
    #     # print(ads['active'])
    #     geojson = toGeojson(ads)
    #     features = geojson['features']
    #     found_active = False
    #     for active_prop in [feature['properties']['active'] for feature in features]:
    #         if active_prop:
    #             print('Found active')
    #             found_active = True
    #             break
    #     self.assertTrue(found_active, 'Nenhum anúncio com status ativo verdadeiro encontrado')
    
    def test_make_geojson_features(self):
        print('\nBeginning toGeojson function test\n')
        ads = getAds()
        # print(ads['active'])
        features = makeFeatures(ads)
        found_active = False
        for active_prop in [feature['properties']['active'] for feature in features]:
            if active_prop:
                print('Found active')
                found_active = True
                break
        self.assertTrue(found_active, 'Nenhum anúncio com status ativo verdadeiro encontrado')

class OlxScraperTests(unittest.TestCase):
    config = dotenv.dotenv_values('.env')
    GEOAPIFY_API_KEY = config['GEOAPIFY_API_KEY']
    
    ad_url = 'https://pe.olx.com.br/grande-recife/imoveis/casa-a-venda-na-r-sorocaba-9-cordeiro-recife-1369887103'
    text_query = 'Rua Sorocaba, Cordeiro, Recife, PE, 50721530'
    geocode_url = f'https://api.geoapify.com/v1/geocode/search?text={text_query}&format=json&apiKey={GEOAPIFY_API_KEY}'
    expected = dict(
        address = 'Rua Sorocaba, Cordeiro, Recife, PE, 50721530',
        # cep = '50721-530',
        lng = -34.9361836,
        lat = -8.0518979,
    )
    res = requests.get(geocode_url)
    res_json = res.json()
    # results = res_json['results']
    # match = results[0]
    
    def test_geocoding_request(self):
        
        status_code = self.res.status_code
        self.assertEqual(status_code, 200, f"""
            Falha na requisição.
            Status Code: {status_code}
        """)
        
        results = self.res_json['results']
        results_len = len(results)
        self.assertGreaterEqual(results_len, 1, f"""
            Nenhum resultado encontrado com o texto de busca fornecido.
            Query: "{self.text_query}"
        """)
        
        match = results[0]
        # result_type == "street" (ausente se result_type for "suburb")
        self.expected['address'] = f"""{match['street']}, {match['suburb']}, {match['district']}, {match['state_code']}, {normalizeCep(match['postcode'])}"""
        self.expected['lng'] = match['lon']
        self.expected['lat'] = match['lat']
        
        # todo - Testar se os ads com CEP incompatível com a API da Geoapify retornam o mesmo resultado
        # se a busca incluir o endereço completo
        
        address = getAddressAdOLX(self.ad_url)
        self.assertEqual(address, self.expected['address'])
        
        coords = toGeocode(address)
        self.assertEqual(coords['lat'], self.expected['lat'])
        self.assertEqual(coords['lng'], self.expected['lng'])
    
    
    def test_extract_ads_from_page_olx(self):
        params = "pe=1000&ret=1020&ret=1060&ret=1040&sd=3747&sd=3778&sd=3766&sd=3764&sd=3762"
        url = f"https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife?{params}"
        ads = extractAdsFromPages(url)
        self.assertGreaterEqual(len(ads), 1, 'No ads found from the search')
    
    def test_search_olx(self):
        ads = searchOLX()
        print(ads)
    

class GeoservicesTests(unittest.TestCase):
    
    def test_batch_geocode(self):
        addresses = [
            'Rua Sorocaba, Cordeiro, Recife, PE, 50721530',
            'Rua Salema, Várzea, Recife, PE, 50960040',
            'Rua General Polidoro, Várzea, Recife, PE, 50740050',
        ]
        expected = [
            {
                'address': addresses[0],
                'lat': -8.0518979,
                'lng': -34.9361836,
            },
            {
                'address': addresses[1],
                'lat': -8.0382035,
                'lng': -34.9773413,
            },
            {
                'address': addresses[2],
                'lat': -8.0391645,
                'lng': -34.9461157,
            },
        ]
        
        actual = batchGeocodeAddress(addresses)
        self.assertListEqual(actual, expected,)