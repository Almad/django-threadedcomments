from django import forms
from django.contrib.comments.forms import CommentForm
from django.conf import settings
from django.utils.hashcompat import sha_constructor

from threadedcomments.models import ThreadedComment

class ThreadedCommentForm(CommentForm):
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)
    title = forms.CharField(required=False)

    def __init__(self, target_object, parent=None, data=None, initial=None):
        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({'parent': self.parent})
        super(ThreadedCommentForm, self).__init__(target_object, data=data,
            initial=initial)

    def get_comment_model(self):
        return ThreadedComment

    def get_comment_create_data(self):
        d = super(ThreadedCommentForm, self).get_comment_create_data()
        d['parent_id'] = self.cleaned_data['parent']
        d['title'] = self.cleaned_data['title']
        return d

