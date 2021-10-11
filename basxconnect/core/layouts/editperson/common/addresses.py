import htmlgenerator as hg
from bread import layout
from bread.layout.components.icon import Icon
from bread.layout.components.modal import modal_with_trigger
from bread.utils import Link, ModelHref, pretty_modelname, reverse_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from htmlgenerator import mark_safe

from basxconnect.core import models
from basxconnect.core.layouts.editperson.common.base_data_building_blocks import (
    tile_with_icon,
    tiling_col,
)

R = layout.grid.Row
C = layout.grid.Col


def addresses(request):
    return hg.BaseElement(
        R(
            postals(),
            numbers(request),
        ),
        R(
            email(request),
            urls(request),
        ),
    )


def numbers(request):
    return tile_with_datatable(
        models.Phone,
        hg.F(lambda c: c["object"].core_phone_list.all()),
        ["type", "number"],
        request,
    )


def tile_with_datatable(model, queryset, fields, request):
    modal = layout.modal.Modal.with_ajax_content(
        _("Add"),
        ModelHref(
            model,
            "add",
            query=hg.F(lambda c: {"person": c["object"].pk, "asajax": True}),
        ),
        submitlabel=_("Save"),
    )
    return tiling_col(
        layout.datatable.DataTable.from_model(
            model,
            queryset,
            prevent_automatic_sortingnames=True,
            columns=fields,
            rowactions=[
                Link(
                    href=ModelHref(
                        model,
                        "edit",
                        kwargs={"pk": hg.C("row.pk")},
                        query={"next": request.get_full_path()},
                    ),
                    iconname="edit",
                    label=_("Edit"),
                ),
                Link(
                    href=ModelHref(
                        model,
                        "confirm_delete",
                        kwargs={"pk": hg.C("row.pk")},
                        query={"next": request.get_full_path()},
                    ),
                    iconname="trash-can",
                    label=_("Delete"),
                ),
            ],
            primary_button=layout.button.Button(
                _("Add"), buttontype="primary", **modal.openerattributes
            ),
            style="border-top: none;",
        ),
        modal,
    )


def email(request):
    return tile_with_datatable(
        models.Email,
        hg.F(lambda c: c["object"].core_email_list.all()),
        ["type", "email"],
        request,
    )


def urls(request):
    return tile_with_datatable(
        models.Web,
        hg.F(lambda c: c["object"].core_web_list.all()),
        ["type", "url"],
        request,
    )


def edit_heading(model: type):
    return _("Edit %s") % pretty_modelname(model)


def display_postal(postal: models.Postal):
    modal = layout.modal.Modal.with_ajax_content(
        heading=edit_heading(models.Postal),
        url=reverse_model(
            models.Postal,
            "ajax_edit",
            kwargs={"pk": postal.pk},
            query={"asajax": True},
        ),
        submitlabel=_("Save"),
    )
    return R(
        C(
            hg.DIV(
                postal.type,
                " (" + _("primary") + ")"
                if postal.person.primary_postal_address
                and postal.person.primary_postal_address.pk == postal.pk
                else "",
                style="font-weight: bold; margin-bottom: 1rem;",
            ),
            hg.DIV(postal.address, style="margin-bottom: 0.25rem;"),
            hg.DIV(postal.postcode, " ", postal.city, style="margin-bottom: 0.25rem;"),
            hg.DIV(postal.get_country_display()),
            hg.If(
                postal.valid_from,
                hg.DIV(
                    hg.SPAN(_("Valid from: "), style="font-weight: bold;"),
                    postal.valid_from,
                    " ",
                    style="display: inline-block; margin-top: 1rem; margin-right: 1rem;",
                ),
                hg.BaseElement(),
            ),
            hg.If(
                postal.valid_until,
                hg.DIV(
                    hg.SPAN(_("Valid until: "), style="font-weight: bold;"),
                    postal.valid_until,
                    style="display: inline-block; margin-top: 1rem;",
                ),
                hg.BaseElement(),
            ),
            hg.DIV(
                edit_postal_button(modal),
            ),
        ),
        **(
            {"_class": "inactive_postal", "style": "display: none; margin-top: 1.5rem;"}
            if postal.valid_until and postal.valid_until < timezone.now().date()
            else {"style": "margin-top: 1.5rem;"}
        ),
    )


def edit_postal_button(modal):
    return hg.SPAN(
        layout.button.Button(
            "",
            buttontype="ghost",
            icon="edit",
            **modal.openerattributes,
        ),
        modal,
    )


def delete_postal_button(postal):
    return layout.button.Button(
        _("Delete"),
        buttontype="ghost",
        icon="trash-can",
        notext=True,
        hx_post=reverse_model(
            models.Postal,
            "ajax_delete",
            kwargs={
                "pk": postal.pk,
            },
            query={
                "asajax": True,
            },
        ),
    )


def postals():
    return tile_with_icon(
        Icon("map"),
        hg.H4(_("Address(es)")),
        R(
            C(
                hg.Iterator(
                    hg.F(
                        lambda c: getattr(c["object"], "core_postal_list").all()
                        if hasattr(c["object"], "core_postal_list")
                        else []
                    ),
                    "i",
                    hg.BaseElement(
                        hg.F(lambda c: display_postal(c["i"])),
                    ),
                )
            )
        ),
        R(
            C(
                layout.button.Button(
                    _("Hide inactive postals"),
                    onclick="hideInactivePostals();",
                    id="hideInactivePostalsButton",
                    style="display: none;",
                    icon="view--off",
                    buttontype="ghost",
                ),
                layout.button.Button(
                    _("Show inactive postals"),
                    onclick="showInactivePostals();",
                    id="showInactivePostalsButton",
                    icon="view",
                    buttontype="ghost",
                ),
            ),
            style="margin-top: 1.5rem;",
        ),
        R(
            C(
                modal_with_trigger(
                    modal_add_postal(),
                    layout.button.Button,
                    "Add",
                    buttontype="ghost",
                    icon="Add",
                ),
            ),
        ),
        hg.SCRIPT(
            mark_safe(
                """
                function hideInactivePostals() {
                    for(i of $$('.inactive_postal')) {
                        $(i)._.style({display: "none"});
                    }
                    $$('#hideInactivePostalsButton')._.style({display: "none"})
                    $$('#showInactivePostalsButton')._.style({display: "block"})
                }
                function showInactivePostals() {
                    for(i of $$('.inactive_postal')) {
                        $(i)._.style({display: "block"});
                    }
                    $$('#hideInactivePostalsButton')._.style({display: "block"})
                    $$('#showInactivePostalsButton')._.style({display: "none"})
                }
                """
            )
        ),
    )


def modal_add_postal():
    return layout.modal.Modal.with_ajax_content(
        heading=_("Add Address"),
        url=hg.F(
            lambda c: reverse_model(
                models.Postal,
                "ajax_add",
                query={"asajax": True, "person": c["object"].pk},
            ),
        ),
        submitlabel=_("Save"),
    )