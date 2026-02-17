from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Blog
from .serializers import BlogSerializer
from .permissions import IsAdminOrAuthorOrReadOnly

# Create your views here.
# this file defines the BlogViewSet, which is a viewset for handling CRUD operations on the Blog model. It includes custom actions for publishing a blog and retrieving the authenticated user's blogs. The viewset uses the BlogSerializer for serialization and the IsAdminOrAuthorOrReadOnly permission class to control access based on user roles.
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAdminOrAuthorOrReadOnly]
# this method overrides the default queryset to return different sets of blogs based on the user's authentication status and role. Admins can see all blogs, authors can see their own blogs and published blogs, while unauthenticated users can only see published blogs.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_admin:
                return Blog.objects.all()
            if user.is_author:
                return Blog.objects.filter(author=user) | Blog.objects.filter(is_published=True)
        return Blog.objects.filter(is_published=True)
#this method overrides the default create behavior to automatically set the author of a new blog post to the currently authenticated user when a blog is created through the API.
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
#this custom action allows an authenticated admin or the author of a blog to publish it by setting the is_published field to True. It checks the user's permissions before allowing the action and returns an appropriate response.
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        blog = self.get_object()
        if request.user.is_admin or (request.user.is_author and blog.author == request.user):
            blog.is_published = True
            blog.save()
            return Response({'status': 'blog published'})
        return Response({'status': 'permission denied'}, status=403)
    # this custom action allows an authenticated author to retrieve a list of their own blogs. It checks if the user has the author role and returns the serialized data of their blogs, or a permission denied response if they do not have access.
    @action(detail=False, methods=['get'])
    def my_blogs(self, request):
        if request.user.is_author:
            blogs = Blog.objects.filter(author=request.user)
            serializer = self.get_serializer(blogs, many=True)
            return Response(serializer.data)
        return Response({'detail': 'You do not have permission to view your blogs.'}, status=403)