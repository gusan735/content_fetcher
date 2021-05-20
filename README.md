<h1>Introduktion</h1>
Startpunkten på ett webbtjänst vars syfte är att på ett datadrivet och lättillgängligt sätt visa det content jag är intresserad av på fritiden. Grundbultarna är ett antal python-skript som vuxit fram organiskt i en mapp på datorn, men även en vision/idé som jag har funderat på under en tid. 

Exempel på content jag vill visa på sidan:
* Nyheter! Vilka nyheter diskuteras mest just nu i sociala medier? Hur reagerar och kommenterar folk på dessa nyheter, i allmänhet?
* Vilka trender är aktuella just nu på relevanta delar av reddit/flashback?
* Det ska gå att filtrera, söka och visualisera inrapporterade polishändelser på ett smidigt sätt.
* Vilket content finns aktuellt just nu som är associerat till de <b>samhällsprofiler</b> jag är intresserad av? Finns många sociala plattformar att navigera bland. Stort värde i att aggregera data per profil. Uppenbart att det är namnen som drar trafik och intresse oavsett om det är pod/youtube/facebook etc.
* Visualisera ekonomiska/demografiska/politiska eller i övrigt samhällsrelaterade trender som går att mäta över tiden. Hur har ekonomin i min kommun utvecklats på sistone? Hur har skolorna utvecklats? Brottsligheten? Finns massa mätbara trender som kan tillgängliggöras på bättre sätt än idag.

Se Issues för konkreta exempel för vad som ligger i pipen. Denna iteration och detta repo kommer att arkiveras inom kort då jag börjat skissa på en ny approach med mer genomtänkt design och metod. Issues och visionen som helhet följer lyckligtvis med!

<h2>Omfattning</h2>
Hela repot är en sandlåda ala 'quick and dirty'-experimentering rakt igenom. Det finns uppenbara brister i koden över flera dimensioner - vilket jag är smärtsamt medveten om. Det primära syftet har inte varit att skriva snygg, skalbar och vettig kod som faktiskt ska användas i produktion - utan att labba runt i någon form av kreativ process. Koden har byggts på organiskt med tiden, utan någon jättekonkret idé från början. Själva idén har formats under processen och kommer att gestaltas på ett mer genomtänkt sätt i nästa version.


<h2>Algoritmen</h2>
1. Enligt schema, hämta regelbundet data från följande källor:
  * Twitters REST-API: <b>tweet_fetcher.py</b>
  * Öppna data från polisen.se (inrapporterade polishändelser). <b>fetch_events.py</b>
2. Schedulering, import och processing av data hanteras av funktioner i <b>lab_main.py</b>. Tar även hjälp av <b>web_scraper.py</b> för att hämta kompletterande data som inte finns i tillgängliga REST-interface.
3. Data sparas i ett gäng ad hoc-skapade tabeller i en sqlite-fil (project.db)
4. Content presenteras till användare i html/css-format med hjälp av flask-hostad web service.
<h2>Screens</h2>


