import inspect
from datetime import datetime, timedelta

from celery import periodic_task, shared_task
from django.core.mail import send_mail
from users.models import User
from utils.utils import fetch_current_prices

from .models import Alert


def __compose_alert_mail(alert: Alert) -> str:
    user = alert.user
    coin_id = alert.coin_id.upper()
    trigger_value = alert.trigger_value
    return {
        "subject": f"Alert! {coin_id} has crossed {trigger_value} USD!",
        "message": inspect.cleandoc(
            f"""
            Dear {user.name},

            The price for {coin_id} has crossed {trigger_value} USD.

            ---
            With <3 from Krypto Backend Task
            """
        ),
        "from_email": "Krypto Price Alert Task <krypto-backend-task@rithviknishad.dev>",
        "recipient_list": [user.email],
    }


@periodic_task(run_every=timedelta(seconds=10))
def dispatch_alerts():
    prices = fetch_current_prices()
    # TODO: bulk_update
    alerts_to_be_dispatched = []
    for alert in Alert.objects.filter(deleted=False, triggered=False):
        if alert.coin_id not in prices:
            # potential bug: coins with very low market value (not in top 100) will get ignored.
            # ignoring this edge case in this prototype.
            continue
        should_trigger = alert.trigger_on_lte and prices[alert.coin_id] <= alert.trigger_value
        should_trigger = should_trigger or (not alert.trigger_on_lte) and prices[alert.coin_id] >= alert.trigger_value
        if should_trigger:
            alerts_to_be_dispatched.append(alert)
    now = datetime.now()
    for alert in alerts_to_be_dispatched:
        send_mail(**__compose_alert_mail(alert))
        alert.triggered_on = now
        alert.save(update_fields=["triggered_on"])
