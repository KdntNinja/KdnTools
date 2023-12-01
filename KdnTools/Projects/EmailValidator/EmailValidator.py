import asyncio
import aiodns
import logging
import re
import smtplib
import socket
import collections.abc as abc


class EmailValidator:
    EMAIL_REGEX = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    MX_DNS_CACHE = {}
    MX_CHECK_CACHE = {}

    def __init__(self):
        self.setup_module_logger('verify_email')

    @staticmethod
    def setup_module_logger(name):
        logger = logging.getLogger(name)
        ch = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    @staticmethod
    def is_list(obj):
        return isinstance(obj, abc.Sequence) and not isinstance(obj, str)

    async def get_mx_ip(self, hostname):
        if hostname not in self.MX_DNS_CACHE:
            try:
                resolver = aiodns.DNSResolver()
                self.MX_DNS_CACHE[hostname] = await resolver.query(hostname, 'MX')
            except aiodns.error.DNSError as e:
                self.MX_DNS_CACHE[hostname] = None
        return self.MX_DNS_CACHE[hostname]

    async def get_mx_hosts(self, email):
        hostname = email[email.find('@') + 1:]
        if hostname in self.MX_DNS_CACHE:
            mx_hosts = self.MX_DNS_CACHE[hostname]
        else:
            mx_hosts = await self.get_mx_ip(hostname)
        return mx_hosts

    async def handler_verify(self, mx_hosts, email, timeout=None):
        for mx in mx_hosts:
            res = await self.network_calls(mx, email, timeout)
            if res:
                return res
        return False

    async def syntax_check(self, email):
        if re.match(self.EMAIL_REGEX, email):
            return True
        return False

    async def _verify_email(self, email, timeout=None, verify=True):
        is_valid_syntax = await self.syntax_check(email)
        if is_valid_syntax:
            if verify:
                mx_hosts = await self.get_mx_hosts(email)
                if mx_hosts is None:
                    return False
                else:
                    return await self.handler_verify(mx_hosts, email, timeout)
        else:
            return False

    def validate(self, emails, timeout=None, verify=True, debug=False):
        if debug:
            logger = logging.getLogger('verify_email')
            logger.setLevel(logging.DEBUG)
        result = []
        if not self.is_list(emails):
            emails = [emails]

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.new_event_loop()

        for email in emails:
            resp = loop.run_until_complete(self._verify_email(email, timeout, verify))
            result.append(resp)

        return result if len(result) > 1 else result[0]

    @staticmethod
    async def network_calls(mx, email, timeout=20):
        logger = logging.getLogger('verify_email')
        result = False
        try:
            smtp = smtplib.SMTP(mx.host, timeout=timeout)
            status, _ = smtp.ehlo()
            if status >= 400:
                smtp.quit()
                logger.debug(f'{mx} answer: {status} - {_}\n')
                return False
            smtp.mail('')
            status, _ = smtp.rcpt(email)
            if status >= 400:
                logger.debug(f'{mx} answer: {status} - {_}\n')
                result = False
            if 200 <= status <= 250:
                result = True

            logger.debug(f'{mx} answer: {status} - {_}\n')
            smtp.quit()

        except smtplib.SMTPServerDisconnected:
            logger.debug(f'Server does not permit verify user, {mx} disconnected.\n')
        except smtplib.SMTPConnectError:
            logger.debug(f'Unable to connect to {mx}.\n')
        except socket.timeout as e:
            logger.debug(f'Timeout connecting to server {mx}: {e}.\n')
            return None
        except socket.error as e:
            logger.debug(f'ServerError or socket.error exception raised {e}.\n')
            return None

        return result
