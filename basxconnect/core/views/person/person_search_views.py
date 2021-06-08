import htmlgenerator as hg
from bread import layout as layout
from bread.utils.urls import reverse_model
from django.http import HttpResponse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from haystack.query import SearchQuerySet
from haystack.utils.highlighting import Highlighter

from ... import models

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


# Search view
# simple person search view, for use with ajax calls
def searchperson(request):
    query = request.GET.get("q")
    highlight = CustomHighlighter(query)

    if not query or len(query) < 3:
        return HttpResponse("")

    objects = (
        SearchQuerySet()
        .models(models.Person)
        .autocomplete(name_auto=query)
        .filter_or(personnumber=query)
    )

    ret = display_results(objects, highlight)
    return HttpResponse(
        hg.DIV(
            ret,
            _class="raised",
            style="margin-bottom: 1rem; padding: 16px 0 48px 48px; background-color: #fff",
        ).render({})
    )


def display_results(objects, highlight):
    if objects.count() == 0:
        return _("No results")

    return hg.UL(
        hg.LI(_("%s items found") % len(objects), style="margin-bottom: 20px"),
        hg.Iterator(
            objects,
            "object",
            hg.If(
                hg.C("object.object"),
                hg.LI(
                    hg.F(
                        lambda c, e: hg.SPAN(
                            mark_safe(
                                highlight.highlight(c["object"].object.personnumber)
                            ),
                            style="width: 48px; display: inline-block",
                        )
                    ),
                    " ",
                    hg.F(
                        lambda c, e: mark_safe(
                            highlight.highlight(
                                c["object"].object.search_index_snippet()
                            )
                        )
                    ),
                    style="cursor: pointer; padding: 8px 0;",
                    onclick=hg.BaseElement(
                        "document.location = '",
                        hg.F(
                            lambda c, e: reverse_model(
                                c["object"].object,
                                "edit",
                                kwargs={"pk": c["object"].object.pk},
                            )
                        ),
                        "'",
                    ),
                    onmouseenter="this.style.backgroundColor = 'lightgray'",
                    onmouseleave="this.style.backgroundColor = 'initial'",
                ),
            ),
        ),
    )


class CustomHighlighter(Highlighter):
    def find_window(self, highlight_locations):
        return (0, self.max_length)
