from bread import layout as layout
from bread.layout import register as registerlayout
from bread.utils.urls import reverse, reverse_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Category, RelationshipType, Term


def single_item_fieldset(related_field, fieldname, queryset=None):
    """Helper function to show only a single item of a (foreign-key) related item list"""
    return layout.form.FormSetField(
        related_field,
        layout.form.FormField(fieldname),
        formsetinitial={"queryset": queryset},
        can_delete=False,
        max_num=1,
        extra=1,
    )


def generate_term_datatable(title, category_slug):
    """Helper function to display a table for all terms of a certain term"""
    return layout.datatable.DataTable.from_queryset(
        Term.objects.filter(category__slug=category_slug),
        fields=["term"],
        title=title,
        addurl=reverse_model(
            Term,
            "add",
            query={
                "category": Category.objects.get(slug=category_slug).id,
                "next": reverse("basxconnect.core.views.personsettings"),
            },
        ),
        backurl=reverse("basxconnect.core.views.personsettings"),
    )


@registerlayout()
def generalsettings():
    return layout.BaseElement(
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


@registerlayout()
def editnaturalperson_head():
    R = layout.grid.Row
    C = layout.grid.Col
    active_toggle = layout.toggle.Toggle(None, _("Inactive"), _("Active"))
    active_toggle.input.attributes["id"] = "person_active_toggle"
    active_toggle.input.attributes["hx_trigger"] = "change"
    active_toggle.input.attributes["hx_post"] = layout.F(
        lambda c, e: reverse_lazy("core.person.togglestatus", args=[c["object"].pk])
    )
    active_toggle.input.attributes["checked"] = layout.F(
        lambda c, e: c["object"].active
    )
    active_toggle.label.insert(0, _("Person status"))
    active_toggle.label.attributes["_for"] = active_toggle.input.attributes["id"]

    return layout.grid.Grid(
        R(C(layout.H3(layout.I(layout.ObjectLabel())))),
        R(C(active_toggle)),
    )


@registerlayout()
def editnaturalperson_form():
    R = layout.grid.Row
    C = layout.grid.Col
    F = layout.form.FormField
    # fix: alignment of tab content and tab should be on global grid I think
    return layout.tabs.Tabs(
        (
            _("Base data"),
            layout.BaseElement(
                layout.grid.Grid(
                    R(C(layout.H4(_("General Information")))),
                    R(
                        C(
                            R(
                                C(F("first_name")),
                                C(F("last_name")),
                            ),
                            R(
                                C(F("name")),
                                C(F("preferred_language")),
                            ),
                            R(
                                C(F("date_of_birth")),
                                C(F("profession")),
                            ),
                        ),
                        C(
                            R(
                                C(F("salutation", widgetattributes={"width": "18rem"})),
                                C(F("title")),
                            ),
                            R(
                                C(),
                                C(F("salutation_letter")),
                            ),
                        ),
                    ),
                ),
                layout.DIV(_class="section-separator-bottom"),
                layout.grid.Grid(
                    R(
                        C(
                            R(C(layout.H4(_("Address")))),
                            layout.form.FormSetField(
                                "core_postal_list",
                                R(C(F("address"))),
                                R(
                                    C(
                                        F(
                                            "supplemental_address",
                                            widgetattributes={"rows": 1},
                                        )
                                    )
                                ),
                                R(
                                    C(F("postcode"), breakpoint="lg", width=4),
                                    C(F("city"), breakpoint="lg", width=12),
                                ),
                                R(
                                    C(F("country")),
                                    C(),
                                ),
                                can_delete=False,
                                max_num=1,
                                extra=1,
                            ),
                            _class="section-separator-right",
                        ),
                        C(
                            R(
                                C(layout.H4(_("Relationships"))),
                                _class="section-separator-bottom",
                            ),
                            R(C(layout.H4(_("Communication Channels")))),
                            R(C(layout.H5(_("Phone")))),
                            layout.form.FormSetField(
                                "core_phone_list",
                                R(
                                    C(F("type"), breakpoint="lg", width=4),
                                    C(F("number"), breakpoint="lg", width=12),
                                ),
                                can_delete=False,
                                extra=0,
                            ),
                            R(C(layout.H5(_("Email")))),
                            layout.form.FormSetField(
                                "core_email_list",
                                R(C(F("email"))),
                                can_delete=False,
                                extra=0,
                            ),
                        ),
                    ),
                ),
            ),
        ),
        container=True,
    )


@registerlayout()
def relationshipssettings():
    return layout.BaseElement(
        layout.H3(_("Relationships")),
        layout.datatable.DataTable.from_queryset(
            RelationshipType.objects.all(),
            fields=["name"],
            addurl=reverse_model(
                RelationshipType,
                "add",
                query={"next": reverse("basxconnect.core.views.relationshipssettings")},
            ),
            backurl=reverse("basxconnect.core.views.relationshipssettings"),
        ),
    )


@registerlayout()
def personsettings():
    dist = layout.DIV(style="margin-bottom: 2rem")
    return layout.BaseElement(
        layout.H3(_("Persons")),
        # address type
        generate_term_datatable(_("Address types"), "addresstype"),
        dist,
        generate_term_datatable(_("Address origins"), "addressorigin"),
        dist,
        generate_term_datatable(_("Title"), "title"),
        dist,
        generate_term_datatable(
            _("Correspondence Languages"), "correspondence_language"
        ),
        dist,
        generate_term_datatable(_("Communication Channels"), "communication_channels"),
        dist,
        generate_term_datatable(_("Legal Types"), "legaltype"),
        dist,
    )


@registerlayout()
def editpersonheader():
    return None
