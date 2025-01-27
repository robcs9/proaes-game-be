import pathlib
import unittest, os
from repository import saveAll, saveAdDF, initDF

class RepositoryTests(unittest.TestCase):
  ads = [
    {
        "id": 1,
        "title": "Cozy Beachfront Apartment",
        "price": "R$ 750000",
        "address": "123 Ocean Drive, Recife, PE",
        "url": "http://example.com/property1",
        "property_type": "Apartment",
        "modifiedAt": "2025-01-10T08:00:00Z",
        "active": True,
        "lat": -8.047562,
        "lng": -34.876964,
        "cep": "50030-000"
    },
    {
        "id": 2,
        "title": "Spacious Downtown Loft",
        "price": "R$ 1200000",
        "address": "456 Central Blvd, Recife, PE",
        "url": "http://example.com/property2",
        "property_type": "Loft",
        "modifiedAt": "2025-01-12T12:30:00Z",
        "active": True,
        "lat": -8.051043,
        "lng": -34.872982,
        "cep": "50050-000"
    },
    {
        "id": 3,
        "title": "Modern Suburban House",
        "price": "R$ 950000",
        "address": "789 Greenway Ave, Recife, PE",
        "url": "http://example.com/property3",
        "property_type": "House",
        "modifiedAt": "2025-01-13T14:15:00Z",
        "active": True,
        "lat": -8.035242,
        "lng": -34.889630,
        "cep": "50040-000"
    },
    {
        "id": 4,
        "title": "Luxury Penthouse",
        "price": "R$ 2200000",
        "address": "101 Sky High Road, Recife, PE",
        "url": "http://example.com/property4",
        "property_type": "Penthouse",
        "modifiedAt": "2025-01-11T10:45:00Z",
        "active": True,
        "lat": -8.033684,
        "lng": -34.894921,
        "cep": "50020-000"
    },
    {
        "id": 5,
        "title": "Charming Country Cottage",
        "price": "R$ 560000",
        "address": "202 Tranquil Lane, Recife, PE",
        "url": "http://example.com/property5",
        "property_type": "Cottage",
        "modifiedAt": "2025-01-09T16:00:00Z",
        "active": True,
        "lat": -8.028374,
        "lng": -34.880914,
        "cep": "50010-000"
    }
  ]
  
  def test_saveAdDF(self):
    ads_df = initDF()
    ad = self.ads[0]
    df = saveAdDF(ads_df, ad)
    # self.assertLogs()
    # implement assertion for the resulting file and its contents
    
  def test_saveAll(self):
    dir = './tests/test-saved-data'
    if not os.path.exists(dir):
      print('O diretório test_saved_data não existe. Criando agora...')
      os.mkdir(dir)
    saveAll(self.ads, dir=dir)
    # self.assertLogs()
    # implement assertion for the resulting file and its contents