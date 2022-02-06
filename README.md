# Badsender
Send your log from Valhala or Artillery honeypots to your intel inbox

## Usage

_Windows (Server 2016 & Server 2019) & Linux compatible._

* Configure and launch your honeypot
* Rename **data_template.py** to **data.py**
* Put your SMPT and log info into **data.py**
* Select a time interval (in seconds)
* Input your password when prompted
* Get your intel and hunt'em all

## Example

```
python3.exe .\badsender.py valhala "C:\valhala\" 10800
```