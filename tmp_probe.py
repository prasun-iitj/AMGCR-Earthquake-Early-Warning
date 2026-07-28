from obspy.clients.fdsn import Client
from obspy import UTCDateTime

providers = ['IRIS','USGS','EMSC','GFZ','https://service.iris.edu','https://earthquake.usgs.gov']
for provider in providers:
    try:
        client = Client(provider, timeout=20)
        print('PROVIDER', provider, '->', client.base_url)
        print('SERVICES', client.services)
        try:
            cat = client.get_events(starttime=UTCDateTime('2024-01-01'), endtime=UTCDateTime('2024-01-02'), minmagnitude=4.0, maxmagnitude=8.0, limit=3)
            print('EVENTS', len(cat))
        except Exception as exc:
            print('EVENT_ERR', type(exc).__name__, exc)
    except Exception as exc:
        print('CLIENT_ERR', provider, type(exc).__name__, exc)
    print('---')
