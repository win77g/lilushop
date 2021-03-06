from django.shortcuts import render
from products.models import *
from filters.models import *
from django.db.models import Q
from django.http import Http404,HttpResponseRedirect
from django.core.paginator import Paginator
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.db.models import Count
import collections
import operator
from itertools import chain
from more_itertools import unique_justseen,unique_everseen
from queryset_sequence import QuerySetSequence
from functools import reduce

# Create your views here.
def category_filter_sort(request):
    if request.POST:
        print('верх category_filter_sort')
        data = request.POST["price"]
        # создали сессию и положили туда price
        request.session['sort'] = data
        # достали subcategory из сессии
        subcategory = request.session.get('subcategory')
        # достали из сессии данные фильтрации
        height = request.session.get('height')
        deep = request.session.get('deep')
        width = request.session.get('width')
        if height:
           height = height[0]
        if deep:
           deep = deep[0]
        if width:
           width = width[0]
        # достали price из сессии
        sort = request.session.get('sort')
        change_sort = ''
        # получаем slug
        slug = request.session.get('slug')
        categorys = Category.objects.get(slug = slug)
        # получаем attributes
        attributes = Attributs.objects.annotate(Count('product')).filter(category = categorys).values()
        filters_higth = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Высота').values()
        filters_deep = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Глубина').values()
        filters_width = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Ширина').values()
        #
        # cat = FilterCategory.objects.all().values()
        # pr = ProductFilter.objects.all().values('product','filter_category','values')
        d = request.session.get('d')
        product= []
        prod= []
        for q in d:
          prod = Product.objects.filter(is_active=True, id =q).values()
          product.append(reduce(QuerySetSequence, prod))

        count = len(product)
         # сортировка
        if sort == '-price':
          product = sorted(product,key=lambda x: x['price'], reverse=True)
        if sort == 'price':
          product = sorted(product,key=lambda x: x['price'], reverse=False)
        #  пагинация
        page = request.GET.get('page',1)
        paginator = Paginator(product, 9)  # Show 25 contacts per page
        try:
           product_page = paginator.get_page(page)
        except PageNotAnInteger:
           product_page = paginator.page(1)
        except EmptyPage:
           product_page = paginator.page(paginator.num_pages)
        if subcategory:
         subcategory = subcategory[0]
         att = Attributs.objects.get(id = subcategory)
         prod = Product.objects.filter(is_active=True, attributes = subcategory)
         count = prod.count()
        # сортируем
         product = prod.order_by(sort)
         #  пагинация
         page = request.GET.get('page',1)
         paginator = Paginator(product, 9)  # Show 25 contacts per page
         try:
           product_page = paginator.get_page(page)
         except PageNotAnInteger:
           product_page = paginator.page(1)
         except EmptyPage:
           product_page = paginator.page(paginator.num_pages)
        # else:
        #   print('hi')
    else:
       print('низ category_filter_sort')
       sort = request.session.get('sort')
       # достали subcategory из сессии
       subcategory = request.session.get('subcategory')
       # достали из сессии данные фильтрации
       height = request.session.get('height')
       deep = request.session.get('deep')
       width = request.session.get('width')
       if height:
         height = height[0]
       if deep:
           deep = deep[0]
       if width:
           width = width[0]
       # достали price из сессии
       sort = request.session.get('sort')
       change_sort = ''
       # получаем slug
       slug = request.session.get('slug')
       categorys = Category.objects.get(slug = slug)
       # получаем attributes
       attributes = Attributs.objects.annotate(Count('product')).filter(category = categorys).values()
       filters_higth = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Высота').values()
       filters_deep = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Глубина').values()
       filters_width = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Ширина').values()

       # cat = FilterCategory.objects.all().values()
       # pr = ProductFilter.objects.all().values('product','filter_category','values')
       d = request.session.get('d')
       product= []
       prod= []
       for q in d:
          prod = Product.objects.filter(is_active=True, id =q).values()
          product.append(reduce(QuerySetSequence, prod))

       count = len(product)
       # сортировка
       if sort == '-price':
          product = sorted(product,key=lambda x: x['price'], reverse=True)
       if sort == 'price':
          product = sorted(product,key=lambda x: x['price'], reverse=False)
       #  пагинация
       page = request.GET.get('page',1)
       paginator = Paginator(product, 9)  # Show 25 contacts per page
       try:
           product_page = paginator.get_page(page)
       except PageNotAnInteger:
           product_page = paginator.page(1)
       except EmptyPage:
           product_page = paginator.page(paginator.num_pages)
       if subcategory:
         subcategory = subcategory[0]
         att = Attributs.objects.get(id = subcategory)
         prod = Product.objects.filter(is_active=True, attributes = subcategory)
         count = prod.count()
        # сортируем
         product = prod.order_by(sort)
         #  пагинация
         page = request.GET.get('page',1)
         paginator = Paginator(product, 9)  # Show 25 contacts per page
         try:
           product_page = paginator.get_page(page)
         except PageNotAnInteger:
           product_page = paginator.page(1)
         except EmptyPage:
           product_page = paginator.page(paginator.num_pages)
    return render(request,'category_filter.html', locals())


