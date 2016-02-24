###################################################################################
#
# BotsPlugin
# Plugin for B3 (www.bigbrotherbot.com)
# (c) 2006 www.xlr8or.com (mailto:xlr8or@xlr8or.com)
#
# This program is free software and licensed under the terms of
# the GNU General Public License (GPL), version 2.
#
# http://www.gnu.org/copyleft/gpl.html
###################################################################################

BotsPlugin (v1.0.0) for B3
###################################################################################

This plugin works for 4.1 only!
This plugin add and remove bot from server


Added Commands:
!kickbots (!kb) - kick all bots and stop the process regul
!regulbots (!rb) <on/off> - Run/Stop of the process regul (no bots add and remove)

Each command can be leveled in the config file.

maximumbot:
Set the number max of bots on the server (max is 8)

FrequencyCycle:
In second, it's the time between two checks


Requirements:
###################################################################################

- ioUrT
- B3 version 1.1.3 or higher


Installation of the B3 plugin:
###################################################################################

To install the b3-plugin part:

1. Unzip the contents of this package. Go to the unzipped folder extplugins and
place the .py file in the bots folder b3/extplugins and the config file .xml in
the b3/extplugins/conf folder.

2. Open the .xml file with your favorit editor and modify the
levels if you want them different. Do not edit the command-names
for they will not function under a different name.

3. Open your B3.xml file (in b3/conf) and add the next line in the
<plugins> section of the file:

<plugin name="bots" priority="31" config="@b3/extplugins/conf/bots.xml"/>

The numer 31 in this just an example. Make sure it fits your
plugin list.

Important!
###################################################################################
For having no problem, once your bots are connected to the server, put them in a high
 level (like admin) for they are not kick by the bot for tk.

If you used poweradminurt, enabled the bot in the poweradminurt.xml :
<set name="bot_enable">True</set>
and choose zero bot :
<set name="bot_minplayers">0</set>

In the server.cfg, set bot_enabled = 1



Configuration!
###################################################################################
How to set a bot :
for exemple in the console : /rcon addbot python 3 blue 110 toto
in the xml :
		<set name="name_bot3">toto</set>
		<set name="caracteristic_bot3">python 3 blue 110</set>

python is the type of bot (with definite weapons)
3 is the level (0 is bad 5 is god)
blue/red is the team
110 is the ping of the bot
toto is the name

Alternate blue and red for having teams balanced (ex bot1 red, bot2 blue...)

Detail of type of bot in UrT!
###################################################################################
    Name: Boa				Name: Cheetah
    Primary: ZM LR300 ML		Primary: Kalashnikov AK103
    Secondary: H&K MP5K			Secondary: Franchi SPAS-12
    Sidearm: .50 Desert Eagle		Sidearm: .50 Desert Eagle
    Grenades: HE Grenades		Grenades: HE Grenades
    Item 1: Kevlar Vest			Item 1: Kevlar Vest
    Item 2: -				Item 2: -
    Item 3: -				Item 3: -

    Name: Chicken				Name: Cobra 
    Primary: H&K G36			Primary: ZM LR300 ML
    Secondary: H&K MP5K			Secondary: H&K MP5K
    Sidearm: .50 Desert Eagle		Sidearm: .50 Desert Eagle
    Grenades: HE Grenades		Grenades: Smoke Grenades
    Item 1: Kevlar Vest			Item 1: Kevlar Vest
    Item 2: -				Item 2: -
    Item 3: -				Item 3: -

    Name: Cockroach			Name: Cougar
    Primary: H&K UMP45			Primary: H&K G36
    Secondary: -				Secondary: -
    Sidearm: Beretta 92G		Sidearm: Beretta 92G
    Grenades: Flash Grenades		Grenades: Flash Grenades
    Item 1: Kevlar Vest			Item 1: Silencer
    Item 2: -				Item 2: Kevlar Vest
    Item 3: -				Item 3: -

    Name: Goose				Name: Mantis
    Primary: H&K 69			Primary: ZM LR300 ML
    Secondary: H&K UMP45		Secondary: -
    Sidearm: .50 Desert Eagle		Sidearm: Beretta 92G
    Grenades: -				Grenades: -
    Item 1: Extra Ammo			Item 1: Laser Sight
    Item 2: Kevlar Vest			Item 2: Silencer
    Item 3: -				Item 3: Kevlar Vest

    Name: Penguin				Name: Puma
    Primary: ZM LR300 ML		Primary: ZM LR300 ML
    Secondary: -				Secondary: -
    Sidearm: .50 Desert Eagle		Sidearm: Beretta 92G
    Grenades: -				Grenades: -
    Item 1: Laser Sight			Item 1: Laser Sight
    Item 2: Silencer			Item 2: Silencer
    Item 3: Kevlar Vest			Item 3: Kevlar Vest

    Name: Python				Name: Raven
    Primary: H&K G36			Primary: H&K PSG-1
    Secondary: Franchi SPAS-12	Secondary: H&K MP5K
    Sidearm: .50 Desert Eagle		Sidearm: .50 Desert Eagle
    Grenades: HE Grenades		Grenades: -
    Item 1: Kevlar Vest			Item 1: Kevlar Vest
    Item 2: -				Item 2: Silencer
    Item 3: -				Item 3: -

    Name: Scarab				Name: Scorpion
    Primary: H&K G36			Primary: Remington SR8
    Secondary: H&K MP5K			Secondary: H&K MP5K
    Sidearm: .50 Desert Eagle		Sidearm: Beretta 92G
    Grenades: -				Grenades: HE Grenades
    Item 1: Kevlar Vest			Item 1: Kevlar Vest
    Item 2: Silencer			Item 2: -
    Item 3: -				Item 3: -

    Name: Tiger				Name: Widow
    Primary: Kalashnikov AK103	Primary: ZM LR300 ML
    Secondary: -				Secondary: H&K MP5K
    Sidearm: Beretta 92G		Sidearm: Beretta 92G
    Grenades: HE Grenades		Grenades: -
    Item 1: Medkit			Item 1: Kevlar Vest
    Item 2: Kevlar Vest			Item 2: Laser Sight
    Item 3: -				Item 3: -


Whant bot more intelligent who can capture flags ?
###################################################################################

Add "ut4_urbotpack_v0.1.13_.pk3" in q3ut4 folder, restart the server and you can add 5 new personnality.

    Name: Commando			Name: Soldier
    Primary: ZM LR300 ML		Primary: Kalashnikov AK103
    Secondary: -				Secondary: H&K MP5K
    Sidearm: Beretta 92G		Sidearm: .50 Desert Eagle
    Grenades: -				Grenades: -
    Item 1: Kevlar Vest			Item 1: Kevlar Vest
    Item 2: Laser Sight			Item 2: Helmet
    Item 3: Silencer			Item 3: -

    Name: Trooper				Name: Guard
    Primary: ZM LR300 ML		Primary: Kalashnikov AK103
    Secondary: Franchi SPAS-12	Secondary: H&K UMP45
    Sidearm: .50 Desert Eagle		Sidearm: Beretta 92G
    Grenades: -				Grenades: -
    Item 1: Kevlar Vest			Item 1: Kevlar Vest
    Item 2: Laser Sight			Item 2: Helmet
    Item 3: -				Item 3: -

    Name: Sharpshooter
    Primary: H&K G36
    Secondary: -
    Sidearm: Beretta 92G
    Grenades: -
    Item 1: Kevlar Vest
    Item 2: Helmet
    Item 3: Silencer

Changelog
###################################################################################
 
v1.0.0         : Initial release. 

###################################################################################
Beber888 - 06 november 2010 - www.bigbrotherbot.com

