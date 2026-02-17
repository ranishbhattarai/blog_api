from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Blog
from .serializers import BlogSerializer
from .permissions import IsAdminOrAuthorOrReadOnly

# Create your views here.

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAdminOrAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        blog = self.get_object()
        if request.user.is_admin or (request.user.is_author and blog.author == request.user):
            blog.is_published = True
            blog.save()
            return Response({'status': 'blog published'})
        return Response({'status': 'permission denied'}, status=403)
    
    @action(detail=True, methods=['post'])
    def my_blogs(self, request):
       if request.user.is_author:
              blogs = Blog.objects.filter(author=request.user)
              serializer = self.get_serializer(blogs, many=True)
              return Response(serializer.data)
       return Response({'detail': 'You do not have permission to view your blogs.'}, status=403)