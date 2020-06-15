# Examples of simple analysis of covid19 data

## World

### Using cocoa
* `testing_current_version.ipynb` gives basic use of cocoa for accessing world data and giving simple plots

### Using covid19 API
* `CocoaMap_vWorld-covid19.ipynb` gives basic use of the covid19 API outsite the cocoa framework 

## France
* `CocoaMap_vFranceDep-DC.ipynb` gives a map of cumulative deaths by departements in France. 
* `CocoaMap_vFranceDep-Cas.ipynb` gives a map of latest daily new cases in metropolitan France area, departement by departement.
* `CocoaMap_vFranceDep-Cas-wSliderBokehServer.ipynb` is similar but a slider can go earlier. You should launch locally a `bokeh` server :
```
bokeh serve --show CocoaMap_vFranceDep-Cas-wSliderBokehServer.ipynb
```
