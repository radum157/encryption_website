##### Steganographic website - Marin Radu
# README

## View as webpage
```
sudo pip3 install grip
grip  README.md
# open http://localhost:6419/
```

## About the website

**Jinja2** templates were used alongside **Flask**, **HTML** and **CSS** (with **Bootstrap**). As the homepage might suggest, the site implements a simple `steganographic` application. Not much can be said about it. The design was kept simple, following the example of a previously developed app, at least from a `styling` point of view. The HTML part consists of nothing more than a few paragraphs along with two input `forms`.

On the server side, everything was straight forward: receive a file, perform an *encryption* or *decryption* using it, save it then return the requested values. The encryption / decryption was done as such: every 3 pixel's *least significant bits* stored one letter of the message. **Note** that an arbitrary terminator was used to mark the end of the message, so any images not respecting this rule cannot be deciphered.

Further details can be found inside the source files (through comments, variable names etc). A `Dockerfile` was also provided for ease of deployment.
