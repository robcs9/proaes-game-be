# todo - add missing imports

# WQ multi-pages test url
# testing-only, keep commented out otherwise
# url_wq = "https://www.webquarto.com.br/busca/quartos/recife-pe?page=1&price_range[]=0,15000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"


def findDataWQ(raw):
    # target text between 'window.search' and 'window.search.city_name'
    for line in raw:
        content = line.get_text().strip()
        begin = "window.search = {"
        end = "window.search.city_name"
        if content.find(begin) > -1:
            end_idx = content.find(end)
            data_str = content[len(begin) - 1 : end_idx].strip()[:-1]
            rest_str = content[end_idx:]
            return data_str, rest_str
    return ""

def findPaginationWQ(src):
    arr = src.split(" = ")
    s = arr[3]
    end = s.find("window")
    s = s[:end - 4]
    return json.loads(s)

# Remove caracteres com encoding irrelevante
def sanitizeWQ(s):
    import ast, re, html
    
    # Remove caracteres unicode irrelevantes (emojis, etc.)
    #r = codecs.charmap_encode(re.sub(r'\\/', '/', s), 'ignore')[0].decode('unicode_escape')
    # r = codecs.charmap_encode(s, 'ignore')[0]#.decode('unicode_escape')
    r = re.sub(r'\\/', '/', s)
    charmap_tuple = codecs.charmap_encode(r, 'ignore')
    u_escaped = charmap_tuple[0].decode('unicode_escape', 'replace')
    
    # Remove surrogate pairs (html emojis (e.g.: '\ud83d\udc4', ' &#55356;&#57117;' ) )
    emojiless_str = re.sub(r'[\uD800-\uDFFF]', '', u_escaped)
    # r = re.sub(r'\\u[0-9a-fA-F]{4}', '', r)
    emojiless_str = re.sub(r'\\u[0-9a-fA-F]{4}', '', emojiless_str)
    # bullet point removal
    # emojiless_str = re.sub(r'&\#[a-zA-Z0-9]{1,5}', '', emojiless_str)
    result = emojiless_str
    result = re.sub(r"[\n\r]", r" ", result)
    
    # undef_chars = result.strip().split()
    # for w in undef_chars:
    #     print(w)
    # print(f'length: {len(undef_chars)}')
    return result

# parses string data from WebQuarto to JSON
def adsDataToJsonWQ(data_str):
    ads = []
    # set loads 'strict' arg to False to allow unescaped characters
    data = json.loads(data_str,strict=False)['ads']
    
    for d in data:
        # Compare and normalize both data shapes
        ad = {
            'url': d['url'], 
            'title': f"{d['title']}",# {d['description']}. {d['about_roommate']}",
            'thumbnail': d['main_photo'],
            'price': d['rent_price'],
            'address': f"{d['address']}, {d['location']}",
            'property_type': f"{d['property_type']}. {d['room_type']}",
            'latlng': f'{d['lat']},{d['lng']}',
            'lat': d['lat'],
            'lng': d['lng'],
            'active': True,
            'modifiedAt': utils.dateTimeNow()
        }
        ads.append(ad)
    return ads


def searchWQ():
    soup = makeSoup(url_wq)
    raw_scripts = soup.find_all("script")
    ads = []
    
    data_str, pagination = findDataWQ(raw_scripts)
    pagination = findPaginationWQ(pagination)
    data_str = sanitizeWQ(data_str)
    ads.append(adsDataToJsonWQ(data_str))
    print(f"WebQuarto Page 1 done")
    
    for i in range(pagination['last_page'] - 1):
        page_url = f"https://www.webquarto.com.br/busca/quartos/recife-pe?page={i + 1}&price_range[]=0,15000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"
        makeSoup(page_url)
        raw_scripts = soup.find_all("script")
        data_str, _ = findDataWQ(raw_scripts)
        data_str = sanitizeWQ(data_str)
        ads.append(adsDataToJsonWQ(data_str))
        print(f"WebQuarto Page {i+1} done")
    
    # Dados dos anúncios em flat list
    ads = [item for sublist in ads for item in sublist]
    return ads
