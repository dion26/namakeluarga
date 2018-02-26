from django.db import models
from django.db.models import Count, Q, F
from django.db.models.signals import pre_save, post_save

from .utils import unique_slug_generator

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),)

# Create your models here.
class Person(models.Model):

    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=30)
    gender          = models.CharField(max_length=1, choices=GENDER)
    father          = models.ForeignKey('Person', on_delete=models.SET_NULL,
                      null=True, blank=True, limit_choices_to={'gender': 'M'},
                      related_name='children_of_father')
    mother          = models.ForeignKey('Person', on_delete=models.SET_NULL,
                      null=True, blank=True, limit_choices_to={'gender': 'F'},
                      related_name='children_of_mother')
    #relation_with   =
    date_birth      = models.DateField()
    slug            = models.SlugField(null=True, blank=True)

    @property
    def title(self):
        name = self.first_name + self.last_name
        return name

    @property
    def name(self):
        name = self.first_name + ' ' + self.last_name
        return name

    @property
    def pasangan(self):
        pa = []
        if self.gender == 'M':
            if self.children_of_father.all().exists():
                cil = self.children_of_father.all()
                for obj in Person.objects.all():
                    if (list(obj.children_of_mother.all()) == list(cil)):
                        pa.append(obj.name)

        elif self.gender == 'F':

            if self.children_of_mother.all().exists():
                cil = self.children_of_mother.all()
                for obj in Person.objects.all():
                    if (list(obj.children_of_father.all()) == list(cil)):
                        pa.append(obj.name)
        else:
            pa.append('-')

        return pa

    @property
    def anak(self):
        an = []
        if self.gender == 'M':
            try:
                for obj in self.children_of_father.all():
                    an.append(obj.name)
            except:
                pass
        if self.gender == 'F':
            try:
                for obj in self.children_of_mother.all():
                    an.append(obj.name)
            except:
                pass
        return an


    @property
    def older_brother(self):

        older_brother = []
        for ol in Person.objects.all():
            if (ol.father == self.father and ol.mother == self.mother and
                ol.mother != None and ol.gender == 'M'):
                if ol.date_birth < self.date_birth:
                    older_brother.append(ol.name)
        if older_brother:
            return older_brother
        else:
            return '-'


    @property
    def younger_brother(self):

        younger_brother = []
        for ol in Person.objects.all():
            if (ol.father == self.father and ol.mother == self.mother and
                ol.mother != None and ol.gender == 'M'):
                if ol.date_birth > self.date_birth:
                    younger_brother.append(ol.name)
        if younger_brother:
            return younger_brother
        else:
            return '-'

    @property
    def younger_sister(self):

        younger_sister = []
        for ol in Person.objects.all():
            if (ol.father == self.father and ol.mother == self.mother and
                ol.mother != None and ol.gender == 'F'):
                if ol.date_birth > self.date_birth:
                    younger_sister.append(ol.name)
        if younger_sister:
            return younger_sister
        else:
            return '-'

    @property
    def older_sister(self):

        older_sister = []
        for ol in Person.objects.all():
            if (ol.father == self.father and ol.mother == self.mother and
                ol.mother != None and ol.gender == 'F'):
                if ol.date_birth < self.date_birth:
                    older_sister.append(ol.name)
        if older_sister:
            return older_sister
        else:
            return '-'

    @property
    def m_grand_father(self):
        try:
            grand_father = self.father.father.name
            return grand_father
        except AttributeError:
            return '-'

    @property
    def m_grand_mother(self):
        try:
            grand_mother = self.father.mother.name
            return grand_mother
        except AttributeError:
            return '-'

    @property
    def f_grand_father(self):
        try:
            grand_father = self.mother.father.name
            return grand_father
        except AttributeError:
            return '-'

    @property
    def f_grand_mother(self):
        try:
            grand_mother = self.mother.mother.name
            return grand_mother
        except AttributeError:
            return '-'
    @property
    def m_older_uncle(self):
        try:
            gp = self.father.father
            gm = self.father.mother
            gp.name
            gm.name
        except AttributeError:
            return '-'
        else:
            uncle = []

            for obj in Person.objects.all():
                if (obj.father == gp and obj.mother == gm and
                    gm != None and obj.gender == 'M' and obj != self.father):
                    if obj.date_birth < self.father.date_birth:
                        uncle.append(obj.name)

                try: gpp = obj.father.father # suami dari bibi muda
                except:
                    pass
                else:
                    if (gpp == gp and obj.mother.date_birth < self.father.date_birth
                        and obj.father != self.father and obj.father.name not in uncle):
                        uncle.append(obj.father.name)


            if uncle:
                return uncle
            else:
                return '-'

    @property
    def m_younger_uncle(self):
        try:
            gp = self.father.father
            gm = self.father.mother
            gp.name
            gm.name
        except AttributeError:
            return '-'
        else:
            uncle = []

            for obj in Person.objects.all():
                if (obj.father == gp and obj.mother == gm and
                    gm != None and obj.gender == 'M' and obj != self.father):
                    if obj.date_birth > self.father.date_birth:
                        uncle.append(obj.name)

                try: gpp = obj.father.father # suami dari bibi muda
                except:
                    pass
                else:
                    if (gpp == gp and obj.mother.date_birth > self.father.date_birth
                        and obj.father != self.father and obj.father.name not in uncle):
                        uncle.append(obj.father.name)

            if uncle:
                return uncle
            else:
                return '-'

    @property
    def f_older_uncle(self):
        try:
            gp = self.mother.father
            gm = self.mother.mother
            gp.name
            gm.name
        except AttributeError:
            return '-'
        else:

            uncle = []

            for obj in Person.objects.all():
                if (obj.father == gp and obj.mother == gm and
                    gm != None and obj.gender == 'M' and obj != self.father):
                    if obj.date_birth < self.mother.date_birth:
                        uncle.append(obj.name)

                try: gpp = obj.father.father # suami dari bibi muda
                except:
                    pass
                else:
                    if (gpp == gp and obj.mother.date_birth < self.mother.date_birth
                        and obj.father.name not in uncle):
                        uncle.append(obj.father.name)


            if uncle:
                return uncle
            else:
                return '-'

    @property
    def f_younger_uncle(self):
        try:
            gp = self.mother.father
            gm = self.mother.mother
            gp.name
            gm.name
        except AttributeError:
            return '-'
        else:

            uncle = []

            for obj in Person.objects.all():
                if (obj.father == gp and obj.mother == gm and
                    gm != None and obj.gender == 'M' and obj != self.father):
                    if obj.date_birth > self.mother.date_birth:
                        uncle.append(obj.name)

                try: gpp = obj.father.father # suami dari bibi muda
                except:
                    pass
                else:
                    if (gpp == gp and obj.mother.date_birth > self.mother.date_birth
                        and obj.father.name not in uncle):
                        uncle.append(obj.father.name)

            if uncle:
                return uncle
            else:
                return '-'

    @property
    def m_older_auntie(self):

        try:
            gp = self.father.father
            gm = self.father.mother
            gp.name
            gm.name
        except AttributeError:
            return '-'
        else:

            auntie = []

            for obj in Person.objects.all():
                if (obj.father == gp and obj.mother == gm and
                    gm != None and obj.gender == 'F'):
                    if obj.date_birth < self.father.date_birth:
                        auntie.append(obj.name)

                try: gpp = obj.father.father # istri dari om muda
                except:
                    pass
                else:
                    if (gpp == gp and obj.father.date_birth < self.father.date_birth
                        and obj.mother != self.mother and obj.mother.name not in auntie):
                        auntie.append(obj.mother.name)

            if auntie:
                return auntie
            else:
                return '-'

    @property
    def m_younger_auntie(self):

        try:
            gp = self.father.father
            gm = self.father.mother
            gp.name
            gm.name
        except AttributeError:
            return '-'
        else:

            auntie = []

            for obj in Person.objects.all():
                if (obj.father == gp and obj.mother == gm and
                    gm != None and obj.gender == 'F'):
                    if obj.date_birth > self.father.date_birth:
                        auntie.append(obj.name)

                try: gpp = obj.father.father # istri dari om muda
                except:
                    pass
                else:
                    if (gpp == gp and obj.father.date_birth > self.father.date_birth
                        and obj.mother != self.mother and obj.mother.name not in auntie):
                        auntie.append(obj.mother.name)

            if auntie:
                return auntie
            else:
                return '-'

    @property
    def f_older_auntie(self):

        try:
            gp = self.mother.father
            gm = self.mother.mother
            gp.name
            gm.name
        except AttributeError:
            return '-'
        else:

            auntie = []

            for obj in Person.objects.all():
                if (obj.father == gp and obj.mother == gm and
                    gm != None and obj.gender == 'F' and obj != self.mother):
                    if obj.date_birth < self.mother.date_birth:
                        auntie.append(obj.name)

                try: gpp = obj.father.father
                except:
                    pass
                else:
                    if (gpp == gp and obj.father.date_birth < self.mother.date_birth
                        and obj.mother != self.mother and obj.mother.name not in auntie):
                        auntie.append(obj.mother.name)

            if auntie:
                return auntie
            else:
                return '-'

    @property
    def f_younger_auntie(self):

        try:
            gp = self.mother.father
            gm = self.mother.mother
            gp.name
            gm.name
        except AttributeError:
            return '-'
        else:

            auntie = []

            for obj in Person.objects.all():
                if (obj.father == gp and obj.mother == gm and
                    gm != None and obj.gender == 'F' and obj != self.mother):
                    if obj.date_birth > self.mother.date_birth:
                        auntie.append(obj.name)

                    try: gpp = obj.father.father # istri dari om muda
                    except:
                        pass
                    else:
                        if (gpp == gp and obj.father.date_birth > self.mother.date_birth
                            and obj.mother != self.mother and obj.mother.name not in auntie):
                            auntie.append(obj.mother.name)

            if auntie:
                return auntie
            else:
                return '-'


    def __str__(self):
        name = self.first_name + ' ' + self.last_name
        return name

# for slug generator

def pr_pre_save_receiver(sender, instance, *args, **kwargs):
    print('saving...')
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

def pr_post_save_receiver(sender, instance, *args, **kwargs):
    print('saved')

pre_save.connect(pr_pre_save_receiver, sender=Person)
post_save.connect(pr_post_save_receiver, sender=Person)
