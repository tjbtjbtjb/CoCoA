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

Countries are named according to https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/ names. Caution.
"""
            
import requests
import pandas


class WorldInfo:
    __pandasData = pandas.DataFrame()

    def __init__(self):
        self.__url = "https://www.worldometers.info/world-population/population-by-country/"
        htmlContent = requests.get(self.__url).content
        self.__pandasData = pandas.read_html(htmlContent)[
            0][['Country (or dependency)', 'Population (2020)', 'Land Area (Km²)']]
        self.__pandasData.columns = ['Country', 'Population', 'Area']

    def getBaseUrl(self):
        return self.__url

    def getData(self):
        return self.__pandasData

    def getEUCountries(self):
        country = ['Portugal', 'Spain', 'Ireland', 'United Kingdom', 'France', 'Italy', 'Germany', 'Belgium',
                   'Netherlands', 'Luxembourg', 'Austria', 'Denmark', 'Sweden', 'Finland',
                   'Estonia', 'Latvia', 'Lithuania', 'Poland', 'Slovakia', 'Hungary', 'Slovenia',
                   'Croatia', 'Romania', 'Bulgaria', 'Greece', 'Malta', 'Cyprus','Czechia']
        return sorted(country)

    def getEuropeCountries(self):
        country = ['Andorra', 'Albania', 'Austria', 'Belgium', 'Bulgaria', 'Belarus',
                   'Germany', 'Denmark', 'Estonia', 'Finland', 'France', 'Greece', 'Hungary',
                   'Ireland', 'Iceland', 'Italy', 'Liechtenstein', 'Lithuania',
                   'Luxembourg', 'Latvia', 'North Macedonia', 'Malta', 'Netherlands',
                   'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'Sweden', 'Slovenia',
                   'Slovakia', 'Ukraine', 'Bosnia and Herzegovina',
                   'Croatia', 'Moldova', 'Monaco', 'Montenegro', 'Serbia', 'Spain', 'Switzerland',
                   'United Kingdom','Czechia','Kosovo','San Marino','Holy See']
        return sorted(country)

    def getAsiaCountries(self):
        country = ['Afghanistan', 'Armenia', 'Azerbaijan', 'Bangladesh', 'Bahrain', 'Brunei',
                   'Bhutan', 'China', 'Cyprus', 'Georgia', 'Indonesia','Israel',
                   'India', 'Iraq', 'Iran', 'Jordan', 'Japan', 'Kyrgyzstan', 'Korea, South',
                   'Kuwait', 'Lebanon', 'Mongolia', 'Maldives', 'Malaysia', 'Nepal', 'Oman',
                   'Philippines', 'Pakistan', 'Qatar', 'Saudi Arabia', 'Singapore', 'Syria', 'Thailand',
                   'Tajikistan', 'Turkey', 'Uzbekistan', 'Vietnam', 'Yemen', 'Cambodia',
                   'Timor-Leste', 'Kazakhstan', 'Laos', 'Sri Lanka', 'United Arab Emirates',
                   'Burma','Taiwan*','West Bank and Gaza','Western Sahara']
        return sorted(country)
        
    def getOceaniaCountries(self):
        country = ['Australia','New Zealand','Fiji','Papua New Guinea']
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
                   'Chad', 'Comoros', 'Equatorial Guinea', 'Morocco', 'South Africa','Eswatini',
                   'Sao Tome and Principe','South Sudan']
        return sorted(country)
        
    def getWorldCountries(self):
        country=self.getAfricaCountries() \
            + self.getSouthAmericaCountries() \
            + self.getNorthAmericaCountries() \
            + self.getOceaniaCountries() \
            + self.getAsiaCountries() \
            + self.getEuropeCountries()
        return sorted(country)
