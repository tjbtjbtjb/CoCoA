# -*- coding: utf-8 -*-

"""
Project : CoCoA
Date :    april-june 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
Copyright © CoCoa-team-17
License: See joint LICENSE file

Module : cocoa.world
About :

Provide simple quantitative information about countries in the worlds for normalisation purpuses of the CoCoA project.
The database in use is explicitly available throuh the getBaseUrl() method.
The EU and all continental country list have been added for CoCoa specific needs.

"""

import requests
import pandas


class WorldInfo:
    __pandasData = pandas.DataFrame()

    def __init__(self):
        self.__url = "https://www.worldometers.info/world-population/population-by-country/"
        htmlContent = requests.get(self.__url).content
        self.__pandasData = pandas.read_html(htmlContent)[
            0][['Country (or dependency)', 'Population (2020)', 'Land Area (Km²)','Density (P/Km²)']]
        self.__pandasData.columns = ['Country', 'Population', 'Area','Density']
        self.CountriesNamesUnified()

    def CountriesNamesUnified(self):
        ''' Change worldometers names countries to JohnsHopkins names ones'''
        self.__pandasData=self.__pandasData.replace('Congo','Congo (Brazzaville)')
        self.__pandasData=self.__pandasData.replace('DR Congo','Congo (Kinshasa)')
        self.__pandasData=self.__pandasData.replace('Côte d\'Ivoire','Cote d\'Ivoire')
        self.__pandasData=self.__pandasData.replace('South Korea','Korea, South')
        self.__pandasData=self.__pandasData.replace('Saint Kitts & Nevis','Saint Kitts and Nevis')
        self.__pandasData=self.__pandasData.replace('St. Vincent & Grenadines','Saint Vincent and the Grenadines')
        self.__pandasData=self.__pandasData.replace('United States','US')
        self.__pandasData=self.__pandasData.replace('Czech Republic (Czechia)', 'Czechia')

    def getBaseUrl(self):
        return self.__url

    def getData(self):
        return self.__pandasData

    def getEUCountries(self):
        country = ['Portugal', 'Spain', 'Ireland', 'United Kingdom', 'France', 'Italy', 'Germany', 'Belgium',
                   'Netherlands', 'Luxembourg', 'Austria', 'Denmark', 'Sweden', 'Finland',
                   'Estonia', 'Latvia', 'Lithuania', 'Poland', 'Slovakia', 'Hungary', 'Slovenia',
                   'Croatia', 'Romania', 'Bulgaria', 'Greece', 'Malta', 'Cyprus']
        return sorted(country)

    def getEuropeCountries(self):
        country = ['Andorra', 'Albania', 'Austria', 'Belgium', 'Bulgaria', 'Belarus','Czechia',
                   'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
                   'Ireland', 'Iceland', 'Italy', 'Liechtenstein', 'Lithuania',
                   'Luxembourg', 'Latvia', 'North Macedonia', 'Malta', 'Netherlands',
                   'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'Sweden', 'Slovenia',
                   'Slovakia', 'Ukraine', 'Bosnia and Herzegovina',
                   'Croatia', 'Moldova', 'Monaco', 'Montenegro', 'Serbia', 'Spain', 'Switzerland',
                   'United Kingdom']
        return sorted(country)

    def getAsiaCountries(self):
        country = ['Afghanistan', 'Armenia', 'Azerbaijan', 'Bangladesh', 'Bahrain', 'Brunei',
                   'Bhutan', 'China', 'Cyprus', 'Georgia', 'Indonesia', 'Israel',
                   'India', 'Iraq', 'Iran', 'Jordan', 'Japan', 'Kyrgyzstan', 'Korea, South',
                   'Kuwait', 'Lebanon', 'Mongolia', 'Maldives', 'Malaysia', 'Nepal', 'Oman',
                   'Philippines', 'Pakistan', 'Qatar', 'Saudi Arabia', 'Singapore', 'Syria', 'Thailand',
                   'Tajikistan', 'Turkey', 'Uzbekistan', 'Vietnam', 'Yemen', 'Cambodia',
                   'Timor-Leste', 'Kazakhstan', 'Laos', 'Sri Lanka', 'United Arab Emirates']
        return sorted(country)

    def getNorthAmericaCountries(self):
        country = ['Antigua and Barbuda', 'Barbados', 'Bahamas', 'Belize', 'Canada', 'Costa Rica', 'Cuba',
                   'Dominica', 'Dominican Republic', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico',
                   'Nicaragua', 'Panama', 'Trinidad and Tobago', 'US', 'El Salvador', 'Grenada',
                   'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines']
        return sorted(country)

    def getSouthAmericaCountries(self):
        country = ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Peru',
                   'Paraguay', 'Suriname', 'Uruguay', 'Venezuela']
        return sorted(country)

    def getAfricaCountries(self):
        country = ['Angola', 'Burkina Faso', 'Burundi', 'Benin', 'Botswana',
                   'Congo (Brazzaville)', 'Congo (Kinshasa)', 'Cote d\'Ivoire', 'Cameroon', 'Cabo Verde', 'Djibouti', 'Egypt',
                   'Eritrea', 'Ethiopia', 'Gabon', 'Ghana', 'Gambia', 'Guinea', 'Guinea-Bissau', 'Kenya',
                   'Liberia', 'Lesotho', 'Libya', 'Madagascar', 'Mali', 'Mauritania', 'Mauritius', 'Malawi', 'Mozambique',
                   'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Seychelles', 'Sudan', 'Sierra Leone', 'Senegal', 'Somalia',
                   'Togo', 'Tunisia', 'Tanzania', 'Uganda', 'Zambia', 'Zimbabwe', 'Algeria', 'Central African Republic',
                   'Chad', 'Comoros', 'Equatorial Guinea', 'Morocco', 'South Africa']
        return sorted(country)

    def getAllCountriesWorld(self):
        country =  self.getAfricaCountries() +  self.getSouthAmericaCountries() +\
        self.getNorthAmericaCountries() + self.getAsiaCountries() + self.getEuropeCountries()
        return sorted(country)


    def getAuvergneRhoneAlpes(self):
        department = ['01','03','07','15','26','38','42','43','63','69','73','74']
        name='Auvergne Rhone Alpes'
        return sorted(department),name

    def getBourgogneFrancheComte(self):
        department = ['21','25','39','58','70','71','89','90']
        name='Bourgogne Franche Comte'
        return sorted(department), name

    def getBretagne(self):
        department = ['22','29','35','56']
        name='Bretagne'
        return sorted(department),name

    def getCentreValdeLoire(self):
        department = ['18','28','36','37','41','45']
        name='Centre Val de Loire'
        return sorted(department),name

    def getCorse(self):
        department = ['2A','2B']
        name = 'Corse'
        return sorted(department),name

    def getGrandEst(self):
        department = ['08','51','52','54','55','57','67','68','88']
        name = 'Grand Est'
        return sorted(department),name

    def getHautsdeFrance(self):
        department = ['02','59','60','62','80']
        name = 'Hauts de France'
        return sorted(department),name

    def getIleDeFrance(self):
        department = ['75','77','78','91','92','93','94','95']
        name = 'Ile de France'
        return sorted(department),name

    def getCalvados(self):
        department = ['14','27','50','61','76']
        name='Calvados'
        return sorted(department),name

    def getNouvelleAquitaine(self):
        department = ['16','17','19','23','24','33','40','47','64','79','86','87']
        name='Nouvelle Aquitaine'
        return sorted(department),name

    def getOccitanie(self):
        department = ['09','11','12','30','31','32','34','46','48','65','66','81','82']
        name= 'Occitanie'
        return sorted(department),name

    def getPaysdelaLoire(self):
        department = ['44','49','53','72','85']
        name='Pays de la Loire'
        return sorted(department),name

    def getProvenceAlpesCotedAzur(self):
        department = ['04','05','06','13','83','84']
        name='Provence Alpes Cote d\' Azur'
        return sorted(department),name

    def getAllFranceDepartment(self):
        department = self.getAuvergneRhoneAlpes()[0] + self.getBourgogneFrancheComte()[0] + self.getBretagne()[0] + \
        self.getCentreValdeLoire()[0] + self.getCorse()[0] + self.getGrandEst()[0] + self.getHautsdeFrance()[0] + \
        self.getIleDeFrance()[0] + self.getCalvados()[0] + self.getNouvelleAquitaine()[0] + self.getOccitanie()[0] +\
        self.getPaysdelaLoire()[0] + self.getProvenceAlpesCotedAzur()[0]
        #dep , name = department
        return department

    def getAllFranceRegions(self):
        regions=[]
        department = [self.getAuvergneRhoneAlpes(),self.getBourgogneFrancheComte(),self.getBretagne() , \
        self.getCentreValdeLoire() , self.getCorse() , self.getGrandEst() ,self.getHautsdeFrance() , \
        self.getIleDeFrance() , self.getCalvados() , self.getNouvelleAquitaine() , self.getOccitanie() ,\
        self.getPaysdelaLoire() , self.getProvenceAlpesCotedAzur()]
        for i in department:
            regions.append(i)
        return regions

    def CountriesOver65yearsAbolute(self):
        df = pandas.read_html("https://en.wikipedia.org/wiki/List_of_countries_by_age_structure")[0]
        df.columns = [ '_'.join(x) for x in df.columns ]
        df=df.rename(columns={"Country_Country":"Country"})\
				 .rename(columns={"Population by age_age over 65 years[3]":"over65"})
        df['over65'] = list(map(lambda x: x[:-1], df['over65'].values))
        df['over65'] = df['over65'].astype(float)
        coun,over65,percentage=[],[],[]
        w=self.__pandasData
        for i in df['Country']:
            if w.loc[w['Country']==i,'Population'].empty or df.loc[df['Country']==i,'over65'].empty:
                val=-1
            else:
                val=(w.loc[w['Country']==i,'Population'].values*\
					df.loc[df['Country']==i,'over65'].values/100.	)[0]
            coun.append(i)
            over65.append(val)
            percentage.append(df.loc[df['Country']==i,'over65'].values[0])
        return pandas.DataFrame({'Country':coun,'Percentage':percentage,'PopulationOver65':over65})
