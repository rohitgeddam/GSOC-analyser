import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.google-melange.com"



def get_gsoc_year():
    url="https://www.google-melange.com/archive/gsoc"
    r = requests.get(url)
    content = r.content
    s = BeautifulSoup(content,'html.parser')

    #class="mdl-list__item mdl-list__item--one-line"
    data = {}
    all_links = s.findAll("li", {"class": "mdl-list__item mdl-list__item--one-line"})
    # for x in all_links:
    #     #data.append(x.find('a')['href'])
    #     url = BASE_URL + x.find('a')['href']
    #     data[x.text] = url

    # return links #{"2015" : "links"} but we want {"2015" : {"links" : "-----","about": "#####","icons":"url of icon"}}
    for x in all_links:
        url = BASE_URL + x.find('a')['href']
        # data[(x.text).rstrip('\n')]
        data[(x.text).strip('\n')] = {}
        data[(x.text).strip('\n')]["Year_Link"] = url

    return data


def get_list_of_org():
    #class = mdl-list__item mdl-list__item--one-line
    data = get_gsoc_year()


    for key,val in data.items():
        url = data[key]["Year_Link"]
        r = requests.get(url)
        content = r.content
        s = BeautifulSoup(content,'html.parser')
        #span-class = mdl-list__item-primary-content
        orgs = s.findAll('li',{"class":"mdl-list__item mdl-list__item--one-line" })
        # imgs = s.findAll('img',{"class":"small-logo"})
        data[key]["Org_list"] = {}
        for org in orgs:
            org_name = org.find('span',{'class':"mdl-list__item-primary-content"}).find('a').text
            url = BASE_URL + org.find('span',{'class':"mdl-list__item-primary-content"}).find('a')['href']
            #sicon_src = org.find('span',{'class':"small-logo-box mdl-list__item-icon"}).get('img') #returning none object.
            # sicon_src = org.find('img',{'class':"small-logo"})
            # img_src = sicon_src.find('img',{'class':"small-logo"})
            #class="small-logo-box mdl-list__item-icon"
            data[key]["Org_list"][org_name] = {}
            data[key]["Org_list"][org_name]["url"] = url
            # data[key]["Org_list"][org_name]["Logo-small"] = sicon_src
            # data[key]["Org_list"][org_name]["Logo-large"] = ''


            # data[key]["Org_list"]["url"] = url
    return data

def get_projects_of_org():
    data = get_list_of_org()

    for key,val in data.items():
        url = data[key]["Org_list"]
        for org , org_url in url.items():
            #org['Projects'] = {}


            url_of_orgs = org['url']

            r = requests.get(url_of_orgs)
            content = r.content
            s = BeautifulSoup(content,'html.parser')

            urls_of_projects = s.findAll('li',{'class':"mdl-list__item mdl-list__item--two-line"})
            #this returns a list of urls_of_projects
            for x , y in urls_of_projects:
                hf = x.find('span',{"class":"mdl-list__item-primary-content"}).find("a")["href"]
                name = x.find('span',{"class":"mdl-list__item-primary-content"}).find("a").text
                desc = x.find('span',{"class":"mdl-list__item-sub-title"}).text

                #{name:{hf:"#",desc="#"}}
                org['Projects']["name"] = name
                org['Projects']["name"]["link"] = hf
                org['Projects']["name"]["description"] = desc


            # class = mdl-list__item mdl-list__item--two-line

    return data


# get_list_of_org()
print(get_projects_of_org())
# data = get_gsoc_year()
# for key,val in data.items():
#     print(data[key]["Year_Link"])
