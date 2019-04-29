import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
from Utilities import Utilities
import io
import sys
import os


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


util = Utilities()

class SnipsConfigParser(configparser.ConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.read_file(f)
            #conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()
      
def subscribe_intent_hello(hermes, intentMessage):
    sayMessage = "How are you doing"
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)
    
def subscribe_intent_fine(hermes, intentMessage):
    sayMessage = "Excellent!, by the way I'm the best!"
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)
    
def subscribe_intent_bye(hermes, intentMessage):
    sayMessage = "Bye then, this is awkward"
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)

def subscribe_intent_lastGlu(hermes, intentMessage):
    sayMessage = "Your Glucose level was: 94 milimiters per deciliter"
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)

def subscribe_intent_newGlu(hermes, intentMessage):
    sayMessage = "Allright, tell me your new measurement."
    
    current_session_id = intentMessage.session_id
    hermes.publish_continue_session(current_session_id, sayMessage, ["&KV4lavkZXDmNqwJXKn6Mxmx6W1jegAM6Oyr2o1PE:gluData"])

def subscribe_intent_gluData(hermes, intentMessage):
    sayMessage = "Okay, it is now logged." 
    # The number will be logged via the command center
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)

def subscribe_intent_newHeart(hermes, intentMessage):
    sayMessage = "Excellent!, put your finger on the device for slot seconds starting NOW!"
    #The max30100 will send a publish to the command centre with this this info and will be sorted here.
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)

def subscribe_intent_lastHeart(hermes, intentMessage):
    sayMessage = "Your heart rate was 74 beats per minute"
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)

def subscribe_intent_historicData(hermes, intentMessage):
    #again glunumber should be provided by an MQTT publish from the command centre, this is just for example purposes
   
 
    sayMessage = "Staying at a healthy weight can help you prevent and manage problems like prediabetes, type 2 diabetes, heart disease, high blood pressure and unhealthy cholesterol. Keep at it you are doing great. Try not to smoke and do contant exercise!"    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)
    
def subscribe_intent_Help(hermes, intentMessage):
    #again glunumber should be provided by an MQTT publish from the command centre, this is just for example purposes
   
 
    sayMessage = "Your request has been sent, the nurse will be here right away"    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)



if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("&KV4lavkZXDmNqwJXKn6Mxmx6W1jegAM6Oyr2o1PE:hello",       subscribe_intent_hello) \
            .subscribe_intent("&KV4lavkZXDmNqwJXKn6Mxmx6W1jegAM6Oyr2o1PE:bye",       subscribe_intent_bye) \
            .subscribe_intent("&KV4lavkZXDmNqwJXKn6Mxmx6W1jegAM6Oyr2o1PE:fineYes",         subscribe_intent_fine) \
            .subscribe_intent("&KV4lavkZXDmNqwJXKn6Mxmx6W1jegAM6Oyr2o1PE:lastGlu",         subscribe_intent_lastGlu) \
            .subscribe_intent("&KV4lavkZXDmNqwJXKn6Mxmx6W1jegAM6Oyr2o1PE:newGlu",         subscribe_intent_newGlu) \
            .subscribe_intent("&KV4lavkZXDmNqwJXKn6Mxmx6W1jegAM6Oyr2o1PE:gluData",         subscribe_intent_gluData) \
            .subscribe_intent("&KV4lavkZXDmNqwJXKn6Mxmx6W1jegAM6Oyr2o1PE:newHeart",         subscribe_intent_newHeart) \
            .subscribe_intent("&KV4lavkZXDmNqwJXKn6Mxmx6W1jegAM6Oyr2o1PE:lastHeart",         subscribe_intent_lastHeart) \
            .subscribe_intent("&KV4lavkZXDmNqwJXKn6Mxmx6W1jegAM6Oyr2o1PE:historicData",         subscribe_intent_historicData) \
            .subscribe_intent("&KV4lavkZXDmNqwJXKn6Mxmx6W1jegAM6Oyr2o1PE:Help",         subscribe_intent_Help) \
            .loop_forever()
