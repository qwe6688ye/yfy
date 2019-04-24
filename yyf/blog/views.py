from django.shortcuts import render
from blog.models import Movies
from django.http import HttpResponse
from blog.models import Digital
import requests
from lxml import etree
from selenium import webdriver
import time

# Create your views here.
def load(request):
    Movies.objects.all().delete()
    k=1
    for i in range(0,10):
        url="https://movie.douban.com/top250?start="+str(i*25)+"&filter="
        re=requests.get(url)
        tree=etree.HTML(re.text)
        top250=tree.xpath('//a/span[@class="title"][1]/text()')
    for i in top250:   
        m=Movies(id=k,name=i)
        m.save()
        k=k+1
    return render(request,"list.html")    

def loadshuma(request):
        driver=webdriver.Firefox()
        driver.get("https://www.jd.com/")
        Digital.objects.all().delete()
        searchWhat=driver.find_element_by_id("key")
        #获取id叫做'yschsp'的元素
        searchWhat.clear()
        #通过clear方法，可以将输入框内的字符清空，比较保险的做法
        searchWhat.send_keys("数码")
        #通过send_keys方法把'python'传递给serchWhat元素，即id叫做'yschsp'的元素
        searchBtn=driver.find_element_by_class_name("button")
        #获取id叫做'sbb'的元素，但通常不推荐用class找，用selector能更精确的找到
        searchBtn.click()
        getonepage(driver)
        for i in range(0,9):
                overpage(driver)
        driver.close()
        return render(request,"list.html")
def getonepage(driver):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
        name=driver.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[3]/a/em')
        price=driver.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[2]/strong/i')
        count=driver.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[4]/strong')
        for p,w,q in zip(name,price,count):
                m=Digital(D_name=p.text,D_price=w.text,D_count=q.text)
                m.save()
def overpage(driver):
        driver.find_element_by_xpath('//a[@class="pn-next" and @onclick]').click()
        getonepage(driver)
def showMovies(request):
        list=Movies.objects.all()
        return render(request,'MoviesShow.html',{"m_list":list})
def showDigital(request):
        list=Digital.objects.all()
        return render(request,'DigitalShow.html',{"d_list":list}) 