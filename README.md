# VSSM
Vehicle Safety and Security Monitor

The VSSM is intended to provide additional means for a user to interact with their vehicle. The device uses a Raspberry Pi 3 B+ and several hardware modules to function as a GPS tracker while allowing the user to record video and upload data through voice commands. Eventually, the device will also be able to send SMS messages to emergency contacts.  

The VSSM is housed near the vehicle’s DLC in order to constantly maintain a connection. While the car is not running the UPS prevents battery drain by keeping the device from booting up. When the UPS detects a large voltage increase (13.1 V for 2 seconds), it is assumed to be the vehicle starting. This causes the UPS to send a startup signal to the Raspberry Pi 3 B+. Upon starting, a process is set to trigger the execution of a main driver program that manages our subprocesses. Firmware and basic drivers control most of the hardware initialization, including the data connection through the SixFab 4G Base Hat and Quectel EC25. This driver program initializes three subprocesses:

Voice: This process constantly parses audio detected by the Bluetooth microphone looking for spoken key phrases. These phrases allow the user to trigger video recordings, upload the latest recording to the website, and contact emergency services.

GPS: This process obtains the current location of the vehicle through the GPS dongle and then converts and uploads this data to the website and the related database. The website then uses the JavaScript Maps API to plot these points so users can follow the travel of the vehicle. This happens consistently while the vehicle is in operation.

OBD: This process attempts to pulls DTCs from the vehicle’s OBD-II port using most supported communication methods. Since a fully functioning vehicle may not have any codes stored the connection is proven by requesting and receiving a non-zero RPM measurement through this connection. Once this data is obtained, it is sent to the website and added to the related database.

Website: The website has two options on the landing page. The first is a date entry that will allow users to view that day’s travel locations as well as any DTCs triggered while driving. Second is a page listing all available videos that the user may download, sorted newest to oldest.

Once the user has arrived at their destination and turned the engine off, the VSSM will continue to operate until the battery drops to a specific level (11.5 V for 10 seconds). Once this occurs, the UPS sends a shutdown signal to the Pi.

References are included in the product design document. Some code was adapted from the Google Maps JavaScript API and the Vosk API examples. 
