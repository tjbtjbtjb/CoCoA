![CoCoA Logo](/misc/cocoa_640_320.png)

Vous lisez actuellement la version <img src="/misc/FR.png" height="14px" alt="UK flag" /> du *Readme* de <a href="https://github.com/tjbtjbtjb/CoCoA">CoCoA</a>. Il existe également <a href="README.md">la version <img src="/misc/UK.png" height="14px" alt="FR flag" /></a>.

Avril/octobre 2020

* Tristan Beau - [UFR de Physique](https://physique.u-paris.fr/) - [Université de Paris](http://u-paris.fr) - [laboratoire LPNHE](http://lpnhe.in2p3.fr/)
* Julien Browaeys - [UFR de Physique](https://physique.u-paris.fr/) - [Université de Paris](http://u-paris.fr) - [laboratoire MSC](http://www.msc.univ-paris-diderot.fr/)
* Olivier Dadoun - [CNRS](http://cnrs.fr)/[IN2P3](http://www.in2p3.fr) - [laboratoire LPNHE](http://lpnhe.in2p3.fr/)

Le projet CoCoA (Covid Collaborative Analysis) propose un environnement logiciel Python™ d'accès simplifié et unifié à différentes bases de données concernant le Covid19. Il s'agit de proposer au plus grand nombre (grand public non spécialiste, élèves du secondaire, étudiantes et étudiants, journalistes scientifiques, mais aussi scientifiques non spécialistes des méthodes informatiques d'accès aux données) un outil simple et pratique d'étude de données : accès aux données brutes, représentation de séries temporelles, de cartes. Il est ensuite aisé d'effectuer des analyses simples mais aussi plus complexes. Les problèmes d'accès aux bases, d'unification des méthodes, de géo-localisation des données sont assurés par CoCoA. 

Ainsi, en quelques lignes de code, avec peu voire pas de connaissance de Python™, nous pouvons produire un graphique ou une carte. Par exemple, après [installation de CoCoA](https://github.com/tjbtjbtjb/CoCoA/wiki/FR:Install) :

```
import cocoa.cocoa as cc
cc.plot(where=['France','Italy'],which='confirmed',what='Cumul')
cc.map(where=['European Union','United kingdom'])
```

produit d'une part le tracé de la série temporelle du nombre de cas confirmé pour deux pays (France et Italie), ou bien la carte des décès Covid au sein l'UE et du Royaume Uni. 

<img src="/misc/cocoa_plot_example.png" height="180px"/> <img src="/misc/cocoa_map_example.png" height="180px" />

CoCoA est prévu pour fonctionner aussi bien 
- localement (installation locale de Python™ via par exemple [`Spyder`](https://www.spyder-ide.org/) )
- sur des plateformes `Jupyter` fermées ou ouvertes comme [`Google Colab`](https://colab.research.google.com/) par exemple
- via un `docker`, utilisant par exemple [`mybinder`](https://mybinder.org/).

La documentation complète est disponible au travers [du Wiki](https://github.com/tjbtjbtjb/CoCoA/wiki/FR:Home), en particulier :
- [Installation](https://github.com/tjbtjbtjb/CoCoA/wiki/FR:Install)
- [Utilisation simple](https://github.com/tjbtjbtjb/CoCoA/wiki/FR:Basics)
- [Utilisation avancée](https://github.com/tjbtjbtjb/CoCoA/wiki/FR:AdvancedUsage)
- [Gestion des localisation](https://github.com/tjbtjbtjb/CoCoA/wiki/FR:Geo)
