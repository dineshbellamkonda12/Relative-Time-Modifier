import pytest
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from relative_time_modifier import parse


@pytest.mark.parametrize("input_str, expected_date", [
    # Addition
    ("now()+1d@h", datetime.utcnow().replace(minute=0,
     second=0, microsecond=0) + timedelta(days=1)),

    ("now()+2h@m", datetime.utcnow().replace(second=0,
     microsecond=0) + timedelta(hours=2)),

    ("now()+3mon@d", datetime.utcnow().replace(hour=0, minute=0,
     second=0, microsecond=0) + relativedelta(months=3)),

    ("now()+1y@mon", datetime.utcnow().replace(day=1,
     hour=0, minute=0, second=0, microsecond=0) + relativedelta(years=1)),

    ("now()+28d", datetime.utcnow() + timedelta(days=28)),

    # Subtraction
    ("now()-1h", datetime.utcnow() - timedelta(hours=1)),

    ("now()-1d@h", datetime.utcnow().replace(minute=0,
     second=0, microsecond=0) - timedelta(days=1)),

    ("now()-2h@m", datetime.utcnow().replace(second=0,
     microsecond=0) - timedelta(hours=2)),

    ("now()-3mon@d", datetime.utcnow().replace(hour=0, minute=0,
     second=0, microsecond=0) - relativedelta(months=3)),

    ("now()-1y@mon", datetime.utcnow().replace(day=1,
     hour=0, minute=0, second=0, microsecond=0) - relativedelta(years=1)),

    # Snap only
    ("now()@h", datetime.utcnow().replace(minute=0, second=0, microsecond=0)),

    ("now()@m", datetime.utcnow().replace(second=0, microsecond=0)),

    ("now()@d", datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)),

    ("now()@mon", datetime.utcnow().replace(day=1,
     hour=0, minute=0, second=0, microsecond=0)),

    ("now()@y", datetime.utcnow().replace(month=1,
     day=1, hour=0, minute=0, second=0, microsecond=0)),

    # Combined
    ("now()-1y-2mon+3d@h", datetime.utcnow().replace(minute=0, second=0,
     microsecond=0) - relativedelta(years=1, months=2) + timedelta(days=3)),

    ("now()+1mon-15d@h", datetime.utcnow().replace(minute=0, second=0,
     microsecond=0) + relativedelta(months=1) - timedelta(days=15)),

    ("now()+2y-1mon@mon", datetime.utcnow().replace(day=1,
     hour=0, minute=0, second=0, microsecond=0) + relativedelta(years=2) - relativedelta(months=1)),

    ("now()-3d-12h@h", datetime.utcnow().replace(minute=0,
     second=0, microsecond=0) - timedelta(days=3, hours=12)),
])
def test_parse_function(input_str, expected_date):
    parsed_date = parse(input_str)
    assert parsed_date.strftime(
        '%Y-%m-%d %H:%M:%S') == expected_date.strftime('%Y-%m-%d %H:%M:%S')
