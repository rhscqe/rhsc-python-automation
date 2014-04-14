
Environment
------------
* RHS-C instance
* 2 RHS nodes
* rhsc-cli installed
* >= Python 2.6 

Config
------
in config/config.json, replace:
* rest.url with your RHS-C instance REST API url
* hosts[n].host

Run Tests
---------
```
pip install -r requirements.txt --allow-external argparse
nose2
```

To run with report engine:
```
export REPORT_ENGINE_PROPERTY_FILE=$( readlink -f reportengine.properties ) nose2 --reportengine 
```
