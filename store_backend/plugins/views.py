
from rest_framework import generics, permissions
from rest_framework.reverse import reverse

from collectionjson import services

from .models import Plugin, PluginFilter, PluginParameter
from .serializers import PluginSerializer,  PluginParameterSerializer
from .permissions import IsOwnerOrChrisOrReadOnly


class PluginList(generics.ListAPIView):
    """
    A view for the collection of plugins.
    """
    serializer_class = PluginSerializer
    queryset = Plugin.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Overriden to append document-level link relations.
        """
        response = super(PluginList, self).list(request, *args, **kwargs)
        user = self.request.user
        # append document-level link relations
        if user.is_authenticated:
            links = {'user_plugins': reverse('user-plugin-list', request=request),
                     'user': reverse('user-detail', request=request,
                                     kwargs={"pk": user.id})}
            response = services.append_collection_links(response, links)
        # append query list
        query_list = [reverse('plugin-list-query-search', request=request)]
        return services.append_collection_querylist(response, query_list)


class UserPluginList(generics.ListCreateAPIView):
    """
    A view for the collection of plugins.
    """
    serializer_class = PluginSerializer
    queryset = Plugin.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Overriden to return a custom queryset that is only comprised by the plugins
        owned by the currently authenticated user.
        """
        user = self.request.user
        # if the user is chris then return all the plugins in the system
        if (user.username == 'chris'):
            return Plugin.objects.all()
        return Plugin.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        Overriden to associate an owner with the plugin before first
        saving to the DB.
        """
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Overriden to insert the username as a prefix of the submitted plugin name.
        """
        # modify plugin's name to always include username as prefix
        name = request.data['name']
        if not name.startswith(request.user.username + '/'):
            request.data['name'] = request.user.username +  '/' + name
        return super(UserPluginList, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Overriden to append document-level link relations and a collection+json template
        to the response.
        """
        response = super(UserPluginList, self).list(request, *args, **kwargs)
        user = self.request.user
        # append document-level link relations
        links = {'plugins': reverse('plugin-list', request=request),
                 'user': reverse('user-detail', request=request, kwargs={"pk": user.id})}
        response = services.append_collection_links(response, links)
        # append write template
        template_data = {'name': '', 'dock_image': '', 'public_repo': '',
                         'descriptor_file': ''}
        return services.append_collection_template(response, template_data)


class PluginListQuerySearch(generics.ListAPIView):
    """
    A view for the collection of plugins resulting from a query search.
    """
    serializer_class = PluginSerializer
    queryset = Plugin.objects.all()
    filter_class = PluginFilter
        

class PluginDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    A plugin view.
    """
    serializer_class = PluginSerializer
    queryset = Plugin.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrChrisOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        """
        Overriden to append a collection+json template.
        """
        response = super(PluginDetail, self).retrieve(request, *args, **kwargs)
        template_data = {'name': '', 'dock_image': '', 'public_repo': '',
                         'descriptor_file': ''}
        return services.append_collection_template(response, template_data)


class PluginParameterList(generics.ListAPIView):
    """
    A view for the collection of plugin parameters.
    """
    queryset = Plugin.objects.all()
    serializer_class = PluginParameterSerializer

    def list(self, request, *args, **kwargs):
        """
        Overriden to return the list of parameters for the queried plugin.
        """
        queryset = self.get_plugin_parameters_queryset()
        return services.get_list_response(self, queryset)

    def get_plugin_parameters_queryset(self):
        """
        Custom method to get the actual plugin parameters' queryset.
        """
        plugin = self.get_object()
        return self.filter_queryset(plugin.parameters.all())

    
class PluginParameterDetail(generics.RetrieveAPIView):
    """
    A plugin parameter view.
    """
    queryset = PluginParameter.objects.all()
    serializer_class = PluginParameterSerializer