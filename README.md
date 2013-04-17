To run with report engine:
    export REPORT_ENGINE_PROPERTY_FILE=$( readlink -f reportengine.properties )
    nose2 --reportengine 
