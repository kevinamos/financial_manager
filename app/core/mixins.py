from app.accounts.models import User

class CreatorUpdaterMixin(object):

    def create(self, request, *args, **kwargs):
        if 'created_by' not in request.data:
            request.data['created_by'] = request.user.id

        return super(CreatorUpdaterMixin, self).create(request, args, kwargs)

class GetQuerysetMixin(object):

    def get_queryset(self, *args, **kwargs):
        queryset = super(GetQuerysetMixin, self).get_queryset()
        print(self.request.user)
        return queryset.filter(created_by=self.request.user)