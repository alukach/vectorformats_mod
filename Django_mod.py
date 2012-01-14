#####################
# VectorFormats Hack
#
# https://github.com/alukach/VectorFormats-Mod
#####################
""" To be used in place of vectorformats.Format.Django """

import pickle
from vectorformats.Feature import Feature
from vectorformats.Formats.Format import Format
from vectorformats.Formats import GeoJSON

class Django(Format):
    """ This class is designed to decode a Django QuerySet object into
        Feature.Vector objects.

        Simply pass a query_set to the decode method, and it will return
        a list of Features.

        Example Usage:

        >>> from vectorformats.Formats import Django, GeoJSON
        >>> qs = Model.objects.filter(city="Cambridge")
        >>> djf = Django.Django(geodjango="geometry", properties=['city', 'state'])
        >>> geoj = GeoJSON.GeoJSON()
        >>> string = geoj.encode(djf.decode(qs))
        >>> print string
    """

    geodjango = False
    """
    If you have GeoDjango geometry columns, set this to the name of the
    geometry column.
    """

    pickled_geometry = False
    """If you are not using GeoDjango, but have instead stored your geometry
       as pickled GeoJSON geometries in a column in GeoDjango, set
       the pickled_geometry=True option in your class constructor.
    """

    pickled_properties = False
    """A column in the database representing a pickled set of attributes.
    This will be used in addition to any properties in the 'properties' list,
    with the list as a preference.
    """

    properties = []
    """
    List of properties you want copied from the model to the output object.
    To span a relationship between models, just use the field name of related
    fields across models, separated by double underscores, until you get to the
    field you want.
    ex. "neighborhood__city__state__stateNameField"
    """

    queries = []
    class Query:
        def __init__(self, queryparameters, filters, returnfields):
            self.queryparameters = queryparameters
            self.filters = filters
            self.returnfields = returnfields
        def getset(self, querybase):
            queryresults = reduce(getattr, self.queryparameters.split('__'), querybase)()
            if self.filters:
                for qfilter in self.filters:
                    queryresults = qfilter.filterset(queryresults)
            allresults = []
            for result in queryresults:
                returneditem = {}
                for field in self.returnfields:
                    returneditem[field] = reduce(getattr, field.split('__'), result)
                allresults.append(returneditem)
            return allresults
    """
    List of Query() objects that access a queryset from which properties are
    copied to the ouput object.  These querysets allow for following one-to-many
    model relationships.  One-to-many model relations return sets of objects
    rather than individual objects.  These sets are optionally filtered to meet
    certain criteria, and then iterated through, returning properties from each
    model to be copied to the oupout object. The Query() object is set up as
    follows:
        queryparameters: the name of the queryset to be retrieved
        filters (Optional):  a list of QSFilter objects to be used to refine the
        queryset results.  See below for QSFilter object description
        returnfields: a list of model fields to be returned from each queryset
        value (similar to 'properties' used above)
        ex. djf.queries = [
                Django.Query(
                    queryparameters = 'event_set__all',
                    returnfields = ['title', 'description', 'category__category']
                    )
                ]
    """

    class QSFilter: #This is used to filter querysets
        def __init__(self, parameters, criteria, ftype='filter'):
            self.ftype = ftype
            self.parameters = parameters
            self.criteria = criteria
        def filterset(self, queryset):
            return getattr(queryset, self.ftype)(**{self.parameters:self.criteria})
    """
        QSFilter:
        ftype (Optional): type of filter to be applied.  Defaults to 'filter',
        options are 'filter' or 'exclude'
        parameters: the lookup parameters
        criteria: value used to filter returned data
        ex. Django.QSFilter(parameters='pub_date__lte', criteria='2006-01-01') is
        similar to appending .filter(pub_date__lte='2006-01-01') to a QuerySet.
        ex. djf.queries = [
                Django.Query(
                    queryparameters = 'event_set__all',
                    filters = [
                        Django.QSFilter(
                            parameters='eventdate__date__exact',
                            criteria='2012-01-01'
                            )
                        ],
                    returnfields = ['title', 'description', 'category__category']
                    )
                ]
    """

    def decode(self, query_set, generator = False):
        results = []
        for res in query_set:
            feature = Feature(res.id)
            if self.pickled_geometry:
                feature.geometry = pickle.loads(res.geometry)

            elif self.geodjango:
                geom = getattr(res, self.geodjango)
                geometry = {}
                geometry['type'] = geom.geom_type
                geometry['coordinates'] = geom.coords
                feature.geometry = geometry

            if self.pickled_properties:
                props = getattr(res, self.pickled_properties)
                feature.properties = pickle.loads(props.encode("utf-8"))

            if self.properties:
                for p in self.properties:
                # This simple change allows us to span relationships between models:
                    # feature.properties[p] = getattr(res, p)
                    feature.properties[p] = reduce(getattr, p.split('__'), res)

            # An argument can be passed to access querysets (one to many relationships)
            # from each value, appending the queryset to the value's 'properties'
            if self.queries:
                for q in self.queries:
                    itemslist = []
                    for queryresult in q.getset(res):
                        item = {}
                        for k,v in queryresult.iteritems():
                            item[k] = v
                        itemslist.append(item)
                    feature.properties[q.queryparameters] = itemslist
            results.append(feature)
        return results
