
import sys
from datParser import DATParser
from AMMMGlobals import AMMMException
from ValidateConfig import ValidateConfig
from InstanceGenerator import InstanceGenerator

def run():
    try:
        configFile = "C:/Users/Utilisateur/OneDrive/Documents/cours_20242025/AMMM/final_project/InstanceGeneratorProject/config/config.dat"
        print("Instance Generator")
        print("-----------------------")
        print("Reading Config file %s..." % configFile)
        config = DATParser.parse(configFile)
        ValidateConfig.validate(config)
        print("Creating Instances...")
        instGen = InstanceGenerator(config)
        instGen.generate()
        print("Done")
        return 0
    except AMMMException as e:
        print("Exception: %s", e)
        return 1

if __name__ == '__main__':
    sys.exit(run())
