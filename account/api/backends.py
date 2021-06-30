from rest_framework import filters

#need to add in dajango rest_framework setting to add 'SEARCH_PARAM': 'username'
#and then it will only query username
class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('username'):
            return ['username']
        return super(CustomSearchFilter, self).get_search_fields(view, request)
