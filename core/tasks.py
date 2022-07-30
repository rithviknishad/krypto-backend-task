from celery import shared_task

from celery import periodic_task
from datetime import datetime, timedelta
from django.core.mail import send_mail
from users.models import User

import inspect
import requests

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


def __fetch_current_prices() -> dict[str, float]:
    try:
        res = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false"
        )
        data = res.json()
        current_prices = dict((e["symbol"], e["current_price"]) for e in data)
        return current_prices
    except:
        return {}


@periodic_task(run_every=timedelta(seconds=10))
def dispatch_alerts():
    prices = __fetch_current_prices()
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
