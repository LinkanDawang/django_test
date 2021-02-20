from rest_framework.viewsets import GenericViewSet


class MyGenericViewSet(GenericViewSet):

    def get_serializer_class(self):
        """
        ...
        """
        if isinstance(self.serializer_class, dict):
            serializer_class = self.serializer_class.get(self.action)
            if not serializer_class:
                serializer_class = self.serializer_class.get("default")
        else:
            serializer_class = self.serializer_class
        assert serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )
        return serializer_class

