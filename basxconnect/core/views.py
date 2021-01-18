import htmlgenerator as hg
from bread import layout, menu
from bread.forms.forms import generate_form
from bread.utils.urls import aslayout, reverse, reverse_model
from bread.views import EditView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from haystack.query import SearchQuerySet

from . import layouts
from .models import LegalPerson, NaturalPerson, Person, PersonAssociation

# ADD MODEL VIEWS AND REGISTER URLS -------------------------------------------


class NaturalPersonEditView(EditView):
    def layout(self, request):
        return layout.ObjectContext(
            self.object,
            layout.BaseElement(
                layouts.editperson_toolbar(),
                layouts.editperson_head(),
                layout.form.Form.wrap_with_form(
                    layout.C("form"),
                    layouts.editnaturalperson_form(),
                ),
            ),
        )


class LegalPersonEditView(EditView):
    def layout(self, request):
        return layout.ObjectContext(
            self.object,
            layout.BaseElement(
                layouts.editperson_toolbar(),
                layouts.editperson_head(),
                layout.form.Form.wrap_with_form(
                    layout.C("form"),
                    layouts.editlegalperson_form(),
                ),
            ),
        )


class PersonAssociationEditView(EditView):
    def layout(self, request):
        return layout.ObjectContext(
            self.object,
            layout.BaseElement(
                layouts.editperson_toolbar(),
                layouts.editperson_head(),
                layout.form.Form.wrap_with_form(
                    layout.C("form"),
                    layouts.editpersonassociation_form(),
                ),
            ),
        )


# ADD SETTING VIEWS AND REGISTER URLS -------------------------------------------


@aslayout
def generalsettings(request):
    from basxconnect.core.layouts import generalsettings

    layoutobj = generalsettings()
    form = generate_form(
        request,
        LegalPerson,
        layoutobj,
        LegalPerson.objects.get(id=1),  # must exists due to migration
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()

    return lambda request: hg.BaseElement(
        hg.H3(_("General")),
        hg.H4(_("Information about our organization")),
        layout.form.Form(form, layoutobj),
    )


@csrf_exempt
def togglepersonstatus(request, pk: int):
    if request.method == "POST":
        person = get_object_or_404(Person, pk=pk)
        person.active = not person.active
        person.save()
    return HttpResponse(
        _("%s is %s") % (person, _("Active") if person.active else _("Inactive"))
    )


@aslayout
def personsettings(request):
    return lambda request: layouts.personsettings()


@aslayout
def relationshipssettings(request):
    return lambda request: layouts.relationshipssettings()


# MENU ENTRIES ---------------------------------------------------------------------

settingsgroup = menu.Group(_("Settings"), icon="settings")
persongroup = menu.Group(_("Persons"), icon="group")

menu.registeritem(
    menu.Item(menu.Link(reverse_model(Person, "browse"), _("Persons")), persongroup)
)

menu.registeritem(
    menu.Item(
        menu.Link(reverse("basxconnect.core.views.generalsettings"), _("General")),
        settingsgroup,
    )
)
menu.registeritem(
    menu.Item(
        menu.Link(reverse("basxconnect.core.views.personsettings"), _("Persons")),
        settingsgroup,
    )
)
menu.registeritem(
    menu.Item(
        menu.Link(
            reverse("basxconnect.core.views.relationshipssettings"),
            _("Relationships"),
        ),
        settingsgroup,
    )
)


# Search view
# simple person search view, for use with ajax calls
def searchperson(request):
    query = request.GET.get("query")
    if not query:
        return HttpResponse("")

    objects = [
        result.object
        for result in SearchQuerySet()
        .models(NaturalPerson, LegalPerson, PersonAssociation)
        .autocomplete(name_auto=query)
    ]
    if not objects:
        return HttpResponse(
            hg.DIV(
                _("No results"),
                _class="bx--tile",
                style="margin-bottom: 1rem;",
            ).render({})
        )

    return HttpResponse(
        hg.DIV(
            hg.UL(
                hg.Iterator(
                    objects,
                    hg.LI(
                        layout.ObjectContext.Binding(hg.DIV)(
                            layout.ObjectLabel(),
                            layout.ObjectContext.Binding(hg.DIV)(
                                hg.F(
                                    lambda c, e: mark_safe(
                                        e.object.core_postal_list.first()
                                        or _("No address")
                                    )
                                ),
                                style="font-size: small; padding-bottom: 1rem; padding-top: 0.5rem",
                            ),
                        ),
                        style="cursor: pointer; padding: 0.5rem;",
                        onclick=hg.BaseElement(
                            "document.location = '", layout.ObjectAction("edit"), "'"
                        ),
                        onmouseenter="this.style.backgroundColor = 'lightgray'",
                        onmouseleave="this.style.backgroundColor = 'initial'",
                    ),
                    layout.ObjectContext,
                ),
            ),
            _class="bx--tile",
            style="margin-bottom: 2rem;",
        ).render({})
    )
