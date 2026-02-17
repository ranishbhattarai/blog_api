from rest_framework import permissions

class IsAdminOrAuthor(permissions.BasePermission):
    """
    Custom permission to only allow authors of a blog or admins to edit it.
    """

    def has_permission(self, request, view):
        # Admins can do anything
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for published blogs
        if request.method in permissions.SAFE_METHODS:
            if obj.is_published or request.user.is_admin or (request.user.is_author and obj.author == request.user):
                return True
            return False
        
        # Write permissions only for admins or the author
        if request.user.is_admin:
            return True
        if request.user.is_author and obj.author == request.user:
            return True
        return False