def category_filter(request):
    if request.POST:
     print('верх category_filtter')
     data = request.POST.getlist("subcategory")
     height = request.POST.getlist("height")
     request.session['height'] = height
     deep = request.POST.getlist("deep")
     request.session['deep'] = deep
     width = request.POST.getlist("width")
     request.session['width'] = width

     if height:
         height = height[0]
     if deep:
         deep = deep[0]
     if width:
         width = width[0]
     request.session['subcategory'] = data
     # достали price из сессии
     sort = request.session.get('sort')
     # достали slug из session
     slug = request.session.get('slug')
     categorys = Category.objects.get(slug = slug)
     # получаем attributes
     attributes = Attributs.objects.annotate(Count('product')).filter(category = categorys).values()
     # данные для фильтрации
     filters_higth = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Высота').values()
     filters_deep = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Глубина').values()
     filters_width = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Ширина').values()
     # filters = FilterSelect.objects.all().values()
     # cat = FilterCategory.objects.all().values()
     pr = ProductFilter.objects.all().values()
     print(pr)
     change_sort = ''

     prod_filter = ProductFilter.objects.filter(Q(filter_category = 'Высота', values = height)|Q(filter_category = 'Глубина', values = deep)|Q(filter_category = 'Ширина', values = width)).values()
     print(1)
     print(prod_filter)
     # обьеденяем словарики
     z = list(prod_filter)
     # получаем словари с повторение больше двух совпадений
     q = get_repit_items(z)
     print(2)
     print(q)
     # выделяем уникальные словарики по product_id
     w=[]
     if q:
       w = list(unique_everseen( q , key= operator.itemgetter('product_id') ))
     else:
         # получаем словари с повторение больше одного совпадений
       s = get_repit_items_two(z)
       w = list(unique_everseen( s , key= operator.itemgetter('product_id') ))
     if not w:
       # если ввели в поиск одно значение
       w = list(unique_everseen( z , key= operator.itemgetter('product_id') ))
     print(3)
     print(w)
     d =[]
     for item in w:
         if (item['product_id']):
            d.append(item['product_id'])
     request.session['d'] = d

     product= []
     prod= []
     if d:
       for q in d:
         prod = Product.objects.filter(is_active=True, id =q).values()
         product.append(reduce(QuerySetSequence, prod))

     else:
        data_atr = data[0]
        prod = Product.objects.filter(is_active=True, attributes = data_atr).values()
        att = Attributs.objects.get(id = data_atr)
        product = list(prod)
     product = list(product)
     count = len(product)
     # max_price = ''
     # if product:
     #  max_price = max(product,key=lambda x: x['price'])
     #  max_price = max_price['price']
     # сортировка
     if sort == '-price':
       product = sorted(product,key=lambda x: x['price'], reverse=True)
     if sort == 'price':
       product = sorted(product,key=lambda x: x['price'], reverse=False)
     # #  пагинация
     page = request.GET.get('page',1)
     paginator = Paginator(product, 9)  # Show 25 contacts per page
     try:
        product_page = paginator.get_page(page)
     except PageNotAnInteger:
        product_page = paginator.page(1)
     except EmptyPage:
        product_page = paginator.page(paginator.num_pages)
    else:
     print('низ category_filtter')

        #  пагинация
     data = request.session.get('subcategory')
     sort = request.session.get('sort')
     change_sort = ''
     slug = request.session.get('slug')
     categorys = Category.objects.get(slug = slug)
     # создали сессию и положили туда Slug

     # получаем attributes
     # attributes = Attributs.objects.filter(category = categorys).values()
     # получаем данные для фильтра по категории
     filters_higth = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Высота').values()
     filters_deep = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Глубина').values()
     filters_width = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Ширина').values()
     cat = FilterCategory.objects.all().values()
     pr = ProductFilter.objects.all().values('product','filter_category','values')


     attributes = Attributs.objects.annotate(Count('product')).filter(category = categorys).values()

     d = request.session.get('d')
     product= []
     prod= []
     if d:
       for q in d:
         prod = Product.objects.filter(is_active=True, id =q).values()
         product.append(reduce(QuerySetSequence, prod))

     else:
        data_atr = data[0]
        prod = Product.objects.filter(is_active=True, attributes = data_atr).values()
        att = Attributs.objects.get(id = data_atr)
        product = list(prod)
     product = list(product)
     count = len(product)
     # max_price = ''
     # if product:
     #  max_price = max(product,key=lambda x: x['price'])
     #  max_price = max_price['price']
     # сортировка
     if sort == '-price':
       product = sorted(product,key=lambda x: x['price'], reverse=True)
     if sort == 'price':
       product = sorted(product,key=lambda x: x['price'], reverse=False)
     # #  пагинация
     page = request.GET.get('page',1)
     paginator = Paginator(product, 9)  # Show 25 contacts per page
     try:
        product_page = paginator.get_page(page)
     except PageNotAnInteger:
        product_page = paginator.page(1)
     except EmptyPage:
        product_page = paginator.page(paginator.num_pages)


    return render(request,'category_filter.html',locals())

