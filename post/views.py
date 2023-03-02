from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Like, Unlike
from .serializers import UserSerializer, PostSerializer, LikeSerializer, UnlikeSerializer
class AllowPostAuthenticated(permissions.BasePermission):
    """
    Allows POST requests for unauthenticated users, but requires authentication
    for all other methods.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowPostAuthenticated]
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class LikePost(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        try:
            post_id = kwargs.get('post_id')
            post = Post.objects.get(id=post_id)
            like = Like.objects.create(user=request.user, post=post)
            print(like)
            return Response({'status': 'success'} , status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'failed', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UnlikePost(generics.CreateAPIView):
    queryset = Unlike.objects.all()
    serializer_class = UnlikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        try:
            post_id = kwargs.get('post_id')
            post = Post.objects.get(id=post_id)
            Unlike.objects.create(user=request.user, post=post)
            return Response({'status': 'success'})
        except Exception as e:
            return Response({'status': 'failed', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UnlikeDelete(generics.DestroyAPIView):
    serializer_class = UnlikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        unlike = Unlike.objects.filter(post__id=post_id, user=self.request.user)
        return unlike

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().first()
            if instance:
                self.perform_destroy(instance)
                return Response({'status': 'success'})
            else:
                return Response({'status': 'failed', 'message': 'You have not disliked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'failed', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LikeDelete(generics.DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        like = Like.objects.filter(post__id=post_id, user=self.request.user)
        return like

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().first()
            if instance:
                self.perform_destroy(instance)
                return Response({'status': 'success'})
            else:
                return Response({'status': 'failed', 'message': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'failed', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
