- 
  - Creating objects

    ```python
    
    from weblog.models import Blog
    
    # Use (keyword arguments) to instantiate Blog model
    b = Blog(name='Beatles Blog', tagline='All')
    b.save()
    ```

  - saving changes to objects

    ``` python
    
    b = Blog.objects.get(pk=1)
    b.name = 'New name2'
    b.save()
    
    # saving foreignKey
    entry = Entry.objects.get(pk=1)
    entry.blog = b
    
    # saving ManyToManyField
    a1 = Author.objects.get(pk=1)
    a2 = Author.objects.get(pk=2)
    
    # 
    entry.authors.add(a1)
    entry.authors.add(a2)
    
    # 
    entry.authors.add(a1, a2)
    
    entry.save()
    
    ```

- Retrieving (检索)

  - all objects

    ``` python
    all_entries = Entry.objects.all()
    
    ```













- Copying model instances

  -  

    ``` python
    
    
    ```

    





- Aggregation

  - Cheat Sheet(小抄)

    ``` python
    # 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # 
    from django.db.models import FloatField, Max, Avg, Count, Q
    
    # 需求, 查询Publisher(出版社)的信息 [该出版社下的大于5分评价的书的数量]
    above_5 = Count('book', filter=Q(book__rating__gt=5))
    below_5 = Count('book', filter=Q(book__rating__lte)=5)
    # 为QuerySet添加聚合后的字段
    pubs = Publisher.objects.annotate(below_5=below_5).annotate(above_5=avbove_5)
    
    
    ```

    





- testing

  -  

  - ``` shell
    
    
    # run all the tests in the animals.tests moudle
    
    $ ./manage.py test animals.tests
    
    
    
    
    
    ```

  - 