from bread import layout
from bread.layout.components.icon import Icon
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models
from basxconnect.core.layouts import editperson

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editpersonassociation_form(request):
    return editperson.editperson_form(request, base_data_tab, mailings_tab)


def base_data_tab():
    return layout.tabs.Tab(
        _("Base data"),
        editperson.grid_inside_tab(
            R(
                editperson.tile_col_edit_modal(
                    models.PersonAssociation,
                    Icon("building"),
                    [
                        "name",
                        "preferred_language",
                        "salutation_letter",
                    ],
                ),
                editperson.person_metadata(),
            ),
            editperson.contact_details(),
        ),
    )


def mailings_tab(request):

    from django.apps import apps

    if apps.is_installed("basxconnect.mailer_integration"):
        from basxconnect.mailer_integration.layouts import mailer_integration_tile

        mailer_tile = mailer_integration_tile(request)
    else:
        mailer_tile = editperson.tiling_col()

    return layout.tabs.Tab(
        _("Mailings"),
        editperson.grid_inside_tab(
            R(
                mailer_tile,
                editperson.tiling_col(),
            ),
        ),
    )
