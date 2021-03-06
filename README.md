#vectorformats_mod#

##Overview##

A modification of [vectorformat](http://packages.python.org/vectorformats/)'s [Django class](http://packages.python.org/vectorformats/formats/Django.html).  This operates exactly in the same way as the original vectorformats, but with two enhancements:

1. The properties you want copied from the model to the output object can now include properties that span a relationship between models.
2. A queryset is additionally able to return querysets for each object, allowing access to each object's [one-to-many relationships](https://docs.djangoproject.com/en/1.4/topics/db/examples/many_to_one/).  Optionally, these querysets can be filtered to meet given criteria.


##Functionality##

###Spanned Relationships###

To span a relationship between models, just use the field name of related fields across models, separated by double underscores, until you get to the field you want.

    >>> from myProject.myApp.vectorformats_mod.Django import Django
    >>> from vectorformats.Formats import GeoJSON
    >>> qs = Model.objects.filter(city="Cambridge")
    >>> djf = Django.Django(geodjango="geometry", properties=['city', 'city__state', 'city__state__country'])
    >>> geoj = GeoJSON.GeoJSON()
    >>> string = geoj.encode(djf.decode(qs))
    >>> print string

###Accessing Querysets of Queried Results###

Querysets can be accessed from each result by adding a `Query()` object to the `queries` list property of the `Django()` object.  The `Query()` object has two mandatory and one optional parameter. These are:

* **queryset_name**: The name of the queryset to be retrieved.
* **properties**: List of properties you want copied from the model to the output object. Spanning relationships between models is allowed.
* **filters** (Optional): List of QSFilter objects to be used to refine the queryset results.  See below for QSFilter object description.


Take, for example, a situation in which you were querying your database for all objects in the City model.  Within the serialized results, you also wish to include each all of the parks within each city (a one-to-many relationship, only retrievable with querysets).  This could be done like so:

    >>> qs = City.objects # Select all cities
    >>> parksInCity = Django.Query(
    ...     queryset_name = 'park_set__all',
    ...     properties = ['park', 'address', 'size']
    ... )
    >>> djf = Django.Django(
    ...     geodjango="geometry", 
    ...     properties=['city', 'city__state', 'city__state__country'],
    ...     queries=[parksInCity]
    ... )

By setting the ``queryset_name`` to ``park_set__all``, we are effectively accessing the ``park_set.all()`` of each value returned in the ``City.objects`` queryset.  This will append the name and address of each park as a property labeled park_set__all, under each city.

Additionally, these querysets can be filtered.  For instance, if you were only interested in parks with a ``size`` property greater than 30 units, you could create a filter.  A full example could be:

    >>> from myProject.myApp.vectorformats_mod.Django import Django
    >>> from vectorformats.Formats import GeoJSON
    >>> from myProject.myApp.models import City
    >>> qs = City.objects # Select all cities
    >>> largeParks = Django.QSFilter(
    ...         parameters='size__gt', 
    ...         criteria=30
    ...  )
    >>> parksInCity = Django.Query(
    ...     queryset_name = 'park_set__all',
    ...     properties = ['park', 'address', 'size']
    ...     filters = [largeParks]
    ... )
    >>> djf = Django.Django(
    ...     geodjango="geometry", 
    ...     properties=['city', 'city__state', 'city__state__country'],
    ...     queries=[parksInCity]
    ... )
    >>> geoj = GeoJSON.GeoJSON()
    >>> string = geoj.encode(djf.decode(qs))
    >>> print string

##Usage##

The vectorformats_mod is to be used in replacement of the standard vectorformats module.

1. Install the module via Pip: ``pip install -e git+git@github.com:alukach/vectorformats_mod.git#egg=vectorformats``
2. Import it in views.py: ``from vectorformats.Django import Django``


