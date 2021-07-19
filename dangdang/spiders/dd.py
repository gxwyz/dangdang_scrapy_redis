import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
from dangdang.items import DangdangItem

'''需要修改'''
class DdSpider(RedisSpider):#需要修改
    name = 'dd'
    allowed_domains = ['dangdang.com']
    #start_urls = ['http://dangdang.com/']
    redis_key = "dangdang"

    #redis-cli
    #redis里面添加一条记录 lpush dangdang http://book.dangdang.com/
    #flushall flushdb
    #keys *
    #llen dd:items
    #lrange dd:items 0 -1
    #lrange dangdang 0 -1

    def parse(self, response):
        #大分类分组
        div_list = response.xpath("//div[@class='con flq_body']/div")
        for div in div_list:
            item = DangdangItem()
            item["b_cate"] = div.xpath("./dl/dt//text()").getall()
            item["b_cate"] = [i.strip() for i in item["b_cate"] if len(i.strip()) > 0] #去掉空字符串
            #中间分类分组
            dl_list = div.xpath("./div//dl[@class='inner_dl']")
            for dl in dl_list:
                item["m_cate"] = dl.xpath("./dt//text()").getall() #作家没有a标签，
                item["m_cate"] = [i.strip() for i in item["m_cate"] if len(i.strip()) > 0][0]  # 去掉空字符串，选列表第一个
                #小分类分组，在a标签下面
                a_list = dl.xpath("./dd/a")
                for a in a_list:
                    item["s_href"] = a.xpath("./@href").get()
                    item["s_cate"] = a.xpath("./text()").get()
                    if item["s_href"] is not None:
                        yield scrapy.Request(
                            item["s_href"],
                            callback=self.parse_book_list,
                            meta={"item":deepcopy(item)}
                        )

    def parse_book_list(self,response):
        item =  response.meta["item"]
        li_list = response.xpath("//ul[@class='bigimg']/li")
        for li in li_list:
            item["book_img"] = li.xpath("./a[@class='pic']/img/@data-original").get()
            item["book_img"] = "http:" + str(item["book_img"])
            item["book_title"] = li.xpath("./p[@class='name']/a/@title").get()
            item["book_author"] = li.xpath("./p[@class='search_book_author']/span[1]/a/text()").getall() #第一个span，有3个
            item["book_desc"] = li.xpath("./p[@class='detail']/text()").get()
            item["book_price"] = li.xpath(".//span[@class='search_now_price']/text()").get()
            item["book_pulish_date"] = li.xpath("./p[@class='search_book_author']/span[2]/text()").get()
            item["book_press"] = li.xpath("./p[@class='search_book_author']/span[3]/a/text()").get()
            yield item

        # 下一页
        next_url = response.xpath("//li[@class='next']/a/@href").get()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item":item}
            )




