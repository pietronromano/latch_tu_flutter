"""
 This library offers an API to use LatchAuth in a python environment.
 Copyright (C) 2013 Telefonica Digital España S.L.

 This library is free software you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation either
 version 2.1 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""
import time

from latchsrc.latchauth import LatchAuth



class LatchApp(LatchAuth):

    def __init__(self, app_id, secret_key):
        """
        Create an instance of the class with the Application ID and secret obtained from Eleven Paths
        @param $app_id
        @param $secret_key
        """
        super(LatchApp, self).__init__(app_id, secret_key)

    def pair(self, token, web3Wallet=None, web3Signature=None):
        if web3Wallet is None or web3Signature is None:
            return self._http("GET", self.API_PAIR_URL + "/" + token)
        else:
            params = {"wallet": web3Wallet, "signature": web3Signature}
            return self._http("POST", self.API_PAIR_URL + "/" + token, None, params)

    def status(self, account_id, silent=False, nootp=False):
        url = self.API_CHECK_STATUS_URL + "/" + account_id
        if nootp:
            url += '/nootp'
        if silent:
            url += '/silent'
        return self._http("GET", url)



    def unpair(self, account_id):
        return self._http("GET", self.API_UNPAIR_URL + "/" + account_id)

    def lock(self, account_id, operation_id=None):
        if operation_id is None:
            return self._http("POST", self.API_LOCK_URL + "/" + account_id)
        else:
            return self._http("POST", self.API_LOCK_URL + "/" + account_id + "/op/" + operation_id)

    def unlock(self, account_id, operation_id=None):
        if operation_id is None:
            return self._http("POST", self.API_UNLOCK_URL + "/" + account_id)
        else:
            return self._http("POST", self.API_UNLOCK_URL + "/" + account_id + "/op/" + operation_id)

    def history(self, account_id, from_t=0, to_t=None):
        if to_t is None:
            to_t = int(round(time.time() * 1000))
        return self._http("GET", self.API_HISTORY_URL + "/" + account_id + "/" + str(from_t) + "/" + str(to_t))
    
    def totp_create(self, account_id):
        url = "/api/3.0/totps"
        params = dict()
        params["userId"] = account_id
        params["commonName"] = account_id
        return self._http("POST", url,None,params)
    
    def operation(self, account_id):
        url = "/2.0/operation"  + "/" + account_id
        return self._http("GET", url)