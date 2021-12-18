import scrapy
from ..items import AarhusboligItem
"""Følger https://www.pythongasm.com/introduction-to-scrapy/"""
j = 0

class LejeboligerSpider(scrapy.Spider):
    name = 'lejeboliger'
    """allowed_domains = ['https://aarhusbolig.dk']"""
    start_urls = ['https://aarhusbolig.dk/Soeg-bolig?Fritekst=&8000+Aarhus+C=01&omr-data-carrier=8000+Aarhus+C&BoligOmraader=01&org-data-carrier=&Selskaber=&bolig-data-carrier=&BoligTyper=&FloorWish.Min=&FloorWish.Max=&min-data-carrier=&HuslejeMin=&max-data-carrier=&HuslejeMax=&antv-data-carrier=&AntalVaerelser=&antvmax-data-carrier=&AntalVaerelserMax=&div-data-carrier=&BoligArealMin=0&BoligArealMax=200&orderby=&sort=']

    def parse(self, response):
        print("\n")
        print("HTTP STATUS: "+str(response.status))
        print(response.css("title::text").get())
        print(response.url)
        print("\n")

        # der findes også en mobil del til html siden, desktopContainer plugger desktop delen.
        desktopContainer = response.css("div.desktop-only-large")
        allAds = desktopContainer.css("div.hc-details")
        allAds[0].get()
        # firstAd = allAds[0]
        for ad in allAds:
            # ny, tilføj adresse info
            #Y1 = pd.DataFrame([ad.css("div.hc-address>p::text").getall()],columns=["Afdeling", "Adresse", "Postnummer"])
            #Y.append(Y1,ignore_index=True)
            hcAddress = ad.css("div.hc-address>p::text").getall()
            if len(hcAddress) == 3 :
                [afdeling, adresse, postnummer] = hcAddress
            else:
                [afdeling, postnummer] = hcAddress
                adresse = ""

            details = ad.css("table.hc-bolig-data")
            boligtype = details.css("td::text")[0].get()
            no_of_appartments = details.css("td::text")[1].get()
            værelser = details.css("td::text")[2].get()
            area = details.css("td::text")[3].get()
            extraInfo = ad.css("div.hc-extra-info")
            googlemaps = extraInfo.css('a.icon-map::attr(href)').get()

            if googlemaps is None:
                googlemaps = 'link mangler'
                koordinates = 'Na,Na'
            else:
                koordinates = googlemaps[googlemaps.rfind("|")+1:]
                [Y,X] = [float(x) for x in koordinates.split(',') ]


            price = extraInfo.css("span.hc-price::text").get()
            boligLink = 'https://aarhusbolig.dk' + extraInfo.css("a.hc-link::attr(href)").get()

            print("====NEW PROPERTY===")
            print(area)
            print(price)

            print("\n")

            """
            items = AarhusboligItem()

            items['area'] = area
            items['price'] = price

            yield items
            """
            yield {
                'Rooms' : værelser,
                'Area' : area,
                'Price' : price,
                'Afdeling': afdeling,
                'Adresse' : adresse,
                'Postnummer' : postnummer,
                'Googlemaps' : googlemaps,
                'X koordinate' : X,
                'Y koordinate' : Y,
                'Bolig link' : boligLink
            }

        """ Følgende er et forsøg på at følge links til næste side, det ser dog ud til at den bare
        indsætter side 1 om og om igen in i csv output filen, så der er et eller andet mellem overstående og
        nedestående der der ikke hænger sammen... måske skal link statement være indlejret i overstående
        for loop?

        for at stoppe med at følge link kigger jeg efter om der findes en "span.icon-arrow-right" med
        regular expression."""

        next_page_button = response.css('div.desktop-only-large')[-1].css('a.btn')[-1]
        last_page_check = next_page_button.css('span.icon-arrow-right::attr(class)').re(r'right')

        if last_page_check is not None:
            next_page = next_page_button.css('a::attr(href)').get()
            next_page = response.urljoin(next_page)
            #j += 1
            #print("page {}".format(j),end='\n')
            yield scrapy.Request(next_page, callback=self.parse)

"""
nedestående kommer af at højre-klikke > copy > xpath etc i web debugger tool:
/html/body/div[1]/div[2]/div/div[4]/div/ul/li[1]/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]
html.no-js body div.w-page div.w-document div.result-page.search-page.js-document--result div.housecard-slider-container div.housecard-slider.w-housecards.desktop-only-large ul.l-housecards.search-housecards li.search-housecard div.slide-inner div.hc.b-89_s-31_a-4_r-1 div.hc-details div.hc-specs table.hc-bolig-data tbody tr td
div.desktop-only-large:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)
<td>41 m<sup>2</sup></td>
"""