# вывод страницы с категориям
def category(request,slug):
    if request.POST:
     print('верх category')
     data = request.POST["price"]
     # создали сессию и положили туда price
     request.session['sort'] = data
     # достали price из сессии
     sort = request.session.get('sort')
     change_sort = ''

     categorys = Category.objects.get(slug = slug)

     # получаем attributes
     attributes = Attributs.objects.annotate(Count('product')).filter(category = categorys).values()

     # данные для фильтрации
     filters_higth = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Высота').values()
     filters_deep = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Глубина').values()
     filters_width = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Ширина').values()
     # filters = FilterSelect.objects.all().values()
     cat = FilterCategory.objects.all().values()
     pr = ProductFilter.objects.all().values('product','filter_category','values')
     # print(attributes)
     product= []
     prod = Product.objects.filter(is_active=True, categ = categorys).values()
     # подсчет продуктов
     product = list(prod)
     # максимальная и минимальная цена для фильтра
     # max_p = max(product,key=lambda x: x['price'])
     # max_p = max_p['price']
     # min_p = min(product,key=lambda x: x['price'])
     # min_p = min_p['price']
     # сортировка
     if sort == '-price':
      product = sorted(product,key=lambda x: x['price'], reverse=True)
     if sort == 'price':
       product = sorted(product,key=lambda x: x['price'], reverse=False)
     #   print(product)
     count = len(prod)
     #  пагинация
     page = request.GET.get('page',1)
     paginator = Paginator(product, 9)  # Show 25 contacts per page
     try:
        product_page = paginator.get_page(page)
     except PageNotAnInteger:
        product_page = paginator.page(1)
     except EmptyPage:
        product_page = paginator.page(paginator.num_pages)
    else:
     print('низ category')
     sort = request.session.get('sort')
     change_sort = ''
     categorys = Category.objects.get(slug = slug)
     # создали сессию и положили туда Slug
     request.session['slug'] = slug
     # получаем attributes
     attributes = Attributs.objects.filter(category = categorys).values()
     # получаем данные для фильтра по категории
     filters_higth = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Высота').values()
     filters_deep = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Глубина').values()
     filters_width = FilterSelect.objects.filter(category_id = categorys,filter_category_id = 'Ширина').values()
     # cat = FilterCategory.objects.all().values()
     # pr = ProductFilter.objects.all().values('product','filter_category','values')
     attributes = Attributs.objects.annotate(Count('product')).filter(category = categorys).values()

     product= []
     prod = Product.objects.filter(is_active=True, categ = categorys).values()
     # подсчет продуктов
     product = list(prod)
     # максимальная и минимальная цена для фильтра
     # max_p = max(product,key=lambda x: x['price'])
     # max_p = max_p['price']
     # min_p = min(product,key=lambda x: x['price'])
     # min_p = min_p['price']
     # сортировка
     if sort == '-price':
       product = sorted(product,key=lambda x: x['price'], reverse=True)
     if sort == 'price':
       product = sorted(product,key=lambda x: x['price'], reverse=False)
     count = len(prod)
        #  пагинация
     page = request.GET.get('page',1)
     paginator = Paginator(product, 9)  # Show 25 contacts per page
     try:
        product_page = paginator.page(page)
     except PageNotAnInteger:
        product_page = paginator.page(1)
     except EmptyPage:
        product_page = paginator.page(paginator.num_pages)

    # except Category.DoesNotExist:
    #         raise Http404("Такой категории несушествует")

    return render(request,'category.html',locals())
