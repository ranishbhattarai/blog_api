from rest_framework import permissions

class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a blog or admins to edit it.
    """

#this permission class allows anyone to read published blogs, but only authenticated users with the role of admin or author can create, update, or delete blogs. Additionally, authors can only edit their own blogs, while admins can edit any blog.
    def has_permission(self, request, view):
        # Allow read-only requests for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write requests require authenticated admin or author
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_admin or request.user.is_author)
        )
#this method checks if the user has permission to perform the requested action on a specific blog object. It allows read permissions for published blogs, but write permissions are only granted to admins or the author of the blog.
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
