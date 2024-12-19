import unittest
import geoservices as ctc
import plot
import re
from repository import getAds
from repository import toGeojson
from repository import makeFeatures
        
class CepToCoordsTests(unittest.TestCase):
    
    def test_coordinates_retrieval(self):
        # self.assertEqual(ctc.getCoordsFromCep('50810000'), {'lat': '1', 'lng': '2'})
        pass
    def test_batch_geocode(self):
        # res = ctc.batchGeocode(['54330-075','54000-000','55000-000'])
        # aprint(res)
        pass

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
