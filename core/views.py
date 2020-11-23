from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

import htmlgenerator as hg
from bread import layout
from bread.forms.forms import generate_form
from bread.utils.urlgenerator import registerurl

from .models import Category, JuristicPerson, Term


def single_item_fieldset(related_field, fieldname, queryset=None):
    return layout.form.FormSetField(
        related_field,
        layout.form.FormField(fieldname),
        formsetinitial={"queryset": queryset},
        can_delete=False,
        max_num=1,
        extra=1,
    )


@registerurl
def generalsettings(request):
    instance = JuristicPerson.objects.get(id=1)  # must exists due to migration

    formlayout = layout.BaseElement(
        layout.grid.Grid(
            layout.grid.Row(layout.grid.Col(layout.form.FormField("type"))),
            layout.grid.Row(layout.grid.Col(layout.form.FormField("name"))),
            layout.grid.Row(layout.grid.Col(layout.form.FormField("name_addition"))),
        ),
        layout.form.FormSetField(
            "core_postal_list",
            layout.grid.Grid(
                layout.grid.Row(layout.grid.Col(layout.form.FormField("address"))),
                layout.grid.Row(
                    layout.grid.Col(layout.form.FormField("supplemental_address"))
                ),
                layout.grid.Row(
                    layout.grid.Col(
                        layout.form.FormField("postcode"), breakpoint="lg", width=2
                    ),
                    layout.grid.Col(
                        layout.form.FormField("city"), breakpoint="lg", width=3
                    ),
                    layout.grid.Col(
                        layout.form.FormField("country"), breakpoint="lg", width=3
                    ),
                ),
            ),
            can_delete=False,
            max_num=1,
            extra=1,
        ),
        layout.grid.Grid(
            layout.grid.Row(
                layout.grid.Col(single_item_fieldset("core_phone_list", "number")),
                layout.grid.Col(single_item_fieldset("core_fax_list", "number")),
            ),
            layout.grid.Row(
                layout.grid.Col(
                    single_item_fieldset(
                        "core_email_list",
                        "email",
                    )
                ),
                layout.grid.Col(single_item_fieldset("core_web_list", "url")),
            ),
        ),
        layout.form.SubmitButton(_("Save")),
    )

    form = generate_form(request, JuristicPerson, formlayout, instance)

    if request.method == "POST":
        if form.is_valid():
            form.save()

    pagelayout = hg.BaseElement(
        hg.H1(_("General")),
        hg.H2(_("General information")),
        layout.form.Form(form, formlayout),
    )

    return render(request, "bread/layout.html", {"layout": pagelayout})


@registerurl
def appearancesettings(request):
    pagelayout = hg.BaseElement(hg.H2(_("Appearance")))
    return render(request, "bread/layout.html", {"layout": pagelayout})


@registerurl
def personssettings(request):
    from bread.admin import site

    pagelayout = hg.BaseElement(
        hg.H2(_("Persons")),
        # address type
        layout.datatable.DataTable.from_queryset(
            Term.objects.filter(category__slug="addresstype"),
            fields=["term"],
            title=_("Address types"),
            addurl=site.get_default_admin(Term).reverse(
                "add",
                query_arguments={
                    "category": Category.objects.get(slug="addresstype").id,
                    "next": reverse(personssettings),
                },
            ),
        ),
        # address origin
        layout.datatable.DataTable.from_queryset(
            Term.objects.filter(category__slug="addressorigin"),
            fields=["term"],
            title=_("Address origins"),
            addurl=site.get_default_admin(Term).reverse(
                "add",
                query_arguments={
                    "category": Category.objects.get(slug="addressorigin").id,
                    "next": reverse(personssettings),
                },
            ),
        ),
        # salutation
        layout.datatable.DataTable.from_queryset(
            Term.objects.filter(category__slug="salutation"),
            fields=["term"],
            title=_("Salutation"),
            addurl=site.get_default_admin(Term).reverse(
                "add",
                query_arguments={
                    "category": Category.objects.get(slug="salutation").id,
                    "next": reverse(personssettings),
                },
            ),
        ),
    )
    return render(request, "bread/layout.html", {"layout": pagelayout})


@registerurl
def relationshipssettings(request):
    pagelayout = hg.BaseElement(hg.H2(_("Relationships")))
    return render(request, "bread/layout.html", {"layout": pagelayout})


@registerurl
def apikeyssettings(request):
    pagelayout = hg.BaseElement(hg.H2(_("APK Keys")))
    return render(request, "bread/layout.html", {"layout": pagelayout})