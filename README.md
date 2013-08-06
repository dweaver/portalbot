PTL! Automated Portals Widget Development
-----------------------------------------

PTL fires up a browser and uploads widget code to Portals. Modify the domain css and/or widget js files on your PC, then run ptl to upload them into your portal. It even presses the "Execute Javascript" button for you.

*Installation*

```bash

    $ pip install -r requirements.txt
```

*Usage*

```bash

    $ ./ptl.py -h

ptl - Portals Utility - update widget js and domain css

Usage:
    ptl upload [options] --domain=<domain> --user=<user> [--pass=<pass>] [--widgetjs=<file> --portal=<id> --dashboard=<id> --widget=<id>] [--domaincss=<file>]
    
    If --pass is omitted, ptl fills in your username and gives you 60 seconds to enter your password. Don't dawdle!

    portal and dashboard ids can be taken from the dashboard url: /view/<portal>/<dashboard>

    widget id requires inspecting the DOM. In Chrome, right click on the down arrow on the top right
    in the widget and select Inspect Element. The id is from the id of that element, e.g. if
    you see <img id="menuicon1" ... the widget id is 1.

Options:
    -h --help     Show this screen
    -v --version  Show version
```

Example:

```bash

    $ ptl/ptl.py upload --domain=mydomain --user=myname@company.com --pass=mypassword --domaincss=domain.css --widgetjs=mywidget.js --portal=1219686468 --dashboard=1297260819 --widget=1
```
