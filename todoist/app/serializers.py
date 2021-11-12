# DRF imports
from rest_framework import serializers

# Local imports
from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    # Имя автора вместо id
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Note
        fields = '__all__'


class NoteDetailSerializer(serializers.ModelSerializer):
    # Имя автора вместо id
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Note
        exclude = ('public',)


class NoteEditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ['date_add', 'author', ]
