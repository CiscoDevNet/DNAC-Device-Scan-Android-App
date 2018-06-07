# DNAC Device Scan Android App


### Description
This project is an Andriod app that scans a device's Serial Number and provides insights into the device. It also has a middleware app that is the interface to a DNA Center instance. 

### Possible Application Scenarios
1. A network operator will be able to quickly identify a device by its inventory information without having to loggging into its terminal or a management station that might manage it.
2. The user will know the sync status of the device and the DNA Center.

### Install and Setup
* Frontend Mobile App
1. Install nodejs and npm
2. Install ionic using: https://ccoenraets.github.io/ionic-tutorial/install-ionic.html
3. Add android platform support:
  `ionic cordova add platform android`
  
4. Compile 

      `cd frontend/devScan/`
  
      `npm install`
  
      `ionic cordova build android --debug`
  
  
* Middleware installation
1. Create a python virtualenv and activate it
2. Install requirements

      `pip install -r requirements.txt`
      

* Running the middleware
1.  Setup local environment variables for your DNA Center in the file middleware/dnac_instance.conf.  *Provide the info for your DNA Center*

2. Update host-IP on line #27 of middleware/app.py
3. Start the server

    `python middleware/app.py`
    
    
### Using The Application
1.  Open the Android app and provide the middleware host-IP on the onboarding screen
2.  Scan the serial number of a device 
