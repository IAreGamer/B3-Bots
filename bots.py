# Copyright (C) 2008 Courgette
# Inspired by the spree plugin from Walker
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# 
#
# Changelog :
# 1.0.0 : initial release
# 1.1.0 : Some improvement of regul process


__version__ = '1.1.0'
__author__  = 'Beber888'


import b3, threading, time
import b3.plugin



    
#--------------------------------------------------------------------------------------------------
class BotsPlugin(b3.plugin.Plugin):
    
        NameBot1 = ''
        NameBot2 = ''
        NameBot3 = ''
        NameBot4 = ''
        NameBot5 = ''
        NameBot6 = ''
        NameBot7 = ''
        NameBot8 = ''
        ConfigBot1 = ''
        ConfigBot2 = ''
        ConfigBot3 = ''
        ConfigBot4 = ''
        ConfigBot5 = ''
        ConfigBot6 = ''
        ConfigBot7 = ''
        ConfigBot8 = ''

        CompteurErreur = 0

        NombreBot = 0
        NombreBot_Old = 0
        Difference_Bots = 0
        
        NombreJoueurReel = 0
        NombreJoueurReel_Old = 0
        Difference_Reel = 0
        
        NombreJoueurTotal = 0
        NombreJoueurTotal_Old = 0
        Difference_Total = 0

        min_level_kickbots_cmd = 0
        min_level_regul_cmd = 0
        Max_Bot = 0
        frequency_cycle = 30
        
        Demarrage = False      
        kick_bot = False
        Cde_Regul_Bots = True
        AnnuleCeCycle = False
        Perte_Synchro_B3_Rcon = False

        ListeNomBots = []
        ListeConfigBots = []

        

        
        def onLoadConfig(self):


                self.NameBot1 = self.config.get('settings', 'name_bot1')
                self.NameBot2 = self.config.get('settings', 'name_bot2')
                self.NameBot3 = self.config.get('settings', 'name_bot3')
                self.NameBot4 = self.config.get('settings', 'name_bot4')
                self.NameBot5 = self.config.get('settings', 'name_bot5')
                self.NameBot6 = self.config.get('settings', 'name_bot6')
                self.NameBot7 = self.config.get('settings', 'name_bot7')
                self.NameBot8 = self.config.get('settings', 'name_bot8')
                
                self.ConfigBot1 = self.config.get('settings', 'caracteristic_bot1')
                self.ConfigBot2 = self.config.get('settings', 'caracteristic_bot2')
                self.ConfigBot3 = self.config.get('settings', 'caracteristic_bot3')
                self.ConfigBot4 = self.config.get('settings', 'caracteristic_bot4')
                self.ConfigBot5 = self.config.get('settings', 'caracteristic_bot5')
                self.ConfigBot6 = self.config.get('settings', 'caracteristic_bot6')
                self.ConfigBot7 = self.config.get('settings', 'caracteristic_bot7')
                self.ConfigBot8 = self.config.get('settings', 'caracteristic_bot8')
                    
                self.Max_Bot = self.config.getint('settings', 'maximum_bot')
                self.min_level_kickbots_cmd = self.config.getint('settings', 'min_level_kickbots_cmd')
                self.min_level_regul_cmd = self.config.getint('settings', 'min_level_regul_cmd')
                self.frequency_cycle = self.config.getint('settings', 'frequency_cycle_in_seconds')

                        # get the plugin so we can register commands
                self._adminPlugin = self.console.getPlugin('admin')
                if not self._adminPlugin:
                    # something is wrong, can't start without admin plugin
                    self.error('Could not find admin plugin')
                else:
                    self._adminPlugin.registerCommand(self, 'kickbots', self.min_level_kickbots_cmd, self.KickAllBots, 'kb')
                    self._adminPlugin.registerCommand(self, 'regulbots', self.min_level_regul_cmd, self.Cde_RegulBots, 'rb')

        
        def onStartup(self):
                self.CycliqueCheck()
                self.ListeNomBots = [self.NameBot1, self.NameBot2, self.NameBot3, self.NameBot4, self.NameBot5, self.NameBot6, self.NameBot7, self.NameBot8]
                self.ListeConfigBots = [self.ConfigBot1, self.ConfigBot2, self.ConfigBot3, self.ConfigBot4, self.ConfigBot5, self.ConfigBot6, self.ConfigBot7, self.ConfigBot8]
                self.Demarrage = True
                        

        def CycliqueCheck(self):
                self.TempoCheck = threading.Timer(self.frequency_cycle, self.RegulBots)
                self.TempoCheck.start()

        def RegulBots(self):
                
                # Lecture nombre de joueurs par Rcon
                Reponse = self.console.write('players')
                for line in Reponse.split('\n'):
                        if 'Players:' in line:
                                Tableau = line.split(' ')
                                self.NombreJoueurTotal = int(Tableau[1])

                # Au demarrage les joueurs present sont des humains, ajout du nombre de bot manquant
                if self.Demarrage == True:
                        self.NombreJoueurReel =  self.NombreJoueurTotal
                        self.NombreJoueurReel_Old =  self.NombreJoueurTotal
                        self.NombreJoueurTotal_Old =  self.NombreJoueurTotal
                        self.verbose('Nombre joueur reel au depart : %s' %self.NombreJoueurReel)

                        # Ajout des bots si moins du nombre maximum de bots
                        if self.NombreJoueurTotal < self.Max_Bot :
                                self.AddBots(1, self.Max_Bot - self.NombreJoueurTotal)
                        self.Demarrage = False
                                
                        
                
                # Si commande de regul a ON
                if self.Cde_Regul_Bots == True:

                        
                        self.Difference_Total = self.NombreJoueurTotal - self.NombreJoueurTotal_Old

                        # Calcul du nombre exact de joueur de chaque categorie (Bots, Humain)
                        clist = self.console.clients.getClientsByLevel(0)
                        ListeBotsPresents = []
                        if len(clist) > 0:
                                self.NombreBot = 0
                                self.NombreJoueurReel = 0
                                self.AnnuleCeCycle = False
                                for c in clist:
                                        if 'BOT' in c.guid:
                                                self.NombreBot = self.NombreBot + 1
                                                ListeBotsPresents.append(c.name)
                                                if c.name not in self.ListeNomBots:
                                                        self.debug('Bot already present : Kick %s' % c.name)
                                                        self.console.write('kick %s' % c.cid)
                                                        self.kick_bot = True
                                                        self.AnnuleCeCycle = True
                                        if 'BOT' not in c.guid:
                                                self.NombreJoueurReel = self.NombreJoueurReel + 1
                         
                        # Calcul de la variation du nombre de joueurs
                        if self.Difference_Total != 0 or self.NombreBot != self.NombreBot_Old or self.NombreJoueurReel != self.NombreJoueurReel_Old:
                                self.verbose('Variation nombre de joueurs: %s' % self.Difference_Total)
                                self.verbose('Re-Calcul : Nb Bots: %s, Nb Humain: %s' % (self.NombreBot, self.NombreJoueurReel))
                         
                                # Arret du traitement si incoherance entre liste joueurs B3 et liste joueur /rcon player
                                if len(clist) != self.NombreJoueurTotal:
                                        self.Perte_Synchro_B3_Rcon = True
                                        self.debug('Difference number players beetween B3 (%s) and server (%s) : regulation STOPPED' %(len(clist), self.NombreJoueurTotal))

                                # Traitement si aucune incoherance entre liste joueurs B3 et liste joueur /rcon player
                                if len(clist) == self.NombreJoueurTotal and self.AnnuleCeCycle == False:
                                        self.Perte_Synchro_B3_Rcon = False
                                        self.NombreJoueurTotal_Old = self.NombreJoueurTotal

                                        if (self.NombreJoueurTotal == self.Max_Bot) or (self.NombreJoueurTotal > self.Max_Bot and self.NombreBot == 0):
                                                self.CompteurErreur = 0

                                        # Calcul variation du nombre de bot
                                        self.Difference_Bots = self.NombreBot - self.NombreBot_Old

                                        # Variation du nombre de bot
                                        if self.Difference_Bots != 0:

                                                # Ajout bot, mise a jour variables
                                                if self.Difference_Bots > 0:
                                                        self.verbose('Bot en +: %s' % self.Difference_Bots)
                                                        self.NombreBot_Old = self.NombreBot
                                                        
                                                # Perte bot, mise a jour variables                
                                                elif self.Difference_Bots < 0:
                                                        self.verbose('Bot en -: %s' % -self.Difference_Bots)
                                                        # Perte bot sans kick (decrochage du serveur?) 
                                                        if self.kick_bot == False:
                                                                a = 0
                                                                i = 0
                                                                self.debug('Loss of %s bots' % -self.Difference_Bots)
                                                                        
                                                                # Perte bot sans kick, rajout des bots disparus
                                                                while a <= self.Max_Bot:
                                                                        if self.ListeNomBots[a] not in ListeBotsPresents:
                                                                                self.console.write('addbot %s %s' % (self.ListeConfigBots[a], self.ListeNomBots[a]))
                                                                                self.debug('Added %s because of bots loss' % self.ListeNomBots[a])
                                                                                ListeBotsPresents.append(self.ListeNomBots[a])
                                                                                i = i + 1
                                                                                if i == -self.Difference_Bots:
                                                                                        a = self.Max_Bot
                                                                        a = a + 1

                                                        self.kick_bot = False
                                                        self.NombreBot_Old = self.NombreBot   
                                                

                                        # Calcul variation du nombre d humain
                                        self.Difference_Reel = self.NombreJoueurReel - self.NombreJoueurReel_Old

                                        # Variation du nombre d humain
                                        if self.Difference_Reel != 0:

                                                # Ajout humain, suppression bot
                                                if self.Difference_Reel > 0:
                                                        self.verbose('Humain en +: %s' % self.Difference_Reel)
                                                        self.NombreJoueurReel_Old = self.NombreJoueurReel
                                                        if self.NombreBot != 0:
                                                                DebutASupprimer = self.NombreBot - self.Difference_Reel + 1
                                                                if DebutASupprimer < 1:
                                                                        DebutASupprimer = 1
                                                                self.SupprBots(DebutASupprimer, self.Difference_Reel)
                                                                
                                                        
                                                # Perte humain, ajout bot                
                                                elif self.Difference_Reel < 0:
                                                        self.verbose('Humain en -: %s' % self.Difference_Reel)
                                                        self.NombreJoueurReel_Old = self.NombreJoueurReel
                                                        if self.NombreJoueurTotal < self.Max_Bot:
                                                                self.AddBots(self.NombreBot + 1, -self.Difference_Reel)
                                                        


                                                        
                        # Control de la regul < au nombre de bot max
                        if self.NombreJoueurTotal < self.Max_Bot and self.Perte_Synchro_B3_Rcon == False:
                                self.CompteurErreur = self.CompteurErreur + 1
                                if self.CompteurErreur > 4:
                                        self.verbose('Regulation a %s joueurs (%s Bots, %s Humains)' % (self.NombreJoueurTotal, self.NombreBot, self.NombreJoueurReel))
                                        a = 0
                                        i = 0                         
                                        # Ajout des bots manquants
                                        while a <= self.Max_Bot:
                                                if self.ListeNomBots[a] not in ListeBotsPresents:
                                                        self.console.write('addbot %s %s' % (self.ListeConfigBots[a], self.ListeNomBots[a]))
                                                        self.verbose('Ajout %s suite probleme/arret de regul' % self.ListeNomBots[a])
                                                        ListeBotsPresents.append(self.ListeNomBots[a])
                                                        i = i + 1
                                                        if i == self.Max_Bot - self.NombreJoueurTotal:
                                                                a = self.Max_Bot
                                                a = a + 1

                        # Control de la regul > au nombre de bot max
                        if self.NombreJoueurTotal > self.Max_Bot and self.NombreBot != 0 and self.Perte_Synchro_B3_Rcon == False:
                                self.CompteurErreur = self.CompteurErreur + 1
                                if self.CompteurErreur > 4:
                                        self.verbose('Regulation a %s joueurs (%s Bots, %s Humains)' % (self.NombreJoueurTotal, self.NombreBot, self.NombreJoueurReel))
                                        self.SupprBots(1 , self.Max_Bot)
         
 
 
                self.CycliqueCheck()



        def AddBots (self, Depart, NbBots) :

                
                        self.verbose('Bots : Ajout %s bots a partir du N%s' % (NbBots, Depart))
                        if Depart == 1:
                                if NbBots >= 1 :  
                                        self.console.write('addbot %s %s' % (self.ConfigBot1, self.NameBot1))
                                if NbBots >= 2:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot2, self.NameBot2))
                                if NbBots >= 3:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot3, self.NameBot3))
                                if NbBots >= 4:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot4, self.NameBot4))
                                if NbBots >= 5:
                                        self.console.write('addbot %s %s' % (self.ConfigBot5, self.NameBot5))
                                if NbBots >= 6:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot6, self.NameBot6))
                                if NbBots >= 7:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot7, self.NameBot7))
                                if NbBots == 8:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot8, self.NameBot8))

                        if Depart == 2:
                                if NbBots >= 1:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot2, self.NameBot2))
                                if NbBots >= 2:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot3, self.NameBot3))
                                if NbBots >= 3:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot4, self.NameBot4))
                                if NbBots >= 4:
                                        self.console.write('addbot %s %s' % (self.ConfigBot5, self.NameBot5))
                                if NbBots >= 5:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot6, self.NameBot6))
                                if NbBots >= 6:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot7, self.NameBot7))
                                if NbBots == 7:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot8, self.NameBot8))

                        if Depart == 3:
                                if NbBots >= 1:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot3, self.NameBot3))
                                if NbBots >= 2:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot4, self.NameBot4))
                                if NbBots >= 3:
                                        self.console.write('addbot %s %s' % (self.ConfigBot5, self.NameBot5))
                                if NbBots >= 4:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot6, self.NameBot6))
                                if NbBots >= 5:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot7, self.NameBot7))
                                if NbBots == 6:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot8, self.NameBot8))

                        if Depart == 4:
                                if NbBots >= 1:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot4, self.NameBot4))
                                if NbBots >= 2:
                                        self.console.write('addbot %s %s' % (self.ConfigBot5, self.NameBot5))
                                if NbBots >= 3:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot6, self.NameBot6))
                                if NbBots >= 4:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot7, self.NameBot7))
                                if NbBots == 5:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot8, self.NameBot8))

                        if Depart == 5:
                                if NbBots >= 1:
                                        self.console.write('addbot %s %s' % (self.ConfigBot5, self.NameBot5))
                                if NbBots >= 2:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot6, self.NameBot6))
                                if NbBots >= 3:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot7, self.NameBot7))
                                if NbBots == 4:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot8, self.NameBot8))

                        if Depart == 6:
                                if NbBots >= 1:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot6, self.NameBot6))
                                if NbBots >= 2:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot7, self.NameBot7))
                                if NbBots == 3:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot8, self.NameBot8))          

                        if Depart == 7:
                                if NbBots >= 1:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot7, self.NameBot7))
                                if NbBots == 2:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot8, self.NameBot8))

                        if Depart == 8:
                                if NbBots == 1:  
                                        self.console.write('addbot %s %s' % (self.ConfigBot8, self.NameBot8))



                         
        def SupprBots (self, Depart, NbBots):
                
                        self.verbose('Bots : Suppr %s bots a partir du N%s' % (NbBots, Depart))
                        self.kick_bot = True
                        if Depart == 8:
                                if NbBots == 1:  
                                        self.console.write('kick %s' % self.NameBot8)

                        if Depart == 7:
                                if NbBots >= 1:  
                                        self.console.write('kick %s' % self.NameBot7)
                                if NbBots == 2:  
                                        self.console.write('kick %s' % self.NameBot8)

                        if Depart == 6:
                                if NbBots >= 1:  
                                        self.console.write('kick %s' % self.NameBot6)
                                if NbBots >= 2:  
                                        self.console.write('kick %s' % self.NameBot7)
                                if NbBots == 3:  
                                        self.console.write('kick %s' % self.NameBot8)


                        if Depart == 5:

                                if NbBots >= 1:  
                                        self.console.write('kick %s' % self.NameBot5)
                                if NbBots >= 2:  
                                        self.console.write('kick %s' % self.NameBot6)
                                if NbBots >= 3:  
                                        self.console.write('kick %s' % self.NameBot7)
                                if NbBots == 4:  
                                        self.console.write('kick %s' % self.NameBot8)


                        if Depart == 4:
                                if NbBots >= 1:  
                                        self.console.write('kick %s' % self.NameBot4)
                                if NbBots >= 2:  
                                        self.console.write('kick %s' % self.NameBot5)
                                if NbBots >= 3:  
                                        self.console.write('kick %s' % self.NameBot6)
                                if NbBots >= 4:  
                                        self.console.write('kick %s' % self.NameBot7)
                                if NbBots == 5:  
                                        self.console.write('kick %s' % self.NameBot8)

 

                        if Depart == 3:
                                if NbBots >= 1:  
                                        self.console.write('kick %s' % self.NameBot3)
                                if NbBots >= 2:  
                                        self.console.write('kick %s' % self.NameBot4)
                                if NbBots >= 3:  
                                        self.console.write('kick %s' % self.NameBot5)
                                if NbBots >= 4:  
                                        self.console.write('kick %s' % self.NameBot6)
                                if NbBots >= 5:  
                                        self.console.write('kick %s' % self.NameBot7)
                                if NbBots == 6:  
                                        self.console.write('kick %s' % self.NameBot8)


                        if Depart == 2:
                                if NbBots >= 1:  
                                        self.console.write('kick %s' % self.NameBot2)
                                if NbBots >= 2:  
                                        self.console.write('kick %s' % self.NameBot3)
                                if NbBots >= 3:  
                                        self.console.write('kick %s' % self.NameBot4)
                                if NbBots >= 4:  
                                        self.console.write('kick %s' % self.NameBot5)
                                if NbBots >= 5:  
                                        self.console.write('kick %s' % self.NameBot6)
                                if NbBots >= 6:  
                                        self.console.write('kick %s' % self.NameBot7)
                                if NbBots == 7:  
                                        self.console.write('kick %s' % self.NameBot8)



                        if Depart == 1:
                                if NbBots >= 1:  
                                        self.console.write('kick %s' % self.NameBot1)
                                if NbBots >= 2:  
                                        self.console.write('kick %s' % self.NameBot2)
                                if NbBots >= 3:  
                                        self.console.write('kick %s' % self.NameBot3)
                                if NbBots >= 4:  
                                        self.console.write('kick %s' % self.NameBot4)
                                if NbBots >= 5:  
                                        self.console.write('kick %s' % self.NameBot5)
                                if NbBots >= 6:  
                                        self.console.write('kick %s' % self.NameBot6)
                                if NbBots >= 7:  
                                        self.console.write('kick %s' % self.NameBot7)
                                if NbBots == 8:  
                                        self.console.write('kick %s' % self.NameBot8)


                        self.kick_bot = True


        def KickAllBots (self, data, client, cmd=None):
                """\
                Kick all the bots of the server
                """
                # Kick de tous les bots present sur le serveur
                if client is not None:
                        client.message('^7Kick de tous les bots, Regul : ^1OFF')
                self.Cde_Regul_Bots = False
                self.SupprBots(1, self.Max_Bot)
                            

        def Cde_RegulBots (self, data, client, cmd=None):
                """\
                [ON / OFF] - Allow the regulation of bots
                """
                # Marche Arret du cyclique de regulation de bots
                if data == 'ON' or data == 'on':
                        if client is not None:
                                client.message('^7Regul des bots : ^2ON')
                                self.Cde_Regul_Bots = True


                if data == 'OFF' or data == 'off':
                        if client is not None:
                                client.message('^7Regul des bots : ^1OFF')
                                self.Cde_Regul_Bots = False


                        
                











                

