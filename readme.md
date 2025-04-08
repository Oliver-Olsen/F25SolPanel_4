---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.0
kernelspec:
  display_name: python3
  language: python
  name: python3
---

# Projekt: Optimal opsætning af solpaneler

+++

## Indledning

> En husejer nær DTU ønsker at opsætte solpaneler på sit parcelhus med fladt tag. Hun tænker hun skal vende dem mod syd, men er i tvivl om hvilken vinkel panelet bør danne med taget. I dette projekt skal I **finde den optimale vinkel for husejerens solpaneler**. Projektets mål er at udvikle en model og et Python-program der for en angivet placering på jorden (længde- og breddegrad) kan udregne den optimale vinkel for opsætning af solpaneler under en række simplificerende antagelser. Til simulering skal bruges data fra kalenderåret 2024. I starter med at modellere solens bevægelse på himlen ved hjælp af Python-pakken *[pvlib](https://pvlib-python.readthedocs.io/en/stable/index.html)*. I skal herefter opstille en model for solpanelets energiproduktion, der ikke tager højde for skyer og atmosfære. Solen modelleres som en vektorfelt af parallelle vektorer. For at udregne energiproduktionen skal I kunne integrere vektorfeltets flux gennem solpanelfladen. Vi antager først at panelet er fladt, men I skal efterfølgende generalisere jeres model. En mulig generalisering er følgende: Find en passende flade i bymiljøet omkring DTU, som kan udstyres med tynde, fleksible solpanelsfilm (som https://www.youtube.com/watch?v=TS9ADU0oc50) og udregn energiproduktionen fra sådanne løsninger.

+++

### Forberedelse

- Ortogonale projektioner, Afsnit 2.3 
- Sfæriske koordinater (Eksempel 6.6.1) og det horisontale koordinatsystem (https://en.wikipedia.org/wiki/Horizontal_coordinate_system) 
- Flader og normalvektor, Afsnit 7.1
- Vektorfelter og flux, Afsnit 7.2 og 7.5

+++

## Om projektet

+++

### Projektmål

+++

Det overordnede mål med projektet at lave et Python-program der for angivet placering på jorden (længde- og breddegrad) kan udregne den optimale vinkel for solpaneler.

+++

### Optimalitet

+++

Optimal kan her betyde mange ting:

- **Størst årligt energiproduktion**. Det er dette optimalitets mål vi bruger med mindre andet opgives. 
- Krav om en vis daglig minimumslevering (fx om vinteren).
- Laveste samlede energiomkostninger for boligen. Her skal medregnes forbrugskurver, salg af energi til elnettet, en eventuel elbil, m.m.
- Osv.

+++

### Teori: Model og Antagelser

+++

Solenergi er omdannelsen af ​​energi fra sollys til elektricitet ved hjælp af solceller (photovoltaic (PV) cells). Solpanelers produktion af strøm afhænger af anlæggets størrelse (antallet af paneler), panelernes individuelle effektivitet, panelernes placering og selvfølgelig vejrforhold. 

Solindstråling eller irradians (solar irradiance) er den effekt pr. arealenhed (overfladeeffekttæthed) som modtages fra solen i form af elektromagnetisk stråling i måleinstrumentets bølgelængdeområde. Solindstråling måles i watt pr. kvadratmeter ($W/m^2$) i SI-enheder. Solens indstråling har forskellig bølgelængde, fx UV-stråling, der samlet kaldes indstrålingens spektrum. 

Den *gennemsnitlige* årlige solstråling, der ankommer til toppen af ​​jordens atmosfære, er omkring $1361 W/m^2$. Når solens stråler har passeret atmosfæren, er den samlede stråling (irradians) i Danmark ca. $S_0 := 1100 W/m^2$ på en klar dag midt på dagen. Spektrummet ændres ligeledes gennem atmosfæren, fx kommer den korteste UV-stråling (under 280 nanometer) sjældent ned til Jordens overflade, men vi vil ignore sådanne spektrale ændringer.  

Man kan med god tilnærmelse regne med en lineær sammenhæng mellem solens indstråling og den strømstyrke, som solpanelet leverer, og vi vil bruge denne tilnærmelse. Da temperaturen i praksis stiger ved øget indstråling, og spændingen falder med øget temperatur, vil effekten dog ikke stige helt lineært. Solens stråler modelleres som et vektorfelt $\pmb{V}_S$ af parallelle vektorer af længde $S_0$. Lad os antage at solpanelet er beskrevet ved en flade $\mathcal{F} = \pmb{r}(\Gamma)$, hvor $\pmb{r} : \Gamma \to \mathbb{R}^2$, $\Gamma = [a_1,b_1] \times [a_2,b_2]$, er en parametrisering af fladen. Energiproduktionen for en solcelle afhænger af vinklen mellem fladens normalvektor $\pmb{n}_\mathcal{F}$ og solstrålerne. Hvis solstrålerne er parallelle med normalvektoren er solens effekt maksimal, mens hvis solstrålerne er vinkelrette på normalvektoren er effekten nul. Solens effekt pr areal i punktet $\pmb{r}(u,v)$, hvor $(u,v) \in \Gamma$, er projektionen af solens stråler på fladens enheds normalvektor:

\begin{equation*}
   \left\langle \pmb{V}, \frac{\pmb{n}_\mathcal{F}(u,v)}{\Vert \pmb{n}_\mathcal{F}(u,v) \Vert} \right\rangle 
\end{equation*}

Den samlede effekt fås at integrere denne størrelse op over held fladen, hvilket svarer til fluxen af $V$ gennem fladen $\mathcal{F}$:

\begin{equation*}
   \int_{\Gamma} \langle \pmb{V}, \pmb{n}_\mathcal{F}(u,v) \rangle \mathrm{d}(u,v) 
\end{equation*}

Hvis $\langle \pmb{V}, \pmb{n}_\mathcal{F}(u,v) \rangle < 0$ betyder det er solen lyser på bagsiden af solpanelet, og effekten skal derfor sættes til nul (effekten kan aldrig blive negativ).

+++

Vi angiver her vores **standard-antagelser**, som bruges med mindre andet angives:

- Panelet er **fladt og fastmonteret**.
- Vi antager, at den maksimale irradians (indstråling) fra solen på solpanelet er $S_0 = 1100 \,\mathrm{W/m^2}$. Alle vektorer i solens vektorfelt $\pmb{V}: \mathbb{R}^3 \to \mathbb{R}^3$ er parallelle og har længden $S_0$.
- Solpanelets effekt afhænger **lineært** af solindstrålingen og dermed af **fluxen** af solens vektorfelt gennem panelets overflade.
- **Virkningsgraden** $\eta$ for solpanelet defineres ud fra en standard testbetingelse på $1000 \,\mathrm{W/m^2}$. Ved denne flux leverer panelet
  \begin{equation*}
  \frac{Wp}{L \cdot B} \,\mathrm{W/m^2},
  \end{equation*}
  hvor $Wp$ er panelets peak power (i watt), og $L$ og $B$ er henholdsvis længden og bredden af panelet (i meter).
- Skydække og andre atmosfæriske forstyrrelser modelleres ikke direkte, men sættes til en gennemsnitlig værdi. Vi antager, at disse forstyrrelser i gennemsnit halverer solindstrålingen året rundt:
  \begin{equation*}
  S_0 A_0 = 550 \,\mathrm{W/m^2}, \quad \text{hvor } A_0 = 0.5.
  \end{equation*}
  Dermed antager vi, at solens vektorfelt $\pmb{V}$ stadig har konstant retning, men **reduceret længde** $A_0 S_0$.

Der vil i sidste del af projektet være mulighed for at vende tilbage til disse antagelser og undersøge, om – og i så fald hvordan – de kan erstattes af mere realistiske eller situationsspecifikke modeller.

+++

## Indledende øvelser

+++

> Find via litteratur-søgning den anbefalede vinkel man opstiller solpaneler ved i Danmark. Vinklen siges at være nul grader hvis panelet ligger fladt ned på jorden (eller taget).




+++


+++

> Udvælg en solpanelstype. I kan søge på montører i Danmark og undersøge hvilke paneler de typisk bruger, eller I kan google "solar panel datasheet" eller lignende. Solpanelet bør være et standard panel (der er fladt og altså ikke fx krummer). Find et datablad for det valgte solpanel, og beskriv panelets størrelse (anvend $L$ længde og $B$ for bredde) og angiv Wp/Pmax (kaldet max power, peak power watts eller lignende) under standarden STC. Beskriv hvad standarden STC beskriver. Udregn $Wp/(L B)$ (jvf. listen af standard-antagelser ovenfor). Antag ideelle forhold: solen står vinkelret på solpanelet og solens irradians er $1100 W/m^2$ igennem en hel time. Hvor mange J og kWh leverer panelet på denne time? Hvor mange Wh er dette per $m^2$? 

> Jeres endelige rapport skal desuden indeholde et indledende afsnit, hvor I beskriver solenergi og solceller. I bestemmer selv hvad afsnittet præcist skal indeholde, men nedenstående kilder kan bruges til at finde information. Det anbefales først at skrive dette afsnit, når I nået længere med projektet. 

1. https://www.pveducation.org/
1. https://www.acs.org/education/resources/highschool/chemmatters/past-issues/archive-2013-2014/how-a-solar-cell-works.html

+++


Panelet er fladt, så enhedsnormalvektoren $\pmb{u}_p$ er konstant (og har længde 1) hvor:

\begin{equation*}
\pmb{u}_p = \frac{\pmb{n}_{\mathcal{F}}(u,v)}{\Vert \pmb{n}_\mathcal{F}(u,v) \Vert}
\end{equation*}

> Angiv en formel eller udtryk for fluxen gennem fladen udtrykt ved $A_0$, $\pmb{u}_p, \pmb{V}, L$ og $B$. Vi definerer fluxen til at være nul hvis vinklen mellem $\pmb{u}_p$ og $\pmb{V}$ er større end $\pi/2$ (90 grader), da vi ikke ønsker negativ flux. Jeres udtryk skal tage højde for dette.

*Hint:* Da normalvektoren er konstant, kan I slippe af med integraltegnet.

+++


Fluxen gennem fladen bestemmer den øjeblikkelige effekt for panelet for en bestemt retning af solens stråler $\pmb{V}$ og for en bestemt placering af panelet bestemt ved $\pmb{u}_p$. For at finde den samlede energiproduktion for en solpanel, har vi har derfor brug for at kunne modellere solens bevægelse i forhold til panelet. Dette modeleres med en solspositionsalgoritme (SPA) fra Python-pakken `pvlib`, men inden vi kommer så langt, har vi brug for at udvikle nogle værktøjer i NumPy.

+++

> Angiv SI-enheder for $\pmb{V}$, $L$, $B$, $A_0$, fluxen, energi. Angiv sammenhængen mellem J og kWh.  


+++

## NumPy

+++

I projektet har vi brug for at kunne finde minimum, maksimum og/eller nulpunkter as NumPy-arrays, så vi starter med at blive fortrolige med dette. Vi betragter en simpel funktion $f: [0, 2 \pi] \to \mathbb{R}$ givet ved $f(x) = \cos(x)$ og ønsker at kunne bestemme minimum, maksimum og nulpunkter af denne. Vi vil i projektet dog ikke have selve funktionen eller dens funktionsudtryk, men kun en (lang) række at funktionsværdier, fx $f(t_n)$ for $t_n = 2\pi n/N$ for $n = 0,1, \dots, N-1$. Vi opfatter her $\Delta t_n = 2 \pi/N$ som afstanden mellem vores tids-samples. I NumPy:

```{code-cell} ipython3
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
figurstr = (15, 7)

t = np.linspace(0, 2 * np.pi, 1000)
f = np.cos(t)

plt.figure(figsize=figurstr)
plt.plot(t, f, color='b', linestyle='-')
plt.xlabel('t')
plt.ylabel('cos(t)')
plt.show()

# print(t,f)  # uncomment to see the values of t and f
```

Vi opfatter `t` og `f` som *vektorer* af hhv variabel- og funktionsværdier. NumPy har mange indbyggede metoder, der kan være nyttige, fx

```{code-cell} ipython3
f.max(), f.min(), f.argmax(), f.argmin(), t[f.argmax()], t[f.argmin()]
```

Man kan også spørge hvilke funktionsværdier der fx er mindre end $-0.95$:

```{code-cell} ipython3
idx = f < -0.95
f[idx], t[idx]

# Or in one line
f[f < -0.95], t[f < -0.95]
```

hvor vi også angiver de tilhørende tids-værdier i `t`-vektoren.

+++

> Skriv Python-kode der finder alle funktionsværdier i `f` i intervallet $[-0.05, 0.05]$ og angiver de tilhørende `t`-værdier. 

> Skriv en Python-funktion der kan finde begge fortegnsskift (nulpunkterne) af `f`. 

Tjek at de fundne nulpunkter stemmer rimeligt overens med de eksakte nulpunkter for $f$. Jeres metode bør være simpel og også virke på "vektorer" `np.array([3, 0.5, 0.1,-0.5, -1, -0.5, 0.5, 2])` hvor vi ikke kender den funktion, der ligger bag funktionsværdierne. Specielt bør jeres metode ikke bruge anden viden om $\cos$ (fx at den kan differentieres) end den information I har i `f`-vektoren.  

I kan finde inspiration i bisektionsmetoden (som I stødte på i Matematik 1a i efteråret), eller I kan finde inspiration i NumPy-funktioner `np.where, np.diff, np.sign` eller følgende Python-plot:

```{code-cell} ipython3
plt.figure(figsize=figurstr)
plt.plot(t, np.abs(f), color="r")  # linestyle='-', marker='.'
plt.xlabel("t")
plt.ylabel("|cos(t)|")
plt.show()
```


+++

## Solspositionsmodel

+++

### Koordinatsystem

+++

For at kunne regne på fx solens bevægelse og projektionen af solens stråler ind på panelets normalvektor, skal vi have indført (mindst et) passende koordinatsystem. Vi vælger at placere et fast centrum (origo) $(0,0,0)$ i panelets position. Vi forestiller os herefter tangentplanen til jorden i panelets position. Normalvektoren til dette tangentplan vil være vores $z$-akse. $x$-aksen og $y$-aksen "udspænder" således tangentplanen. Vi fastlægger koordinatsystemet ved at $x$-aksen peger mod nord og $y$-aksen mod øst. Den opmærksomme læser vil have opdaget at dette er et venstredrejet koordinatsystem. Dette er dog traditionen, og koordinatsystemet kaldes det horisontale koordinatsystem https://en.wikipedia.org/wiki/Horizontal_coordinate_system. Vi har altså nu et referencesolpositionssystem, der fokuserer på observatøren (panelet) på en given bredde- og længdegrad på jordens overflade. Lad os opsummere:

1. Koordinatsystemet har centrum i solpanelet (kaldet observatøren). Det er traditionelt at bruge et venstredrejet koordinatsystem hvor $x$-aksen peger mod nord, $y$-aksen peger med øst og $z$-aksen peger mod zenit-punktet i retning af normalvektoren til tangentplanen. Koordinatsystemet kaldes det horisontale koordinatsystem, da det er orienteret efter observatørens lokale horisont. 
1. Ethvert objekt kan beskrives i det horisontale koordinatsystem enten i kartesiske koordinater $(x,y,z)$ eller sfæriske koordinater $(r,\theta,\phi)$. Her er $\phi \in [0,2\pi]$ azimut-vinklen der måles fra $x$-aksen mod $y$-aksen, $\theta \in [0,\pi]$ er zenit-vinklen fra $z$-aksen og $r$ er radius.  
1. Det horisontale koordinatsystem er fastgjort til et sted på Jorden, ikke stjernerne eller solen. Objekter på stjernehimlen forestilles placeret på himmelsfæren i en fast afstand og deres placering beskrives ved azimut- og zenit-vinklen (radius ignoreres således i denne type beskrivelse). Over tiden vil zenit- og azimut-vinklen for et objekt på himlen (som fx solen) ændres, da objektet ser ud til at drive hen over himlen med Jordens rotation. Da det horisontale koordinatsystem er defineret af observatørens lokale *horisont*, vil det samme objekt set fra forskellige steder på Jorden på samme tid have forskellige værdier af azimut- og zenit.

![Kilde: https://assessingsolar.org/notebooks/solar_position.html](solar_position_system.png)


Vi måler enten vinklerne i radianer $(\theta, \phi) \in [0, \pi] \times [0, 2\pi]$ eller grader $(\theta,\phi) \in [0, 180^\circ] \times [0, 360^\circ]$. Der bruges ofte endnu en vinkel, nemlig solens højdevinkel ($\alpha$), som er komplementæren til zenitsolvinklen ($\alpha = 90^\circ - \theta$), der altså måler vinklen fra horisont-planen mod $z$-aksen.

> Skriv en Python-funktion `def solar_elevation_angle(theta)` der givet $\theta$ i grader udregner $\alpha$ i grader.

+++


Hvis vinklerne er givet i radianer, kan vi bruge `solar_elevation_angle` sammen med `np.deg2rad` og `np.rad2deg`. Vi behøver derfor ikke lave funktioner for både grader og radianer, da vi let kan genbruge vores funktioner. Hvis vi fx her ønsker at regne i radianer:

```{code-cell} ipython3
theta_in_rad = np.pi / 3  # zenit-vinkel givet i radianer
print(np.pi / 2. - theta_in_rad)  # højdevinkel givet i radianer
# højdevinkel givet i radianer
# np.deg2rad(solar_elevation_angle(np.rad2deg(theta_in_rad)))  # udkommenter denne
```

Det anbefales i det videre forløb at regne i radianer, men at angive resultater/vikler i grader hvis dette er mere sigende/beskrivende. Bemærk også at vi ikke behøver at bruge `solar_elevation_angle` i det følgende da både zenit- og elevationsvinklen vil være tilgængelige.

+++

I det horisontale koordinatsystem er ethvert objekt på *himmelsfæren* fuldstændig bestemt af zenitvinklen ($\theta$) og azimutvinklen $\phi$. Som nævnt ignorer man den radiale koordinat når alle objekter placeres på himmelsfæren. Vi kan dog sagtens medtage den radiale koordinat: 

> Antag at solen har en fast afstand $r_s$ til jorden. Find en rimelig værdi for $r_s$. Angiv et (matematisk) udtryk for hvordan solens $xyz$-koordinat kan udregnes ud fra $r_s$, $\theta_s$ og $\phi_s$, hvor $\theta_s$ og $\phi_s$ er hhv. zenit og azimut-vinklen for solens placering.

+++


+++

Der placeres et (flat) solpanel i origo af koordinatsystemet. Enhedsnormalen $\pmb{u}_p \in \mathbb{R}^3$ til solpanelet har zenit-vinkel $\theta_p$ og azimut-vinkel $\phi_p$. Vi betrager en normaliseret (dvs enheds-) solvektor $\pmb{u}_{s} \in \mathbb{R}^3$ givet ved $(\theta_s, \phi_s)$. Solens vektorfelt er således givet ved $\pmb{V} = S_0 \pmb{u}_{s}$.  

> Angiv et (matematisk) udtryk for $\pmb{u}_p$ og for $\langle \pmb{u}_{s}, \pmb{u}_p \rangle$ ud fra zenit- og azimut-vinklerne. I bør simplificere udtrykket så det indeholder $\cos(\phi_p-\phi_s)$ og kun 5 trigonometriske funktioner.  Vis at $-1 \le \langle \pmb{u}_{s}, \pmb{u}_p \rangle \le 1$. Forklar man egne ord hvad det betyder når $\langle \pmb{u}_{s}, \pmb{u}_p \rangle < 0$.

+++


> Skriv en Python-funktion `def solar_panel_projection(theta_sol, phi_sol, theta_panel, phi_panel)` der returnerer $\langle \pmb{u}_{s}, \pmb{u}_p \rangle$ når det er positivt og ellers returnerer nul. 

> Kig igen på jeres Python-funktion `def solar_panel_projection(theta_sol, phi_sol, theta_panel, phi_panel)`. Skriv den om så den virker på NumPy-arrays af zenit- og azimut-vinkler. Du kan teste den på følgende de tre situationer, hvor projektionen bør give 0.707107, 0.0 og 0.0 (eller rettere, med numeriske fejl, bør det give `array([7.07106781e-01, 6.12323400e-17, 0.0])`). Forklar solpanelets orientering og solens placering i de tre situationer.

```{code-cell} ipython3
theta_sol = np.array([np.pi / 4, np.pi / 2, 0.0])
phi_sol = np.array([np.pi, np.pi / 2, 0.0])
theta_panel = np.array([0.0, np.pi / 2, np.pi])
phi_panel = np.array([np.pi, 0.0, 0.0])

# solar_panel_projection(theta_sol, phi_sol, theta_panel, phi_panel)
```


+++

### Solpositionsmodellering ved Pvlib

+++

I Python kan solpositionsvinklerne, benævnt $(\theta_s, \phi_s)$, nemt beregnes på ethvert sted ved hjælp af solar positionsalgoritmen (SPA) med pakken `pvlib`, der som standard er implementeret med National Renewable Energy Laboratory's SPA-algoritme [Reda og Andreas, 2003, https://www.nrel.gov/docs/fy08osti/34302.pdf]). Vi følger https://assessingsolar.org/notebooks/solar_position.html.

```{code-cell} ipython3
import pandas as pd
import pvlib
from pvlib.location import Location
```

Vi skal først have defineret observatørens/panelets geografiske placering. Det gøres via objektet *pvlib.location.Location* i biblioteket *[pvlib](https://pvlib-python.readthedocs.io/en/stable/index.html)*, hvor vi skal angive bl.a. breddegrad, længdegrad, tidszone og højde. Til simulering bruges data for $(\theta_s, \phi_s)$ fra fx kalenderåret 2024, men her i denne indledende øvelse nøjes vi med data for nuværende måned, april 2024:

```{code-cell} ipython3
tidszone = "Europe/Copenhagen"
start_dato = "2024-04-01"
slut_dato = "2024-04-30"
delta_tid = "Min"  # "Min", "H",

# Definition of Location object. Coordinates and elevation of Amager, Copenhagen (Denmark)
site = Location(
    55.660439, 12.604980, tidszone, 10, "Amager (DK)"
)  # latitude, longitude, time_zone, altitude, name

# Definition of a time range of simulation
times = pd.date_range(
    start_dato + " 00:00:00", slut_dato + " 23:59:59", inclusive="left", freq=delta_tid, tz=tidszone
)
```

> Vælg placering/lokation for jeres solpanel, fx DTU. Ret overstående GPS-koordinater (målt i DecimalDegrees), højde og navn så det passer med den valgte lokation. 

Vi kan nu finde solpositionen ud fra det horisontale koordinatsystem placering i `site` for det angivne tidsinterval ved følgende kald:

```{code-cell} ipython3
# Estimate Solar Position with the 'Location' object
solpos = site.get_solarposition(times)

# Visualize the resulting DataFrame
solpos.head()
```

Vi ser at DataFramen indeholder solpositionen for hvert minut i april 2024. Tids-samplingen $\Delta t$ kan styres ved `delta_tid = "Min"` (minute) sat ovenfor. Når vi senere skal udregne energiproduktionen over hele 2024, kan det være tilstrækkeligt med at kende solpositionen for hver time (for hele året 2024), DataFramen bliver nemlig meget stor, hvis man bruger `delta_tid = "Min"` for et helt år. Dette klares ved `delta_tid = "H"` (hour). Bemærk at `delta_tid = "M"` (month) sætter $\Delta t$ til en måned (hvilket er for stort til vores behov).

+++


Efter at solvinklerne er estimeret ved hjælp af `pvlib`, kan de visualiseres, fx for den 1. april:

```{code-cell} ipython3
import matplotlib.dates as mdates

valgt_dato = "2024-04-01"

# Plots for solar zenith and solar azimuth angles
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 10))
fig.suptitle("Solar Position Estimation in " + site.name + valgt_dato)

# plot for solar zenith angle
ax1.plot(solpos.loc[valgt_dato].zenith)
ax1.set_ylabel("Solar zenith angle (degree)")
ax1.set_xlabel("Time (hour)")
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H"))

# plot for solar azimuth angle
ax2.plot(solpos.loc[valgt_dato].azimuth)
ax2.set_ylabel("Solar azimuth angle (degree)")
ax2.set_xlabel("Time (hour)")
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
```

Bemærk at $x$-aksen bruger UTC-tidszone og der derfor skal $+2$ for at få dansk tid. De plottede vektorer kan udskrives:

```{code-cell} ipython3
valgt_dato = "2024-04-01"
print(solpos.loc[valgt_dato].zenith)
print(solpos.loc[valgt_dato].elevation)
print(solpos.loc[valgt_dato].azimuth)
```

Her har vi valgt at plotte solvinklerne for 1. april. 

> Plot solens zenit-, azimut- og elevationsvinkel, dvs. $\theta_s, \phi_s, \alpha_s$, for hele dagen den 20. april 2024 som funktion af tiden. 

**Anbefaling:** I det følgende har vi brug af at arbejde med vektorer af fx zenit- og azimut-vikler, specielt at kunne finde maksimumsværdier, nulpunkter, integrere, osv. Det anbefales derfor at arbejde med dataen fra `solpos` som NumPy-arrays. Dette kan gøres ved fx:

```{code-cell} ipython3
np.array(solpos.loc[valgt_dato].elevation)
```

> Plot solens elevationsvinkel og find ud af hvornår på dagen solen står højest den 20. april 2024. Forklar hvad det betyder når $\alpha_s < 0$ eller $\theta_s > 90^\circ$.

+++


+++

> Find tidspunktet for solopgang og solnedgang på DTU den 20. april 2024. Sammenlign med "kendte" værdier fx fra DMI. 

*Hint:* Hvis I ønsker præcise værdier skal I bruge `apparent_elevation` (apparent sun elevation accounting for atmospheric refraction) i stedet for `elevation`. I behøver ikke tage højde for jordens krumning. 


+++

> Find solens højeste punkt på himlen (i grader) på sommersolhverv på DTU, og hvornår på dagen det sker? 

*Hint:* Du bliver nødt til at ændre på start og slut dato for `solpos`-objektet.

+++


> Lav en Python-funktion som kan beregne solens højeste punkt $\alpha_{max}$ på himlen (i grader) på en given dato (year-month-day) i en given lokation (fx by) angivet ved en breddegrad og længdegrad. 

*Hint:* Svaret bør ikke afhænge af længdegraden, da solens højeste punkt på himlen kun afhænger af breddegraden.



+++

I har i en tidligere opgave fundet et udtryk for solens $xyz$-koordinat ud fra $r_s$, $\theta_s$ og $\phi_s$. 

> Skriv en Python-funktion (til brug med NumPy arrays) der omregner fra solens zenit og azimut til solens position angivet i $xyz$-koordinaten. Husk om I regner i radianer eller grader. Her kan `np.deg2rad()`-funktionen være nyttig. Det er fint at bruge en cirka værdi for $r_{s}$ men man kan finde en mere korrekt værdi ved: `pvlib.solarposition.nrel_earthsun_distance(times) * 149597870700`, hvor `149597870700` er antal meter på en astronomisk enhed AU.



+++

> Skriv en Python funktion der omregner fra solens position på himlen i et $xyz$ koordinater til zenit og azimuth (i grader eller radianer). Her kan `np.arctan2(y, x)` og `np.rad2deg()` være nyttige.

+++


+++

## Matematiske overvejelser

+++

### Flux udtrykt udelukkende ved $A_0$, $S_0$ og vinkler

I vores model antages det, at den øjeblikkelige solindstråling, som et solpanel
modtager, afhænger af en atmosfærisk reduktionsfaktor $A_0$ (her $A_0 =
0.5$) og den maksimale irradians $S_0$ (fx $S_0 = 1100\,W/m^2$). For hver
energiberegning fastholdes solpanelets orientering, således at hældningsvinklen
$\theta_p$ og azimutvinklen $\phi_p$ behandles som konstante variable.
Solens position til enhver tid $t$ angives ved zenitvinklen $\theta_s(t)$ og
azimutvinklen $\phi_s(t)$. 

> Udled en eksplicit formel for den øjeblikkelige flux $\text{Flux}(t,\theta_p,\phi_p)$ modtaget af panelet, hvor fluxen udtrykkes udelukkende i de følgende variable og konstanter:
>
>- $A_0$: den atmosfæriske reduktionsfaktor (0.5),
>- $S_0$: solens maksimale irradians (1100 W/m²),
>- $\theta_s(t)$ og $\phi_s(t)$: solens zenit- og azimutvinkel ved tidspunktet $t$,
>- $\theta_p$ og $\phi_p$: panelets orienteringsvinkler.
>- $L$ og $B$: panelets længde og bredde (disse kan udelades hvis fluxen regnes per $m^2$)

Denne opgave bygger direkte videre på tidligere øvelser og bør være til at gå til (uden udregninger). Husk, at fluxen skal defineres således, at der kun tælles positive bidrag, dvs. at den sættes til nul (fx ved hjælp af en funktion som $\max(x,0)$), når solens stråler rammer bagsiden af panelet. Husk også at fluxen skal sættes til nul, hvis solen ikke er stået op -- til dette kan man bruge "tuborg"-notation ("definition by cases") og en betingelse på $\theta_s(t)$).

+++


+++

### Kontinuerte solvinkelfunktioner af tiden

+++

Vi antager, at solens zenitvinkel $\theta_s(t)$ er en kontinuert funktion af tiden $t$.  

> Diskuter, hvorfor denne antagelse er rimelig. (Der forventes ikke et bevis fra den matematiske fysik, men en diskussion baseret på
intuitiv forståelse af den fysiske model.)

Solens azimutvinkel $\phi_s(t)$ er ligeledes  en kontinuert funktion af tiden $t$ på nær i springet fra 360 grader til 0 grader. 

> Forklar hvorfor vi deraf kan udlede at $\cos(\phi_s(t)-\phi_p)$ og $\sin(\phi_s(t))$ er kontinuerte funktioner af tiden.

+++


+++

### Diskontinuiteter i fluxen (over ét døgn)

+++

> Argumentér for, at solpanelets flux $\text{Flux}(t,\theta_p,\phi_p)$ som funktion af $t$ er stykkevis kontinuert. Forklar hvorfor fluxen kan have diskontinuiteter. Beskriv et tilfælde hvor fluxen ikke har diskontinuiteter (over et døgn) og beskriv et tilfælde hvor fluxen har præcis en diskontinuitet (over et døgn). Angiv hvor mange diskontinuiteter fluxen maksimalt kan have over et døgn. Hvis vi er i et tilfælde hvor fluxen ingen diskontinuiteter har, vil fluxen så automatisk også være differentiabel?


+++


+++


### Approksimation af solvinkel over ét døgn

+++

Vi betragter solens bane for et enkelt døgn – her valgt til den 20. april 2024 – og antager, at solens zenitvinkel kan tilnærmes ved en trigonometrisk funktion af formen

\begin{equation*}
\theta_s(t) \approx \widetilde{\theta}_s(t) \quad \text{hvor } \widetilde{\theta}_s(t) := M_z + A_z\,\cos\Bigl(\omega_z\,(t - T_z)\Bigr),
\end{equation*}

og hvor:
- $M_z$ er den gennemsnitlige zenitvinkel (middelværdien),
- $A_z$ er amplituden (dvs. halvdelen af variationen omkring $M_z$),
- $\omega_z$ er den angulære frekvens. Hvis $t$ er angivet i timer, kan man for en 24-timers periode vælge $\omega_z \approx \frac{2\pi}{24}$,
- $T_z$ er tidsforskydningen, der placerer den minimale zenitvinkel (solens højest position) korrekt, typisk omkring middagstid.

For solens azimutvinkel antager vi en lineær (affin) funktion $\widetilde{\phi}_s(t) := a\,t + b$ som approksimation til $\phi_s(t)$, hvor $a$ og $b$ vælges, så modellen opfylder: 

\begin{equation*}
\sin(\phi_s(t)) \approx \sin(a\,t+b) \quad \text{og} \quad \cos(\phi_s(t)-\phi_p) \approx \cos(a\,t+b-\phi_p)
\end{equation*} 

> Brug solpositionsdata for den 20. april 2024 (hentet med pvlib) til at bestemme approksimative værdier for parametrene $M_z$, $A_z$, $\omega_z$, $T_z$, $a$ og $b$. For at gøre dette skal I "fitte" de respektive funktioner til solpositionsdata. Endelig skal I lave to separate plots, der illustrerer jeres tilnærmelse:
>
>Én for zenitvinklen
>
>\begin{equation*}
\theta_s(t) \approx M_z + A_z\,\cos\Bigl(\omega_z\,(t - T_z)\Bigr), 
\end{equation*}
>
>og én for azimutvinklen
>
>\begin{equation*}
\phi_s(t) \approx a\,t + b.
\end{equation*}

(I er velkomne til at foreslå en forbedret model $a\,t + b$ af $\phi_s(t)$)     

+++

### Tidsintegration af flux over ét døgn

+++

Vi definerer den samlede energi, som panelet optager over et døgn, som

\begin{equation*}
E(\theta_p, \phi_p) = \eta \int_{t_1}^{t_2} \text{Flux}(t,\theta_p,\phi_p)\,dt,
\end{equation*}

hvor $t_1$ og $t_2$ markerer starten og slutningen af døgnet 20. april 2024, og $\eta$ er panelets effektivitet. (Hvis fluxen regnes per $m^2$, skal $E(\theta_p, \phi_p)$ gange med solpanelets længde $L$ og bredde $B$.)

Vi ønsker at maksimere energiproduktionen $E(\theta_p, \phi_p)$. Vi antager at solpanelet skal vende med syd så $\phi_p = \pi = 180^\circ$ og skal derfor kun maksimere $E(\theta_p, \pi)$ som funktion af $\theta_p$. Vi ønsker egentligt at maksimere den energiproduktionen over et helt år, så $t_1$ og $t_2$ markerer starten og slutningen af året, men vi vil i denne opgave altså kun betragte 20. april 2024. Yderligere vil vi erstatte $\theta_s(t)$ og $\phi_s(t)$ med tilnærmelserne hhv. $\widetilde{\theta}_s(t)$ og $\widetilde{\phi}_s(t)$ fundet i forrige opgave. 

I denne delopgave antager vi (for at gøre det simpelt) at $\eta\,L\,B =1$. Vælg $t_1$ og $t_2$ som de tidspunkter hvor $\widetilde{\theta}_s(t)=\pi/2=90^\circ$ (dvs. hhv. approksimative solopgangs- og solnedgangstider). 

> Bestem under disse antagelser et udtryk for $E(\theta_p, \pi)$. Afgør om $E(\theta_p, \pi)$ er en kontinuert og/eller differentiabel funktion med hensyn til $\theta_p$. Find maksimum af $E(\theta_p, \pi)$ for 20. april 2024 og angiv den vinkel $\theta_p$ der maksimerer energiproduktionen. 


```{note} 
I dette projekt ønsker vi at finde den optimale solpanelsvinkel $\theta_p$, der maksimerer energiudbyttet. I Matematik 1b foretager vi typisk maksimumsundersøgelser ved at finde stationære punkter samt eventuelle undtagelsespunkter. Derfor er det afgørende at vide, om $E(\theta_p, \pi)$ er differentiabel med hensyn til $\theta_p$, da denne differentiabilitet muliggør en præcis bestemmelse af de stationære punkter og kan afsløre eventuelle undtagelsespunkter.
```

+++

## Effekt- og energiberegninger

+++

Det kan være udfordrende at udregne eksakte integraler, særligt når integrationen skal udføres over et helt år. Derfor vælger vi nu at overgå til numeriske beregninger i Python for at estimere energiudbyttet. Vi får derfor heller ikke brug for de approksimerende funktioner $\widetilde{\theta}_s(t)$ og $\widetilde{\phi}_s(t)$ fra de to foregående spørgsmål.

**Anbefaling:** Det anbefales at I regner alting i radianer. Husk at man kan bruge `np.deg2rad` eller `np.rad2deg`. Hvis I har vinklerne i grader, skal man altså bruge `np.rad2deg`.   

Vi betragter den 20. april. `solpos` indeholder solpositionsdata for hvert minut gennem hele dagen. Da der er 1440 minutter på en dag er solpositionsvinkler over denne dag beskrevet ved en vektor af denne længde, fx:

```{code-cell} ipython3
solpos.loc[valgt_dato].zenith
```

Vi betragter kun $\theta_p \in [0, \pi/2]$, da $\theta_p > \pi/2$ svarer til at vi begynder at vende panelet med bagsiden op ad.  

> Lav en Python-funktion som kan udregne fluxen af solens vektorfelt gennem solpanelets flade for hvert minut gennem dagen. I bør bruge `solar_panel_projection(theta_sol, phi_sol, theta_panel, phi_panel)`. Husk under alle omstændigheder kun at "medtage" sol-zenitvinkler $\theta_s \in [0, \pi/2]$ (hvorfor?) så panelets flux er nul hvis $\theta_s$-værdierne (i en vektor som solpos.loc[valgt_dato].zenith) er over $\pi/2$ dvs. 90 grader.



+++

For at finde energiproduktionen fra solpanelet skal vi integrere fluxen (dvs effekten) op over den betragtede tidsperiode. Vi regner altid i SI-enheder, men I bør angive endelig resultater (fx den samlede energiproduktion) i relevante enheder (fx både i Joules og kWh). Til at integrere kan vi bruge Trapez-metoden kendt fra Matematik 1b. I må gerne bruge jeres egen implementering af Trapez-metoden, men vi vælger her dog at bruge Simpson's regel https://da.wikipedia.org/wiki/Simpsons_regel fra SciPy-pakken. Energiproduktionen kan angives per $m^2$ panel. Husk at medregne solpanelets effektivitet (mht fluxen) som beskrevet i standard-antagelserne.

```{code-cell} ipython3
from scipy import integrate
# flux = np.array(...)  # fra forrige opgave

# husk at tage højde for panelets effektivitet, jvf standard antagelserne

# dx=60 since there are 60 s between time samples

# Udkommenter
# integral_value = integrate.simps(..., dx=60)
# integral_value
```

`flux` er her vektoren (np.array) der indeholder fluxen udregnet for hvert minut dagen igennem.  Parameteren `dx=60` fortæller SciPy at fluxen er samplet hvert minut (1 minut er 60 sekunder i SI-enhed). Hvis I senere vælger at bruge `delta_tid = "H"` når I skal regne energiproduktionen for et helt år, så skal I huske at fortælle `integrate.sipms` om den ændrede tids-sampling, nemlig `dx=3600`. Man kan dog sagtens regne med `delta_tid = "Min"` hele vejen igennem uden at det bliver for tungt at regne på. 

+++


> Peg solpanelet mod syd, dvs azimut-vinkel $\phi_p = 180^\circ$. Udregn energiproduktionen for den 20.april for hver *heltals* vinkel $\theta_p$ mellem 0 og 90 grader.

+++


+++

## Optimal vinkel

+++

Vi skal nu endelig betragte energiproduktionen for hele 2024. Kald et nyt `solpos`-objekter med det relevante tidsinterval. 

> Peg solpanelet mod syd, dvs azimut-vinkel $\phi_p = 180^\circ$. Udregn energiproduktionen for hele 2024 for hver *heltals* vinkel $\theta_p$ mellem 0 og 90 grader.

+++


+++

> Find den optimale vinkel $\theta_p$ og angiv energiproduktionen. Hvor meget mindre bliver energiproduktionen hvis $\phi_p$ fx er $175^\circ$ eller lignende?

+++


+++

> Lav en realistisk opsætning af $X$ antal solpaneler, hvor I vælger $X$ efter en typisk opsætning på et parcelhus. Solpaneler opsættes efter den optimale vinkel. Udregn energiproduktionen for hver dag og plot dette som funktion af tiden (angivet i dage).

+++


+++

## Udvidelser

+++

I skal nu vælge at arbejde videre med *mindst en* af følgende udvidelser:

+++

### Solpanelsfilm på en krum flade

+++

En solpanelsfilm (eng: thin solar/power film) er en tynd film som man kan påklistre forskellige bygningsflader og som virker som et solpanel. Tag på ekskursion i DTUs nærområde, find en ikke-plan flade i bymiljøet som egner sig til påmontering af solpanelsfilm. Men en "ikke-plan" flade menes en krum flade hvor fladens normalvektor ikke er konstant. Den kan være taget på et busskur, øverste etage på Jægersborg vandtårn, osv. Det bør være en flade som I kan parametrisere. Opstil en parametrisering for den valgte bygningsflade. Find et datablad for en solpanelsfilm som (med rimelighed) kan bruges på den valgte bygningsflade og angiv de relevante data. Generaliser jeres model og Python-kode så der tages højde for at solpanelets normalvektor ikke er konstant. Udregn den årlige energiproduktion for solpanelsfilmen på bygningsdelen.   

Da normalvektoren ikke længere er konstant over hele fladen, skal I nu integrere projektionen af $\pmb{V}$ ind på fladens enhedsnormelvektor op over hele fladen. Til dette kan I bruge SciPy. Husk at projektionen skal sætte til nul, når den er negativ. I bør vælge en flade hvor skyggen for fladen selv ikke bliver for kompliceret at håndtere.

+++

### Optimering med hensyn til profit 

I stedet for udelukkende at maksimere den årlige energiproduktion (i kWh) for solpanelerne, skal I nu optimere panelets orientering (**både** $\theta_p$ **og** $ \phi_p$) med henblik på at maksimere den årlige profit, når al strømmen sælges til det danske elnet. Profitten beregnes som den samlede indtjening, hvor den producerede energi i hvert tidsinterval multipliceres med den tidsafhængige  elpris (i DKK/kWh).  Energipriserne varierer time for time, og I kan hente disse data via API'et fra Energidataservice.dk.

Profitfunktionen $P(\theta_p,\phi_p)$ kan formuleres som:

\begin{equation*}
   P(\theta_p,\phi_p) = \eta\,L\,B \int_{\text{år}} \left[ \text{Flux}(t,\theta_p,\phi_p) \cdot \text{Pris}(t) \right] dt,
\end{equation*}

hvor $L\,B \text{Flux}(t,\theta_p,\phi_p)$ (i W) fx omregnes til kWh per tidsinterval, hvis $\text{Pris}(t)$ er elprisen i DKK/kWh for det givne tidsinterval.  
 
1. Udled og/eller implementér profitfunktionen $P(\theta_p,\phi_p)$ for et helt kalenderår (brug fx data fra 2024), hvor elpriserne varierer time for time.  
2. Bestem den optimale panelevinkel $\theta_p$ og $\phi_p$ som maksimerer profitten $P$.  
3. Diskutér, hvordan den tidsvarierende prisstruktur kan ændre den optimale orientering sammenlignet med optimering udelukkende på basis af energiproduktionen. Eksempelvis om det kan betale sig at justere panelets azimutvinkel, så der produceres mere energi i tidsrummet med høje elpriser.
 
  
**Forudsætninger og antagelser:**  
- Brug de samme modeller for flux og solpositionsberegninger, som tidligere. 
- Prisdata for el kan hentes via API'et på [Energidataservice.dk](https://www.energidataservice.dk/guides/api-guides).  
- Vi antager at strømmen kan sælges uden omkostninger (afgifter, transport, m.m. ignoreres) for en pris $\text{Pris}(t)$ der afhænger lineært af spotprisen (for DK1).  


**Kort guide til hentning af prisdata:**  
- Undersøg dokumentationen på Energidataservice.dk for at finde endpointet til timepriser.  
- I Python kan I eksempelvis bruge biblioteket `requests` til at sende en GET-forespørgsel. Et simpelt eksempel kunne være:
  ```python
  import requests
  import pandas as pd

  endpoint = "https://api.energidataservice.dk/dataset/elspotprices"
  params = {
      "start": "2024-01-01T00:00",
      "end": "2024-12-31T23:00",
      "filter": '{"PriceArea":["DK2"]}'  # <-- fixed JSON string
  }

  response = requests.get(endpoint, params=params)
  data = response.json()
  df = pd.DataFrame(data['records'])
  # Konverter evt. enheder (øre/kroner, kWh/J/MJ) hvis nødvendigt.
  print(df.head(20))
  ```
- Integrer herefter de hentede timepriser i profitfunktionen $\text{Pris}(t)$.  
 

+++

## Valgfrie udvidelser

+++

### Medregn atmosfærisk attenuering

+++

Den nuværende model antager, at solens irradians $S_0$ er konstant (f.eks. 1100 W/m²) for alle tidspunkter, hvor solen er over horisonten. Det betyder, at hvis et solpanel er orienteret, så $\pmb{u}_p$ er parallel med solens stråler, vil det modtage samme flux – uanset tidspunktet på dagen, fx solopgang eller middag. Men i virkeligheden er det ikke tilfældet:

- *Atmosfærisk attenuering:* Især ved solopgang og solnedgang skal solens stråler passere en længere strækning gennem atmosfæren, hvilket medfører øget spredning og absorption. Dette reducerer den faktiske irradiance, som panelet modtager.
- *Temperatur og spektral fordeling:* Solens stråling kan ændre karakter afhængigt af tidspunktet på dagen – for eksempel er den kortbølgede del af solens spektrum mere intens omkring middagstid, hvilket påvirker panelernes effektivitet.
- *Air Mass-effekt:* Den såkaldte "air mass" (luftmasse) er et udtryk for, hvor meget atmosfæren solens stråler skal gennemtrænge. Ved lav solhøjde er luftmassen større, og derfor vil den effektive irradians være lavere end ved høj solhøjde (omkring middagstid).

For at gøre modellen mere realistisk, kan I overveje at inkludere en attenueringsfaktor, der afhænger af solens højde (eller air mass). Dermed vil en orientering mod solen ved solopgang ikke give samme flux som ved middagstid, selvom panelets orientering er "optimal" i den forstand, at det rammes direkte af solens stråler.

+++

### Solenergi ved kolonialisering af Mars og Europa (Jupiters måne)

Antag, at vi ønsker at optimere udbyttet af solpaneler ved en eventuel kolonialisering af Mars – og dernæst undersøge potentialet for solenergi ved en kolonialisering af Europa (Jupiters måne).  I den nuværende model anvendes solens irradians $S_0$​ som en konstant værdi (f.eks. 1100 W/m²) for Jorden. Hvordan skal $S_0$​ justeres for Mars og Europa ud fra [invers-kvadratsætningen](https://en.wikipedia.org/wiki/Inverse-square_law), givet at fx Mars’ gennemsnitlige afstand til solen er ca. 1.524 gange Jordens afstand? Besvar følgende:

1. **For Mars:**  
   - Udregn den nye solirradians $S_{\text{Mars}}$ på Mars ved hjælp af invers-kvadratsætningen, givet at Mars’ gennemsnitlige afstand til Solen er ca. 1,524 gange Jordens afstand:
     \begin{equation*}
     S_{\text{Mars}} = S_{\text{Jorden}} \times \left(\frac{d_{\text{Jorden}}}{d_{\text{Mars}}}\right)^2.
     \end{equation*}
   - Diskutér, hvordan den lavere irradiance påvirker den samlede energiproduktion fra solpaneler på Mars, og hvilke yderligere faktorer (fx Mars’ tynde atmosfære, støvstorme og temperaturudsving) der skal tages i betragtning.

2. **For Europa (Jupiters Måne):**  
   - Udregn den forventede solirradians $S_{\text{Europa}}$ for Europa, idet den gennemsnitlige afstand til Solen for Jupiters system er ca. 5,2 gange Jordens afstand:
     \begin{equation*}
     S_{\text{Europa}} = S_{\text{Jorden}} \times \left(\frac{d_{\text{Jorden}}}{d_{\text{Europa}}}\right)^2.
     \end{equation*}
   - Diskutér, om den beregnede irradiance på Europa giver et realistisk grundlag for udnyttelse af solenergi. Tag højde for udfordringer som mangel på en tæt atmosfære, overfladeegenskaber og den høje strålingsbelastning fra Jupiter.

3. **Sammenfatning:**  
   - Sammenlign de beregnede værdier for $S_{\text{Mars}}$ og $S_{\text{Europa}}$ med Jordens irradiance $S_{\text{Jorden}}$ (fx 1100 W/m² under ideelle forhold).  
   - Diskutér, hvordan reduktionen i solirradiansen påvirker design og placering af solpaneler i de to koloniseringsscenarier, og om solenergi kan være en bæredygtig energikilde under disse forhold.

+++

```{hint}
:class: dropdown
Anvend følgende formel for begge beregninger:
\begin{equation*}
S_{\text{ny}} = S_{\text{Jorden}} \times \left(\frac{d_{\text{Jorden}}}{d_{\text{ny}}}\right)^2,
\end{equation*}
hvor $d_{\text{ny}}$ er den gennemsnitlige afstand til Solen for den pågældende himmellegeme (1 AU for Jorden, 1,524 AU for Mars, og ca. 5,2 AU for Europa).
```

+++

### Medregn skygge fra et træ eller bygning

+++

I det horizontale koordinatsystem placeres fx en trækrone i en given afstand, fx 10 m.  Betragt sfæren $r_{træ}=10m$ med centrum i Origo (panelets position) og beskriv træet form på denne sfæren. En simpel model er som følger: Antag at der kun er to muligheder: enten $0\%$ skygge eller $100 \%$ skygge. Udregn overfladearealet af hele sfæren som funktion af $r_{træ}$, antag en størrelse af trækronen (fx dens omtrentlige diameter) og udregn hvor man zenit og azimut-grader træet cirka skygger. Dette kunne være at der er $100 \%$ skygge når $\theta \in [70,80]$ og $\phi \in [150,160]$, og energioptaget skal derfor fraregnes når solen befinder sig i dette interval. Træets form bliver noget unaturlig når man bruger akseparalle områder i $(\theta,\phi)$-planen. Hvilken form svarer det til på sfæren $r_{træ}=10m$? Diskuter hvor stor effekt skygger fra træer og bygninger kan have. Er det muligt at beskrive en kuglerund trækrone? Hvordan vil denne form se ud på sfæren $r_{træ}$?

I kan alternativt modellere skygge fra en nabobygning. Ideen er den samme men skygge-intervallet for $\theta$ bør gå helt ned til jorden, dvs $\theta = 90$. Afhængig af bygningsstørrelse og afstand til solpanel, kan vinkel-intervallerne meget vel blive større, fx $\theta \in [65,90]$. I kan finde inspiration med dette værktøj:  https://www.findmyshadow.com/

+++

### Mere om optimering

+++

1. **Er sydvendt panel optimalt?** Det må det jo være, men lad os undersøge det matematisk. I opgaven ovenfor antog vi $\phi_p = 180^\circ$. I skal nu droppe denne antagelser og udregne panelets energiproduktion som funktion af både $\phi_p$ og $\theta_p$. 
1. **Et panel med motor:**  Antag at solpanelets vinkel kan justeres enten hver dag, hver måned, eller hver kvartal. Hvis I fx vælger hver måned, så skal den optimale vinkel for hver måned angives, og panelet årlige effekt skal derefter udregnes. Sammenlign den årlige effekt med effekten for en tilsvarende fastmonteret panel. Diskuter om det kan betale sig at have solpanelanlæg med paneler hvis vinkel på denne måde kan justeres.

+++

## Kilder

+++

1. https://www.pveducation.org/
1. https://www.acs.org/education/resources/highschool/chemmatters/past-issues/archive-2013-2014/how-a-solar-cell-works.html
1. https://assessingsolar.org/intro.html
1. https://en.wikipedia.org/wiki/Horizontal_coordinate_system
1. https://en.wikipedia.org/wiki/Solar_irradiance


<!-- 
#### Medregn energipriser og forbrugsmønstre

I stedet for at maksimere den årlige energiproduktion for den valgte solpanelsopsætning, kan det være relevant af minimere parcelhuset årlige energiomkostninger. Find et typisk årligt energiforbrug for et standard parcelhus', gerne med data time for time. Find tilsvarende tal med timepriserne for energi. Energiforbruget og energipriserne er typisk høje i tidsintervallet 17-20 og højere om vinteren end sommeren. Hvis I ikke kan finde relevante data, så må I antage et forbrug og et priser, fx at priserne er dobbelt så høje i tidsrummet 17-20 end resten af dagen. Find de optimale vinkler $\theta_p$ og $\phi_s$, der minimere energiomkostningerne ud fra det angivne forbrug. I bør specielt være opmærksomme på $\phi_s$, da det er meget muligt at det kan betale sig at dreje panelerne mod vest for at få mest energi ud af aftensolen hvor energipriserne og forbruget er højt. 

Priserne time-for-time for 2020 kan findes i: <a href="../_assets/elspot-prices_2020_hourly_dkk.xlsx">denne fil</a>.
-->