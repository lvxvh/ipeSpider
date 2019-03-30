class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


if __name__ == "__main__":
    cookie = 'acw_tc=7b39758215520138409462380e7a4b67d2903e854ba217a1ef28dbd7e4fa7e; __utmz=105455707.1552013845.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); .ASPXAUTH=40A0CFD58B1441002300306235BFB8DAB2FB59D2F48C392A723FB0B2EFB063C562455D4192F4BC5E4BCBBE418B5806C1F7576C71B245692587BAA97FCD0258F21418747B823E4CF65CA11C850860289C79580BD9019C457BEC180B24D565B20D596FDF494DD20190A8D4C60C02FBE6E51C16CBB55B0E8B0458C3AC20590163ED05C0599BB7E8DDF5D50188BE2B7F45046D047BF00BF57450DD00941FEFED26F80D1CC704; ASP.NET_SessionId=aev0dzcd4izuywjpqji54yop; ajaxkey=D8E181A537026674ABA67673D4664F799DEFA487DC07061A; __utma=105455707.1742238327.1552013845.1552612173.1552616192.16; __utmc=105455707; __utmt=1; __utmb=105455707.1.10.1552616192; SERVERID=8abfb74b5c7dce7c6fa0fa50eb3d63af|1552616194|1552616189'
    trans = transCookie(cookie)
    print(trans.stringToDict())