from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MAX_RETRY = 20
MAX_RETRY_FOR_SESSION = 10
BACK_OFF_FACTOR = 0.5
ERROR_CODES = (429, 500, 502, 504)


def requests_retry_session(retries=MAX_RETRY_FOR_SESSION,
    back_off_factor=BACK_OFF_FACTOR,
    status_force_list=ERROR_CODES, 
    session=None):
       session = session  
       retry = Retry(total=retries, read=retries, connect=retries,
                     backoff_factor=back_off_factor,
                     status_forcelist=status_force_list,
                     method_whitelist=frozenset(['GET', 'POST']))
       adapter = HTTPAdapter(max_retries=retry)
       session.mount('http://', adapter)
       session.mount('https://', adapter)
       return session