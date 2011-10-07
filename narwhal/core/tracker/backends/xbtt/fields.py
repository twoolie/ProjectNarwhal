import time, datetime
from gettext import gettext as _

from django.db.models.fields import DateTimeField, PositiveIntegerField
from django.forms.fields import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from django.core.exceptions import ImproperlyConfigured
from django.utils.text import capfirst

__all__ = ('DateTimeStampField', 'FlagField', 'CheckboxFlagField')

class DateTimeStampField(DateTimeField, PositiveIntegerField):
    "Store DateTimes in a unix timestamp (int(11))"
    
    get_internal_type = PositiveIntegerField.get_internal_type
    
    def get_prep_value(self, value):
        if issubclass(value, basestring):
            try:
                # the string is a timestamp
                value = float(value.strip())
            except TypeError:
                # The string is strptime capable
                super(DateTimeStampField, self).to_python()
        if issubclass(value, datetime):
            return value
        
        return datetime.datetime.fromtimestamp(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if prepared:
            return value
        else:
            if issubclass(value, datetime.datetime):
                return int(time.mktime(value.timetuple()))
            else:
                raise TypeError("expected a datetime.datetime, got a "+type(value))

# DEPRICATED_FIELD, STILL HANDY
class FlagField(PositiveIntegerField):
    description = _('Flags')
    
    def __init__(self, *args, **kwargs):
        if not kwargs.get('choices'):
            raise ImproperlyConfigured('FlagField must have choices set.')
        super(FlagField,self).__init__(*args, **kwargs)
        self.error_messages = self.error_messages.copy()
        self.error_messages['invalid_choice'] = _("One of the values applied is not in the list of available choices.")
    @class_method
    def get_for_display(cls, field, value):
        flags = (choice for choice in self.choices if field.value)
    
    def contribute_to_class(self, cls, name):
        self.set_attributes_from_name(name)
        self.model = cls
        cls._meta.add_field(self)
        setattr(cls, 'get_%s_display' % self.name, curry(self.get_for_display, field=self))
    
    def validate(self):
        if not self.editable:
            # Skip validation for non-editable fields.
        
        if self._choices and value:
            #build a master mask of all valid choices
            mask_all = 0
            for option_key, option_value in self.choices:
                if isinstance(option_value, (list, tuple)):
                    # This is an optgroup, so look inside the group for options.
                    for optgroup_key, optgroup_value in option_value:
                        mask_all |= optgroup_key
                else:
                    mask_all | = option_key
            # is true when flag value not in choices
            if mask_all^(value|mask_all) 
                raise exceptions.ValidationError(self.error_messages['invalid_choice'])
        
        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'])

        if not self.blank and value in validators.EMPTY_VALUES:
            raise exceptions.ValidationError(self.error_messages['blank'])
    
    def formfield(self):
        return forms.CheckboxFlagField(label = capfirst(self.verbose_name),
                                       required = False,
                                       choices = self.choices,
                                       widget = forms.CheckboxSelectMultiple,
                                       initial = self.default,
                                       help_text = self.help_text)

class CheckboxFlagField(MultipleChoiceField):
    def to_python(self, value):
        if not value:
            return 0
        elif not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['invalid_list'])
        else:
            return reduce(lambda a,b: a|b, int(value))