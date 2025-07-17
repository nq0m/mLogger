# FLRig XML-RPC polling utility for mLogger
#trunk-ignore(bandit/B411): XML-RPC is safe in this context
import xmlrpc.client

def poll_flrig_frequency_mode(host='localhost', port=12345, timeout=2.0):
    """
    Poll FLRig via XML-RPC for current frequency and mode.
    Returns (frequency, mode) as strings, or (None, None) on error.
    host: FLRig host (default 'localhost')
    port: FLRig XML-RPC port (default 12345)
    timeout: socket timeout in seconds
    """
    url = f'http://{host}:{port}'
    try:
        proxy = xmlrpc.client.ServerProxy(url, allow_none=True)
        # FLRig returns frequency in Hz as int, mode as string
        freq_hz = proxy.rig.get_freq()
        mode = proxy.rig.get_mode()
        freq_mhz = str(round(float(freq_hz) / 1_000_000, 5))
        return freq_mhz, mode
    except Exception:
        return None, None
