#vectorformats Mod#

##Overview##

A modification of vectorformat_'s `Django class <http://packages.python.org/vectorformats/formats/Django.html>`_.  This operates exactly in the same way as the original vectorforats, but with two enhancements:
1. The properties you want copied from the model to the output object can now include properties that span a relationship between models.
2. A queryset is additionally able to return querysets for each object, allowing access to each object's `one-to-many relationships <https://docs.djangoproject.com/en/1.4/topics/db/examples/many_to_one/>`.  Optionally, these querysets can be filtered to meet given criteria.


##Functionality##

###Spanned Relationships###

To span a relationship between models, just use the field name of related fields across models, separated by double underscores, until you get to the field you want.

    >>> from vectorformats.Formats import Django, GeoJSON
    >>> qs = Model.objects.filter(city="Cambridge")
    >>> djf = Django.Django(geodjango="geometry", properties=['city', 'city__state', 'city__state__country'])
    >>> geoj = GeoJSON.GeoJSON()
    >>> string = geoj.encode(djf.decode(qs))
    >>> print string

###Accessing Querysets of Queried Results###

Querysets can be accessed from each result by adding a `Query()` object to the `queries` list property of the `Django()` object.  The `Query()` object has two mandatory and one optional parameter. These are:

* **queryparameters**: The name of the queryset to be retrieved.
* **properties**: List of properties you want copied from the model to the output object. Spanning relationships between models is allowed.
* **filters** (Optional): List of QSFilter objects to be used to refine the queryset results.  See below for QSFilter object description.


Take, for example, a situation in which you were querying a country model for it's states.  Within the serialized results, you also wish to include each state's cities (which would be a one-to-many relationship and only retrievable with querysets).

>>> from vectorformats.Formats import Django, GeoJSON
    >>> qs = Model.objects.filter(city="Cambridge")
    >>> djf = Django.Django(geodjango="geometry", properties=['city', 'city__state', 'city__state__country'])
    >>> geoj = GeoJSON.GeoJSON()
    >>> string = geoj.encode(djf.decode(qs))
    >>> print string

   

For example, imagine that you were serializing the locations of different venues in a city. 
    
    

.. vectorformat_: http://packages.python.org/vectorformats/
