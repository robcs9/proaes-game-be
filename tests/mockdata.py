mock_unfiltered_ads = [
    {
        'subject': 'Cozy Beachfront Apartment',
        'url': 'http://example.com/property1',
        'title': 'Cozy Beachfront Apartment',
        'price': 'R$ 750000',
        'address': 'Rua Sorocaba, Cordeiro, Recife, PE, 50721530',
        'category': 'Apartment',
    },
    {
        'foo': 'bar'
    },
    {
        'subject': 'Spacious Downtown Loft',
        'url': 'http://example.com/property2',
        'title': 'Spacious Downtown Loft',
        'price': 'R$ 1200000',
        'address': 'Rua Salema, Várzea, Recife, PE, 50960040',
        'category': 'Loft',
    },
    {
        'subject': 'Loft at Rua General Polidoro',
        'url': 'http://example.com/property3',
        'title': 'Loft at Rua General Polidoro',
        'price': 'R$ 3200000',
        'address': 'Rua General Polidoro, Várzea, Recife, PE, 50740050',
        'category': 'Loft',
    },
    {
        'fizz': 'buzz'
    },
]
mock_addresses = [
    'Rua Sorocaba, Cordeiro, Recife, PE, 50721530',
    'Rua Salema, Várzea, Recife, PE, 50960040',
    'Rua General Polidoro, Várzea, Recife, PE, 50740050',
]
mock_geocodes = {
    mock_addresses[0]: {
        'lat': -8.0518979 ,
        'lng': -34.9361836,
    },
    mock_addresses[1]: {
        'lat': -8.0382035,
        'lng': -34.9773413,
    },
    mock_addresses[2]: {
        'lat': -8.0391645,
        'lng': -34.9461157,
    },
}

mock_ads = [
    {
        'url': 'http://example.com/property1',
        'title': 'Cozy Beachfront Apartment',
        'price': 'R$ 750000',
        'address': 'Rua Sorocaba, Cordeiro, Recife, PE, 50721530',
        'property_type': 'Apartment',
    },
    {
        'url': 'http://example.com/property2',
        'title': 'Spacious Downtown Loft',
        'price': 'R$ 1200000',
        'address': 'Rua Salema, Várzea, Recife, PE, 50960040',
        'property_type': 'Loft',
    },
    {
        'url': 'http://example.com/property3',
        'title': 'Loft at Rua General Polidoro',
        'price': 'R$ 3200000',
        'address': 'Rua General Polidoro, Várzea, Recife, PE, 50740050',
        'property_type': 'Loft',
    },
]
mock_geocoded_ads = [
    {
        'url': 'http://example.com/property1',
        'title': 'Cozy Beachfront Apartment',
        'price': 'R$ 750000',
        'address': 'Rua Sorocaba, Cordeiro, Recife, PE, 50721530',
        'property_type': 'Apartment',
        'lat': -8.0518979 ,
        'lng': -34.9361836,
    },
    {
        'url': 'http://example.com/property2',
        'title': 'Spacious Downtown Loft',
        'price': 'R$ 1200000',
        'address': 'Rua Salema, Várzea, Recife, PE, 50960040',
        'property_type': 'Loft',
        'lat': -8.0382035,
        'lng': -34.9773413,
    },
    {
        'url': 'http://example.com/property3',
        'title': 'Loft at Rua General Polidoro',
        'price': 'R$ 3200000',
        'address': 'Rua General Polidoro, Várzea, Recife, PE, 50740050',
        'property_type': 'Loft',
        'lat': -8.0391645,
        'lng': -34.9461157,
    },
]