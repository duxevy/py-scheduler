from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


def index(request):
    return render(request, 'app/index.html', {'title': 'Главная страница', 'user': request.user})


class NoteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # Забираем из базы все опубликованные записи (QuerySet)
        notes = Note.objects.filter(public=True).order_by('-date_add')
        # Работа сериализатора
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)


class NoteDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, note_id):
        # Берем одну опубликованную запись
        note = Note.objects.filter(pk=note_id, public=True).first()
        # Исключение несуществующей записи
        if not note:
            raise NotFound(f'Записи с id={note_id} не существует')
        # Работа сериализатора
        serializer = NoteDetailSerializer(note)
        return Response(serializer.data)


class NoteAddView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Метод создания новой записи
        # Берем запрос и передаем его сериализатору
        new_note = NoteEditorSerializer(data=request.data)
        # Валидатор
        if new_note.is_valid():
            # Сохранение в базу новой записи. Автор - авторизованный пользователь
            new_note.save(author=request.user)
            return Response(new_note.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteEditorView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, note_id):
        # Метод редактирования
        # Поиск редактируемой записи
        note = Note.objects.filter(pk=note_id, author=request.user).first()
        if not note:
            # Отработка исключений
            raise NotFound(f'Записи с id={note_id} для пользователя {request.user.username} не существует')
        #
        new_note = NoteEditorSerializer(note, data=request.data, partial=True)
        # Валидатор
        if new_note.is_valid():
            new_note.save()
            return Response(new_note.data, status=status.HTTP_200_OK)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, note_id):
        # Метод для удаления записи
        note = Note.objects.filter(pk=note_id).first()
        # Исключение несуществующей записи
        if not note:
            raise NotFound(f'Записи с id={note_id} не существует')

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
