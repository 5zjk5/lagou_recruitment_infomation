from urlManager import urlManager
from htmlDownload import htmlDownload
from parseData import parseData
from dataOutput import  dataOutput
import configparser


class spiderMan():
    '''
    爬虫主模块
    '''
    def __init__(self):
        '''
        初始化各个模块
        '''
        self.manager = urlManager()
        self.download = htmlDownload()
        self.parse = parseData()
        self.ouput = dataOutput()

    def start(self,city,job):
        '''
        开始爬取
        :return:
        '''
        # 创建 csv 文件
        self.ouput.create_csv(city,job)
        # 获取爬取数据的 url
        position_url = self.manager.get_position_url()
        # 爬 30 页
        for pn in range(1,31):

            '''
            买的是动态代理，使用时发现，代理虽然换了，但也常被封，可能是这个代理别人
            也拿去爬拉勾了，所以只要失败就重新换代理再请求
            '''
            while True:
                response = self.download.get_html(pn,position_url,city,job)
                if 'true' not in response.text: # 代表代理失败，请求成功相应中有 true 字符串
                    continue
                else:
                    break

            # 解析爬取数据
            data = self.parse.get_info(response.text)

            if data == None: # 编码错误的页跳过
                continue

            # 判断是否爬取到了最好一页，因为有些职位没有 30 页
            if data == []:
                print('\n爬取完毕或拉勾上此城市没有相关的职位！！！')
                break

            # 写入 csv
            self.ouput.write_to_csv(data,city,job)

            print('\r第 {} 已爬取'.format(str(pn)),end='')

        print('\n爬取完毕，正在生成职位信息报表.....')


if __name__ == '__main__':
    '''
    主接口
    '''
    # 读取同一路径的配置文件
    cf = configparser.ConfigParser()
    cf.read("lagou.conf",encoding='utf8')
    job = str(cf.get('lagou', 'job')).split(',')
    city = str(cf.get('lagou', 'city')).split(',')

    for c in city:
        for j in job:
            spider = spiderMan()
            spider.start(c,j)
            spider.ouput.create_table(c,j) # 生成报表
            print('\n职位报表生成完毕！')