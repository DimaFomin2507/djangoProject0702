from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProfilesOwnerSerializer, CreateUserSerializer
from profiles.models import Profiles, ProfilesRole, User
from django.db import transaction


class CreateProfilesView(CreateAPIView):
    serializer_class = ProfilesOwnerSerializer
    queryset = Profiles.objects.all()

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            admin_ids = serializer.validated_data['admins']
            member_ids = serializer.validated_data['members']
            del serializer.validated_data['admins']
            del serializer.validated_data['members']
            profiles = serializer.save()
            ProfilesRole(
                profiles=profiles,
                user=request.user,

            ).save()
            for admin_id in admin_ids:
                try:
                    user = User.objects.get(id=admin_id)
                except User.DoesNotExist:
                    return Response(data=
                                    {"error": f"user {admin_id} does not exist"},
                                    status=status.HTTP_400_BAD_REQUEST)
                ProfilesRole(
                    profiles=profiles,
                    user=user,

                ).save()
            for member_id in member_ids:
                try:
                    user = User.objects.get(id=member_id)
                except User.DoesNotExist:
                    return Response(data=
                                    {"error": f"user {member_id} does not exist"},
                                    status=status.HTTP_400_BAD_REQUEST)
                ProfilesRole(
                    profile=profiles,
                    user=user,

                ).save()
            return Response(status=status.HTTP_201_CREATED)


class SignUpView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = []

