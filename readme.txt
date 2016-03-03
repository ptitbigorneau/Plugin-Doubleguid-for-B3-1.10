# doubleguid plugin
# Plugin for B3 (www.bigbrotherbot.net)
# www.ptitbigorneau.fr

doubleguid plugin (v1.3) for B3

Requirements
------------

* BigBortherBot(3) >= version 1.10

Installation:
-------------

1. Copy the 'doubleguid' folder into 'b3/extplugins' and 'doubleguid.ini' file into '/b3/extplugins/conf'.

2. Open your B3.ini or b3.xml file (default in b3/conf) and add the next line in the [plugins] section of the file:
    for b3.xml
        <plugin name="doubleguid" config="@b3/extplugins/conf/doubleguid.ini"/>
    for b3.ini
        doubleguid: @b3/extplugins/conf/doubleguid.ini
