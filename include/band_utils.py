# Amateur radio band lookup utility for mLogger

def get_band_from_frequency(freq_mhz):
    """
    Given a frequency in MHz (float or str), return the amateur radio band as a string.
    Returns 'Unknown' if not matched.
    """
    try:
        freq = float(freq_mhz)
    except (ValueError, TypeError):
        return 'Unknown'
    bands = [
        (1.8, 2.0, '160m'),
        (3.5, 4.0, '80m'),
        (5.3305, 5.4065, '60m'),
        (7.0, 7.3, '40m'),
        (10.1, 10.15, '30m'),
        (14.0, 14.35, '20m'),
        (18.068, 18.168, '17m'),
        (21.0, 21.45, '15m'),
        (24.89, 24.99, '12m'),
        (28.0, 29.7, '10m'),
        (50.0, 54.0, '6m'),
        (144.0, 148.0, '2m'),
        (222.0, 225.0, '1.25m'),
        (420.0, 450.0, '70cm'),
        (902.0, 928.0, '33cm'),
        (1240.0, 1300.0, '23cm'),
        (2300.0, 2450.0, '13cm'),
        (3300.0, 3500.0, '9cm'),
        (5650.0, 5925.0, '5cm'),
        (10000.0, 10500.0, '3cm'),
    ]
    for low, high, band in bands:
        if low <= freq <= high:
            return band
    return 'Unknown'
