CoCoA (COvid COlab Analysis) python package
===========================================
April/May 2020

* Olivier Dadoun odadoun@gmail.com
* Tristan Beau tristan.beau@gmail.com
* Julien Browaeys browaeys@gmail.com

Initial project was submitted to the hackathon https://ultrahack.org/covid-19datahack .

As physicists working at CERN experiments, used to dealing with big data, we wish to share our knowledge in statistics to the greatest number of people for Covid-19 analysis. Data mining and statistics should help people learn about the most important subject of current history. For this purpose we have designed the COvid COlab Analysis project, aka COCOA. COCOA will provide open source online statistical tools with a simple user interface and simple modelization schemes. COCOA is based on the Google Colab infrastructure which supplies a popular Python Notebook framework. This gives the opportunity to have multi-user code editing and huge computing infrastructure (included GPU for future Deep Learning Covid-19 analysis). Moreover an original analysis based on particle physics analysis is under development and should be available soon in COCOA.
As physicists working at CERN experiments or data analysts in physics, used to dealing with big data, we wish to share our knowledge in statistics to the greatest number of people for Covid-19 analysis. Data mining and statistics should help people learn about the most important subject of current history.  For this purpose we have designed the COvid COlab Analysis projet, aka COCOA.

# CoCoA package usage

We provide the backend python package cocoa which is available here at GitHub : https://github.com/tjbtjbtjb/CoCoA

It allows the final user to use as simple methods as we can to get data, analyse and/or plot them. The installation and use of the package can be done directly in a Google Colab notebook as describe bellow

##  Using CoCoA in a hurry

If you're not interested in details, just want an efficient way to get data, that's the section you have to read and test. After one command for the `cocoa` installation with the `pip` tool, two `import` line of python, you just need two other lines of python in your notebook to get your first plot of data.

```
!pip install git+https://github.com/tjbtjbtjb/CoCoA.git
import cocoa.covid19 as cc
import matplotlib.pyplot as plt
p=cc.Parser()
```

Plotting is simple.

Data is extracted through p.getStats(...) which takes in several arguments such as Cumul (total amount) or Diff (variation between two consecutive days).

Two example follow, including a semi-logarithmic plot to exhibit exponential growth in the first stages (pre-confinement).

```
plt.plot(p.getStats(country='France',which='deaths',type='Diff'))
plt.show()
plt.semilogy(p.getStats(country=['France','Italy','Spain'],which='confirmed',type='Cumul'))
plt.show()
```

The country list is available through a command `p.getCountries()`

Which dataset are available ? 
```
p.which_data_list
```
→ `['deaths', 'confirmed', 'recovered']`

And finally, the corresponding dates are given by `p.getDates()`.

## Demo code

To go further and test the code, have a look on the `colab` platform to our demo notebook :

https://colab.research.google.com/drive/1SwcGIsarHozUCoWtOhBIGQppJKbKjhhP





