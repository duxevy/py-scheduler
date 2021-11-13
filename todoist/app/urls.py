from django.urls import path
from .views import *

app_name = 'app'
urlpatterns = [
    path('notes/', NoteView.as_view()),
    path('note/<int:note_id>/', NoteDetailView.as_view()),
    path('note/editor/<int:note_id>/', NoteEditorView.as_view()),
    path('note/delete/<int:note_id>/', NoteDeleteView.as_view()),
    path('note/add/', NoteAddView.as_view()),
]
