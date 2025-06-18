################################
# PT NAD Connector for OpenCTI #
################################

import json
import os
import sys
import time
import yaml

from pycti import OpenCTIConnectorHelper, get_config_variable
from ptnad import PTNADClient


class PTNADConnector():
    def __init__(self) -> None:
        
        # Instantiate the connector helper from config
        config_file_path = os.path.dirname(os.path.abspath(__file__)) + "/config.yml"
        config = (
            yaml.load(open(config_file_path), Loader=yaml.FullLoader)
            if os.path.isfile(config_file_path)
            else {}
        )

        # Configuration
        self.helper = OpenCTIConnectorHelper(config)
        self.ptnad_url = get_config_variable("PTNAD_URL", ["ptnad", "url"], config)
        self.ptnad_ssl_verify = get_config_variable(
            "PTNAD_SSL_VERIFY", ["ptnad", "ssl_verify"], config, default=False
        )
        self.ptnad_ip_external_key = get_config_variable(
            "PTNAD_IP_EXTERNAL_KEY", ["ptnad", "ip_external_key"], config, default='opencti-ip'
        )
        self.ptnad_dn_external_key = get_config_variable(
            "PTNAD_DN_EXTERNAL_KEY", ["ptnad", "dn_external_key"], config, default='opencti-dn'
        )
        self.ptnad_uri_external_key = get_config_variable(
            "PTNAD_URI_EXTERNAL_KEY", ["ptnad", "url_external_key"], config, default='opencti-url'
        )
        self.ptnad_md5_external_key = get_config_variable(
            "PTNAD_MD5_EXTERNAL_KEY", ["ptnad", "md5_external_key"], config, default='opencti-md5'
        )
        self.ptnad_ip_replist_name = get_config_variable(
            "PTNAD_IP_REPLIST_NAME", ["ptnad", "ip_replist_name"], config, default='opencti-ip-replist'
        )
        self.ptnad_dn_replist_name = get_config_variable(
            "PTNAD_DN_REPLIST_NAME", ["ptnad", "dn_replist_name"], config, default='opencti-dn-replist'
        )
        self.ptnad_uri_replist_name = get_config_variable(
            "PTNAD_URL_REPLIST_NAME", ["ptnad", "url_replist_name"], config, default='opencti-url-replist'
        )
        self.ptnad_md5_replist_name = get_config_variable(
            "PTNAD_MD5_REPLIST_NAME", ["ptnad", "md5_replist_name"], config, default='opencti-md5-replist'
        )
        self.connector_scope = get_config_variable(
            "CONNECTOR_SCOPE", ["connector", "scope"], config, default='ip,dn,url,md5'
        ).replace(' ','').split(',')

        try:
            self.ptnad_token = get_config_variable(
            "PTNAD_TOKEN", ["ptnad", "token"], config
            )
        except Exception as ex:
            self.helper.connector_logger.warn(
                "Unable token initializate { "
                + str(ex)
                + " }"
            )
            
        try:
            self.ptnad_username = get_config_variable(
            "PTNAD_USERNAME", ["ptnad", "username"], config
            )
            self.ptnad_password = get_config_variable(
            "PTNAD_PASSWORD", ["ptnad", "password"], config
            )
        except Exception as ex:
            self.helper.connector_logger.warn(
                "Unable username or/and password initializate { "
                + str(ex)
                + " }"
            )

        # Initialize PT NAD client
        try:
            self.ptnad_client = PTNADClient(
                base_url=self.ptnad_url,
                verify_ssl=self.ptnad_ssl_verify
            )
            
            if hasattr(self, 'ptnad_username') and hasattr(self, 'ptnad_password'):
                self.ptnad_client.set_auth(
                    username=self.ptnad_username, 
                    password=self.ptnad_password
                )
            else:
                raise ValueError("Username and password are required for PT NAD authentication")
            
            self.ptnad_client.login()
                
        except Exception as ex:
            self.helper.connector_logger.error(
                "Unable to initialize PT NAD client { " + str(ex) + " }"
            )
            sys.exit(0)
        
        try:
            self._initialize_replists()
        except Exception as ex:
            self.helper.connector_logger.error(
                "Unable to initialize collection sets, shutting down { "
                + str(ex)
                + " }"
            )
            sys.exit(0)

    def _initialize_replists(self):
        
        data = self.ptnad_client.replists.get_all_lists()

        opencti_ip_replist_exist = False
        opencti_dn_replist_exist = False
        opencti_url_replist_exist = False
        opencti_md5_replist_exist = False

        if isinstance(data, dict) and 'results' in data:
            replists = data['results']
        elif isinstance(data, list):
            replists = data
        else:
            replists = []

        for replist in replists:
            if replist['external_key'] == self.ptnad_ip_external_key:
                opencti_ip_replist_exist = True
            if replist['external_key'] == self.ptnad_dn_external_key:
                opencti_dn_replist_exist = True
            if replist['external_key'] == self.ptnad_uri_external_key:
                opencti_url_replist_exist = True
            if replist['external_key'] == self.ptnad_md5_external_key:
                opencti_md5_replist_exist = True   

        # for i in self.connector_scope:
        if 'ip' in self.connector_scope and not opencti_ip_replist_exist:
            self.ptnad_client.replists.create_list(
                name=self.ptnad_ip_replist_name,
                type="ip",
                color="7",
                external_key=self.ptnad_ip_external_key
            )

        if 'dn' in self.connector_scope and not opencti_dn_replist_exist:
            self.ptnad_client.replists.create_list(
                name=self.ptnad_dn_replist_name,
                type="dn",
                color="7",
                external_key=self.ptnad_dn_external_key
            )

        if 'url' in self.connector_scope and not opencti_url_replist_exist:
            self.ptnad_client.replists.create_list(
                name=self.ptnad_uri_replist_name,
                type="uri",
                color="7",
                external_key=self.ptnad_uri_external_key
            )

        if 'md5' in self.connector_scope and not opencti_md5_replist_exist:
            self.ptnad_client.replists.create_list(
                name=self.ptnad_md5_replist_name,
                type="md5",
                color="7",
                external_key=self.ptnad_md5_external_key
            )
    

    def _create_indicator(self, indicator, type):
        
        match type:
            case 'ip':
                external_key = self.ptnad_ip_external_key
            case 'dn':
                external_key = self.ptnad_dn_external_key
            case 'md5':
                external_key = self.ptnad_md5_external_key
            case 'uri':
                external_key = self.ptnad_uri_external_key

        self.ptnad_client.replists.add_dynamic_list_item(
            external_key=external_key,
            value=indicator
        )


    def _delete_indicator(self, indicator, type):

        match type:
            case 'ip':
                external_key = self.ptnad_ip_external_key
            case 'dn':
                external_key = self.ptnad_dn_external_key
            case 'md5':
                external_key = self.ptnad_md5_external_key
            case 'uri':
                external_key = self.ptnad_uri_external_key

        self.ptnad_client.replists.remove_item(
            external_key=external_key,
            value=indicator
        )


    def _process_message(self, msg):
        try:
            data = json.loads(msg.data)["data"]
            
            if 'indicator' == data["type"]:
                if msg.event == 'create':
                    if 'file:hashes.MD5' in data['pattern'] and data['revoked'] == False:
                        self._create_indicator(data['pattern'].split('\'')[1], 'md5')
                    elif 'ipv4-addr:value' in data['pattern'] and data['revoked'] == False:
                        self._create_indicator(data['pattern'].split('\'')[1], 'ip')
                    elif 'domain-name:value' in data['pattern'] and data['revoked'] == False:
                        self._create_indicator(data['pattern'].split('\'')[1], 'dn')
                    elif 'url:value' in data['pattern'] and data['revoked'] == False:
                        self._create_indicator(data['pattern'].split('\'')[1], 'uri')
                elif msg.event == 'delete':
                    if 'file:hashes.MD5' in data['pattern']:
                        self._delete_indicator(data['pattern'].split('\'')[1], 'md5')
                    elif 'ipv4-addr:value' in data['pattern'] :
                        self._delete_indicator(data['pattern'].split('\'')[1], 'ip')
                    elif 'domain-name:value' in data['pattern']:
                        self._delete_indicator(data['pattern'].split('\'')[1], 'dn')
                    elif 'url:value' in data['pattern']:
                        self._delete_indicator(data['pattern'].split('\'')[1], 'uri')
                elif msg.event == "update":
                    if 'file:hashes.MD5' in data['pattern']:
                        if data['revoked'] == False:
                            self._create_indicator(data['pattern'].split('\'')[1], 'md5')
                        else:
                            self._delete_indicator(data['pattern'].split('\'')[1], 'md5')
                    elif 'ipv4-addr:value' in data['pattern']:
                        if data['revoked'] == False:
                            self._create_indicator(data['pattern'].split('\'')[1], 'ip')
                        else:
                            self._delete_indicator(data['pattern'].split('\'')[1], 'ip')
                    elif 'domain-name:value' in data['pattern']:
                        if data['revoked'] == False:
                            self._create_indicator(data['pattern'].split('\'')[1], 'dn')
                        else:
                            self._delete_indicator(data['pattern'].split('\'')[1], 'dn')
                    elif 'url:value' in data['pattern']:
                        if data['revoked'] == False:
                            self._create_indicator(data['pattern'].split('\'')[1], 'uri')
                        else:
                            self._delete_indicator(data['pattern'].split('\'')[1], 'uri')

        except Exception as ex:
            self.helper.connector_logger.error(
                "[Processing] Failed processing data { " + str(ex) + " }"
            )
            self.helper.connector_logger.error(
                "[Processing] Message data { " + str(msg) + " }"
            )
            return None

    def start(self):
        self.helper.listen_stream(self._process_message)


if __name__ == "__main__":
   
    try:
        connector = PTNADConnector()
        connector.start()
    except Exception as e:
        print(e)
        time.sleep(10)
        sys.exit(0)
