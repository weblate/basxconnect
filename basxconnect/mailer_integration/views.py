import traceback

import bread.layout.components.notification
import htmlgenerator as hg
from bread import layout, menu
from bread.layout.components.forms import Form
from bread.utils import aslayout, reverse_model
from bread.utils.links import Link
from bread.views import AddView, EditView
from django import conf, forms
from django.urls import reverse_lazy
from django.utils.formats import localize
from django.utils.translation import gettext_lazy as _

from basxconnect.core.views import menu_views
from basxconnect.mailer_integration import download_data, settings
from basxconnect.mailer_integration.abstract.abstract_datasource import MailerPerson
from basxconnect.mailer_integration.mailchimp import datasource
from basxconnect.mailer_integration.models import SynchronizationResult

C = bread.layout.grid.Col
R = bread.layout.grid.Row


@aslayout
def mailer_synchronization_view(request):
    if request.method == "POST":
        try:
            sync_result = download_data.download_persons(settings.MAILER)
            notification = bread.layout.components.notification.InlineNotification(
                "Success",
                f"Synchronized mailing preferences for {sync_result.total_synchronized_persons} Mailchimp "
                f"contacts. {sync_result.new_persons.count()} new persons were added to the BasxConnect database. "
                + (
                    "The following mailchimp contacts are not yet in our database but were also not "
                    "added because they were invalid:"
                    + (", ".join(sync_result.invalid_new_persons.all()))
                    if sync_result.invalid_new_persons.count() > 0
                    else ""
                ),
            )
        except Exception:
            notification = bread.layout.components.notification.InlineNotification(
                "Error",
                f"An error occured during synchronization. {traceback.format_exc()}",
                kind="error",
            )
    else:
        notification = None

    return hg.BaseElement(
        Form.wrap_with_form(
            forms.Form(),
            bread.layout.grid.Grid(
                hg.H3(_("Synchronization of Email Subcriptions")),
                R(
                    C(
                        _(
                            "The button below is currently the only way of getting new subcribers from the mailer into our system. Is it also the only way of getting updates for subscribers that we already have in our system. This is what happens when the button is pressed:"
                        ),
                        hg.UL(
                            hg.LI(
                                _(
                                    "For all the Subscriptions that are in the relevant segment (e.g. 'UM Switzerland') in the Mailer, we check whether the email address is already in BasxConnect."
                                ),
                                _class="bx--list__item",
                            ),
                            hg.LI(
                                _(
                                    "If an email address is already in BasxConnect, the downloaded subscription will be attached to the email address and override the current values in case there are any."
                                ),
                                _class="bx--list__item",
                            ),
                            hg.LI(
                                _(
                                    "If an email address is not yet in BasxConnect and the subscription fulfills some additional criteria, a new person with that email address and subscription is created in BasxConnect. The additional criteria for a subscription to be used for creating a new person are that the status is either 'subscribed' or 'unsubcribed' (and not e.g. 'cleaned') and that the subscription has a valid country."
                                ),
                                _class="bx--list__item",
                            ),
                            _class="bx--list--unordered",
                        ),
                        width=8,
                    )
                ),
                hg.If(notification is not None, notification),
                gutter=False,
            ),
            submit_label=_("Download subscriptions"),
        ),
        display_last_execution(),
    )


def display_last_execution():
    last_execution = SynchronizationResult.objects.order_by(
        "-sync_completed_datetime"
    ).first()
    return hg.DIV(
        hg.H4(_("Report of most recent execution")),
        hg.DIV(
            _("Time of completion: "),
            localize(
                last_execution.sync_completed_datetime, use_l10n=conf.settings.USE_L10N
            ),
        ),
        hg.DIV(
            _("Total subscriptions in segment: "),
            last_execution.total_synchronized_persons,
        ),
        hg.DIV(_("Newly added: "), ", ".join(last_execution.new_persons.all())),
        hg.DIV(_("Invalid: "), ", ".join(last_execution.invalid_new_persons.all())),
    )


menu.registeritem(
    menu.Item(
        Link(
            reverse_lazy(
                "basxconnect.mailer_integration.views.mailer_synchronization_view"
            ),
            _("External mailer"),
        ),
        menu_views.settingsgroup,
    )
)


class AddMailingPreferencesView(AddView):
    def get_success_url(self):
        return reverse_model(
            self.object.email.person, "read", kwargs={"pk": self.object.email.person.pk}
        )

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        settings.MAILER.add_person(MailerPerson.from_mailing_preferences(self.object))
        return response


class EditMailingPreferencesView(EditView):
    fields = ["interests", "language"]

    def get_success_url(self):
        return reverse_model(
            self.object.email.person, "read", kwargs={"pk": self.object.email.person.pk}
        )

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        # TODO: https://github.com/basxsoftwareassociation/basxconnect/issues/140
        datasource.MailchimpDatasource().put_person(
            MailerPerson.from_mailing_preferences(self.object)
        )
        return result

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in self.fields]
        return hg.DIV(*form_fields)
