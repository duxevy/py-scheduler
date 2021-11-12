from django.urls import path
from .views import *

app_name = 'app'
urlpatterns = [
    path('notes/', NoteView.as_view()),
    path('notes/<int:note_id>/', NoteDetailView.as_view()),
    path('notes/add/', NoteEditorView.as_view()),
    path('notes/delete/<int:note_id>/', NoteDeleteView.as_view()),
]
