import utils

class Ad:
  active = True
  
  def __init__(self, id, title, property_type,
  address, price, url, lat, lng):
    self.id = id
    self.title = title
    self.property_type = property_type
    self.address = address
    self.price = price
    self.url = url
    self.lat = lat
    self.lng = lng
    self.modifiedAt = utils.dateTimeNow()
  
  def __init__(self, ad: dict):
    self.id = ad['id']
    self.title = ad['title']
    self.property_type = ad['property_type']
    self.address = ad['address']
    self.price = ad['price']
    self.url = ad['url']
    self.lat = ad['lat']
    self.lng = ad['lng']
    self.modifiedAt = utils.dateTimeNow()
  
    def getId(self):
      return self.id
    def getTitle(self):
      return self.title
    def getProperty_type(self):
      return self.property_type
    def getAddress(self):
      return self.address
    def getPrice(self):
      return self.price
    def getUrl(self):
      return self.url
    def getLat(self):
      return self.lat
    def getLng(self):
      return self.lng
    def getActive(self):
      return self.active
    def getModifiedAt(self):
      return self.modifiedAt
    
    def setId(self, id):
      self.id = id
    def setTitle(self, title):
      self.title = title
    def setProperty_type(self, property_type):
      self.property_type = property_type
    def setAddress(self, address):
      self.address = address
    def setPrice(self, price):
      self.price = price
    def setUrl(self, url):
      self.url = url
    def setLat(self, lat):
      self.lat = lat
    def setLng(self, lng):
      self.lng = lng
    def setActive(self, active):
      self.active = active
    def setModifiedAt(self):
      self.modifiedAt = utils.dateTimeNow()
      
    # def isEqual(self, ad: Ad):
    #   pass