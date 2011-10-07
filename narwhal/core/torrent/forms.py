# -*- coding: utf-8 -*-

import pickle
from hashlib import sha1

from django import forms
from django.utils.translation import ugettext_lazy as _

from bencode import bencode, bdecode, BTFailure
from sorl.thumbnail.fields import ImageFormField

from models import Category, Torrent

class CategoryChoice(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        self.begin_from_level = kwargs.pop('begin_from_level', 0)
        super(CategoryChoice, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return obj.tree_represent(space='-', begin_from_level=self.begin_from_level)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category

    parent = CategoryChoice(queryset=Category.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(level__in=[0,1])

class TorrentForm(forms.ModelForm):
    class Meta:
        model = Torrent

    category = CategoryChoice(queryset=Category.objects.all(), empty_label=None, begin_from_level=1)
    torrent = forms.FileField()
    image = ImageFormField(label=_('image'), required=False)

    def __init__(self, *args, **kwargs):
        super(TorrentForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.exclude(level=0)

    def clean_torrent(self):
        if not self.cleaned_data['torrent'].multiple_chunks():
            try:
                self.decoded = bdecode(self.cleaned_data['torrent'].read())
                return self.cleaned_data['torrent']
            except BTFailure:
                raise forms.ValidationError(_(u'Not a valid torrent file.'))
        else:
            raise forms.ValidationError(_('File too big for torrent file'))

    def save(self, commit=True):
        self.instance.data = self.decoded
        self.instance.info_hash = sha1(bencode(self.decoded['info'])).hexdigest()
        del self.instance.decoded['info']['pieces'] # get rid of piece data
        fail_message = 'created' if self.instance.pk is None else 'changed'
        return forms.save_instance(self, self.instance, self._meta.fields, fail_message, commit)
