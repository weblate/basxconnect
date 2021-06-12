import htmlgenerator as hg
from bread import layout as layout
from bread.layout.components.datatable import DataTableColumn
from bread.menu import Link
from bread.utils.urls import reverse, reverse_model
from bread.views import BrowseView
from django import forms
from django.db.models import Q
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from basxconnect.core import models, settings


class PersonBrowseView(BrowseView):
    columns = [
        DataTableColumn(
            layout.fieldlabel(models.Person, "personnumber"),
            hg.DIV(
                hg.C("row.personnumber"),
                style=hg.If(hg.C("row.deleted"), "text-decoration:line-through"),
            ),
            "personnumber",
        ),
        "status",
        DataTableColumn(_("Category"), hg.C("row._type"), "_type"),
        "name",
        "primary_postal_address.address",
        "primary_postal_address.postcode",
        "primary_postal_address.city",
        "primary_postal_address.country",
        DataTableColumn(
            _("Email"),
            hg.C(
                "row.primary_email_address.asbutton",
            ),
            "primary_email_address__email",
            False,
        ),
    ]
    bulkactions = (
        Link(
            reverse_model(models.Person, "bulkdelete"),
            label=_("Delete"),
            icon="trash-can",
        ),
        Link(
            # make sure possible filter values of the browse view get
            # passed along to the excel-export view
            # TODO: maybe this behaviour should be better integrated in the bread views?
            hg.F(
                lambda c, e: reverse_model(models.Person, "excel")
                + "?"
                + c["request"].META["QUERY_STRING"]
            ),
            label=_("Excel"),
            icon="download",
        ),
    )
    searchurl = reverse(
        "basxconnect.core.views.person.person_search_views.searchperson"
    )
    rowclickaction = "read"

    class FilterForm(forms.Form):
        naturalperson = forms.BooleanField(required=False, label=_("Natural Person"))
        legalperson = forms.BooleanField(required=False, label=_("Legal Person"))
        personassociation = forms.BooleanField(
            required=False, label=_("Person Association")
        )
        naturalperson_subtypes = forms.ModelMultipleChoiceField(
            queryset=models.Term.objects.filter(category__slug="naturaltype"),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        legalperson_subtypes = forms.ModelMultipleChoiceField(
            queryset=models.Term.objects.filter(category__slug="legaltype"),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        personassociation_subtypes = forms.ModelMultipleChoiceField(
            queryset=models.Term.objects.filter(category__slug="associationtype"),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        categories = forms.ModelMultipleChoiceField(
            queryset=models.Term.objects.filter(category__slug="category"),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        preferred_language = forms.MultipleChoiceField(
            choices=settings.PREFERRED_LANGUAGES,
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        status = forms.MultipleChoiceField(
            choices=[("active", _("Active")), ("inactive", _("Inactive"))],
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        include_trash = forms.BooleanField(required=False, label=_("Include trash"))

    def get_layout(self):
        self.checkboxcounterid = hg.html_id(self, "checkbox-counter")
        ret = super().get_layout()
        toolbar = list(
            ret.filter(
                lambda e, a: getattr(e, "attributes", {}).get("_class", "")
                == "bx--toolbar-content"
            )
        )[0]
        toolbar.insert(
            -2,
            hg.DIV(
                hg.SPAN(self._checkbox_count(), id=self.checkboxcounterid),
                layout.icon.Icon(
                    "close",
                    focusable="false",
                    size=15,
                    role="img",
                    onclick=f"document.location = '{self.request.path}'",
                ),
                role="button",
                _class="bx--list-box__selection bx--list-box__selection--multi bx--tag--filter",
                style="margin: auto 0.5rem;",
                tabindex="0",
                title=("Reset"),
            ),
        )
        return ret

    def _filterform(self):
        return self.FilterForm({"status": ["active"], **self.request.GET})

    def _checkbox_count(self):
        counter = 0
        form = self._filterform()
        if form.is_valid():
            counter += 1 if form.cleaned_data["naturalperson"] else 0
            counter += 1 if form.cleaned_data["legalperson"] else 0
            counter += 1 if form.cleaned_data["personassociation"] else 0
            counter += form.cleaned_data["naturalperson_subtypes"].count()
            counter += form.cleaned_data["legalperson_subtypes"].count()
            counter += form.cleaned_data["personassociation_subtypes"].count()
            counter += form.cleaned_data["categories"].count()
            counter += len(form.cleaned_data["preferred_language"])
            counter += len(form.cleaned_data["status"])
            counter += 1 if form.cleaned_data["include_trash"] else 0
        return counter

    def get_queryset(self):
        form = self._filterform()
        if form.is_valid():
            ret = (
                super().get_queryset()
                if form.cleaned_data.get("include_trash", False)
                else self.model.objects.not_deleted()
            )
            if any(
                [
                    form.cleaned_data[i]
                    for i in (
                        "naturalperson",
                        "legalperson",
                        "personassociation",
                        "naturalperson_subtypes",
                        "legalperson_subtypes",
                        "personassociation_subtypes",
                    )
                ]
            ):
                q = Q()
                for i in ("naturalperson", "legalperson", "personassociation"):
                    # setup some logic descriptors
                    maintype_selected = bool(form.cleaned_data[i])
                    subtype_selected = bool(form.cleaned_data[f"{i}_subtypes"])
                    all_subtypes_selected = bool(
                        form.cleaned_data[f"{i}_subtypes"].count()
                        == form.fields[f"{i}_subtypes"].queryset.count()
                    )

                    # the semantics for this filter are not 100% clear
                    # there are also cases where a subtype has the wrong maintype
                    # This code tries to make the selection consistent to what a user
                    # would expect, but these expectations can still vary...
                    if maintype_selected:
                        typeq = Q(_maintype=i)
                        if subtype_selected:
                            if not all_subtypes_selected:
                                typeq &= Q(_type__in=form.cleaned_data[f"{i}_subtypes"])
                        else:
                            typeq &= ~Q(_type__in=form.fields[f"{i}_subtypes"].queryset)
                        q |= typeq
                    else:
                        q |= Q(_type__in=form.cleaned_data[f"{i}_subtypes"])
                ret = ret.filter(q)
            if form.cleaned_data.get("categories"):
                ret = ret.filter(categories__in=form.cleaned_data["categories"])
            if form.cleaned_data.get("preferred_language"):
                ret = ret.filter(
                    preferred_language__in=form.cleaned_data["preferred_language"]
                )
            if len(form.cleaned_data.get("status")) == 1:
                ret = ret.filter(active=form.cleaned_data.get("status")[0] == "active")

        return ret

    def get_settingspanel(self):
        return hg.DIV(
            layout.form.Form(
                self._filterform(),
                hg.DIV(
                    hg.DIV(
                        hg.DIV(layout.helpers.Label(_("Categories"))),
                        hg.DIV(
                            hg.DIV(
                                hg.DIV(
                                    layout.form.FormField(
                                        "naturalperson",
                                        elementattributes={
                                            "onclick": "updateCheckboxGroupItems(this.parentElement.parentElement)"
                                        },
                                    ),
                                    hg.DIV(
                                        layout.form.FormField(
                                            "naturalperson_subtypes",
                                            elementattributes={
                                                "style": "padding-left: 1rem",
                                            },
                                        ),
                                        style="margin-top: -2rem",
                                    ),
                                ),
                                layout.form.FormField(
                                    "personassociation",
                                    elementattributes={
                                        "onclick": "updateCheckboxGroupItems(this.parentElement.parentElement)"
                                    },
                                ),
                                hg.DIV(
                                    layout.form.FormField(
                                        "personassociation_subtypes",
                                        elementattributes={
                                            "style": "padding-left: 1rem"
                                        },
                                    ),
                                    style="margin-top: -2rem",
                                ),
                                style="margin-right: 16px",
                            ),
                            hg.DIV(
                                layout.form.FormField(
                                    "legalperson",
                                    elementattributes={
                                        "onclick": "updateCheckboxGroupItems(this.parentElement.parentElement)"
                                    },
                                ),
                                hg.DIV(
                                    layout.form.FormField(
                                        "legalperson_subtypes",
                                        elementattributes={
                                            "style": "padding-left: 1rem"
                                        },
                                    ),
                                    style="margin-top: -2rem",
                                ),
                                style="margin-right: 16px",
                            ),
                            style="display: flex",
                        ),
                        style="border-right: #ccc solid 1px; margin: 0 16px 0 0",
                    ),
                    hg.DIV(
                        hg.DIV(layout.helpers.Label(_("Tags"))),
                        hg.DIV(
                            layout.form.FormField("categories"),
                            style="margin-right: 16px",
                        ),
                        style="border-right: #ccc solid 1px; margin: 0 16px 0 0; overflow-y: scroll",
                    ),
                    hg.DIV(
                        hg.DIV(layout.helpers.Label(_("Languages"))),
                        hg.DIV(
                            layout.form.FormField("preferred_language"),
                            style="margin-right: 16px",
                        ),
                        style="border-right: #ccc solid 1px; margin: 0 16px 0 0",
                    ),
                    hg.DIV(
                        hg.DIV(layout.helpers.Label(_("Status"))),
                        hg.DIV(layout.form.FormField("status"), style="flex-grow: 0"),
                        hg.DIV(style="flex-grow: 1"),
                        hg.DIV(
                            layout.form.FormField("include_trash"),
                            style="max-height: 2rem",
                        ),
                        style="display: flex; flex-direction: column",
                    ),
                    style="display: flex; max-height: 50vh; padding: 24px 32px 0 32px",
                ),
                hg.DIV(
                    layout.button.Button(
                        _("Cancel"),
                        buttontype="ghost",
                        onclick="this.parentElement.parentElement.parentElement.parentElement.parentElement.style.display = 'none'",
                    ),
                    layout.button.Button(
                        _("Reset"),
                        buttontype="secondary",
                        islink=True,
                        href=self.request.path,
                    ),
                    layout.button.Button(
                        pgettext_lazy("apply filter", "Filter"),
                        type="submit",
                    ),
                    style="display: flex; justify-content: flex-end; margin-top: 24px",
                    _class="bx--modal-footer",
                ),
                method="GET",
            ),
            hg.SCRIPT(
                mark_safe(
                    """
                    function updateCheckboxGroupItems(group) {
                        var items = $$('input[type=checkbox]', group);
                        var value = items[0].getAttribute('aria-checked');
                        value = value == 'true' ? 'true' : 'false';
                        for(var i = 1; i < items.length; ++i) {
                            new CarbonComponents.Checkbox(items[i]).setState(value);
                        }
                    }
                    function updateCheckboxCounter(group) {
                        var items = $$('input[type=checkbox]', group);
                        var count = 0;
                        for(item of items)
                            count += item.getAttribute('aria-checked') == 'true' ? 1 : 0
                        $('#%s').innerHTML = count;
                    }
                    """
                    % (self.checkboxcounterid,)
                )
            ),
            style="background-color: #fff",
            onclick="updateCheckboxCounter(this)",
        )

    def export(self, *args, **kwargs):
        # Fields which are filtered should also be displayed in columns
        form = self._filterform()
        columns = list(self.columns)
        if form.is_valid():

            # only the categories selected in the filter should be visible in the export
            if form.cleaned_data.get("categories"):
                categories = set(form.cleaned_data.get("categories"))

                def render_matching_categories(context, element):
                    return ", ".join(
                        str(i)
                        for i in categories & set(context["row"].categories.all())
                    )

                columns.append(
                    DataTableColumn(
                        layout.fieldlabel(models.Person, "categories"),
                        hg.F(render_matching_categories),
                    )
                )
            if form.cleaned_data.get("preferred_language"):
                columns.append("preferred_language")

        return super().export(*args, columns=columns, **kwargs)