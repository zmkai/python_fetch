from urllib import request
import re
class Spider():
    url = 'https://book.douban.com/top250'
    # root_pattern = '<a href="([\s\S]*?)" onclick="&quot;moreurl(this,{[\s\S]*})&quot;" title="[\s\S]*?">'
    root_pattern = '<div class="pl2">[\s\S]*?</div>'
# <a href="https://book.douban.com/subject/1770782/" onclick="&quot;moreurl(this,{i:'0'})&quot;" title="追风筝的人">
                # 追风筝的人
# <a href="https://book.douban.com/subject/25862578/" onclick="&quot;moreurl(this,{i:'1'})&quot;" title="解忧杂货店">
                # 解忧杂货店

                
            #   </a>
                
            #   </a>
    # 返回所有的书籍信息的一个列表，列表中的数据类型为字典
    def __loop_all_page(self):
        # https://book.douban.com/top250?start=25
        count = 0
        # 控制循环
        books = []
        # while count <= 225 :
        while count <= 225 :
            sub_url = Spider.url+'?start='+str(count)
            links = self.__fetch_one_links(sub_url)
            result_links = self.__analysis_link(links)
            # print(len(result_links))
            # print(result_links)
            book_number = count+1
            for result_link in result_links:
                print('爬取第'+str(book_number)+'本书籍中....')
                book_infos,simple_content,book_name = self.__fetch_bookinfo(result_link)
                dic = self.__analysis_bookinfo(book_infos,simple_content,book_name)
                books.append(dic)
                book_number += 1
            count += 25
        print('爬取结束....')
        print('books的长度为'+str(len(books)))
        return books

    # 抓取一页中包含书籍链接的组
    def __fetch_one_links(self,target_url):
        r = request.urlopen(target_url)
        htmls = r.read()
        htmls = str(htmls,encoding='utf-8')
        # print(htmls)
        links = re.findall(Spider.root_pattern,htmls)
        # print(links[0])
        return links
    # 获取一页中的所有书籍链接，返回一个书籍链接列表
    def __analysis_link(self,links):
        result_links = []
        for link in links:
            link_pattern = ' <a href="([\s\S]*?)"[\s\S]*?>'
            result_link = re.findall(link_pattern,link)
            result_links.append(result_link[0])
        return result_links


    #抓取包含书籍信息的组
    def __fetch_bookinfo(self,link):
        # link = 'https://book.douban.com/subject/1770782/'
        bookinfo_pattern = '<div id="info"[\s\S]*?>([\s\S]*?)</div>'
        simple_pattern = '<div class="intro">([\s\S]*?)</div>'
        book_name_pattern = '<span property="v:itemreviewed">([\s\S]*?)</span>'
        r = request.urlopen(link)
        info_html = r.read()
        info_html = str(info_html,encoding='utf-8')
        simple_content = re.findall(simple_pattern,info_html)
        book_infos = re.findall(bookinfo_pattern,info_html)
        book_name = re.findall(book_name_pattern,info_html)
        # print(book_name)
        # print(book_infos[0])
        # print(simple_content[0])
        return book_infos,simple_content,book_name[0]

    # 获得一本书籍的详情字典信息
    def __analysis_bookinfo(self,book_infos,simple_content,book_name):
        detail_pattern = '<span class="pl">(.*?)</span>([\s\S]*?(<br/>|<br>))'
        info_pattern = '<a href="[\s\S]*?">([\s\S]*?)</a>'
        get_content_pattern = '<p>([\s\S]*?)</p>'
        result1 = re.findall(detail_pattern,book_infos[0])
        dic = {'书名':book_name}
        # print(result1)
        # 处理一本书籍的基本信息
        for t in result1:
            dict1 = {}
            if 'href' in t[1]:
                result2 = re.findall(info_pattern,t[1])
                # print('除去href后的结果')
                # print(result2)
                if len(result2)>0 :
                    temp = result2[0].strip()
                    temp1 = temp.replace('<br/>','')
                    dict1.update({t[0]:temp1})
            else:
                temp = t[1].strip()
                temp1 = temp.replace('<br/>','')
                # dict1 = {t[0]:t[1].strip()}
                dict1.update({t[0]:temp1})
            # print(dict1)
            dic.update(dict1)
        # 处理内容简介
        contents = re.findall(get_content_pattern,simple_content[0])
        content_str = ''
        for i in contents:
            content_str+=i
        dic.update({'内容简介':content_str})
        return dic
    
    def __show_result(self,books):
        number = 1
        for book in books:
            print('--------------------------------------------')
            print('第'+str(number)+'本书籍信息如下:')
            for key in book.keys():
                print(key+'---->'+book.get(key))
            number += 1

    def __test_one_book(self,link):
        book_infos,simple_content,book_name = self.__fetch_bookinfo(link)
        dic = self.__analysis_bookinfo(book_infos,simple_content,book_name)
        print(dic)    

    def go(self):
       books = self.__loop_all_page()
       print(len(books))
       self.__show_result(books)
        # link = 'https://book.douban.com/subject/1007305/'
        # self.__test_one_book(link)

spider = Spider()
spider.go()