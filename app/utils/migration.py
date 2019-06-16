# !/usr/bin/env python

import csv
import os
import re

import django
import pytz
from django.utils import timezone

def read_env():
    """Pulled from Honcho code with minor updates, reads local default
    environment variables from a .env file located in the project root
    directory.
    """
    try:
        with open('.env') as f:
            content = f.read()
    except IOError:
        content = ''


    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))

            print(key, val)
            os.environ.setdefault(key, val)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
read_env()
django.setup()
from app.accounts.models import User
from app.finance.models import Tag, Transaction



if __name__ == '__main__':
    user = User.objects.get(email='peternjengask@gmail.com')

    with open('transactions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        current_tz = timezone.get_current_timezone()
        Transaction.objects.filter(created_by=user).delete()
        for row in csv_reader:
            try:
                date = pytz.utc.localize(timezone.datetime.strptime(row[0], '%Y-%m-%d'))
                description = row[1]
                amount = float(row[3])
                tag = row[5]
                tag = Tag.objects.get(
                    name=tag.lower(),
                    created_by=user,
                )

                transaction = Transaction.objects.create(
                    amount=amount,
                    tag=tag,
                    created_at=date,
                    created_by=user,
                    description=description,
                    transaction_date=date
                )
                transaction.created_at = date
                transaction.transaction_date = date
                transaction.save()

                print(transaction)
            except Exception:
                pass