# -------sort-------------------------------------------------------------------
def sort(request):
    # print(request)
    # try:
    #  categorys = Category.objects.get(id = data.id)
    #  products = Product.objects.get(is_active=True, categ = categorys)
    #  product= products.order_by(data)
    # except Category.DoesNotExist:
    #         raise Http404("Такой категории несушествует")
    return render(request,'category.html')
# вывод продукта детально-------------------------------------------------------
def product_detail(request,slug):
    # print(slug)
    try:
      # captcha = ReCaptchaField(widget=ReCaptchaWidget())
      product = Product.objects.filter(is_active=True, slug = slug)
      gallery = ProductImage.objects.filter(product__in = product)
      # print(imagegallery)
      # создаем сессию
      session_key = request.session.session_key
      if not session_key:
         request.session.cycle_key()
      # print (request.session.session_key)
    except Product.DoesNotExist:
            raise Http404("Такойго продукта несушествует")
    return render(request,'product_detail.html',context={'product':product,'gallery':gallery})

# больше двух совпадений
def get_repit_items(z, key="product_id"):
    # Count how many times each key occurs.
    key_count = collections.defaultdict(lambda: 0)
    for d in z:
        key_count[d[key]] += 1
    # Now return a list of only those dicts with a unique key.
    #Еси нужно отсеить повторяющиеся ==1 , Еси нужно повторяющиеся > 1
    return [d for d in z if key_count[d[key]] > 2]
# больше одного совпадений
def get_repit_items_two(q, key="product_id"):
    # Count how many times each key occurs.
    key_count = collections.defaultdict(lambda: 0)
    for d in q:
        key_count[d[key]] += 1
    # Now return a list of only those dicts with a unique key.
    #Еси нужно отсеить повторяющиеся ==1 , Еси нужно повторяющиеся > 1
    return [d for d in q if key_count[d[key]] > 1]
