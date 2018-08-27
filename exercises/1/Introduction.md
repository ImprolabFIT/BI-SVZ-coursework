# Seznámení se s nástroji pro kurz BI-SVZ
Pro práci na cvičením a později i na domácích úkolech budeme využívat několik nástrojů. 
* [Anaconda](https://www.anaconda.com/) - multiplatformní správce balíčků pro jazyk Python.
* [Jupyter notebook](http://jupyter.org/) - webová aplikace k rychlému prototypování algoritmů v Pythonu.
* Surmon - "krabičková" platforma s algoritmy a rozhraními pro různé druhy kamer.
* [Pylon](https://www.baslerweb.com/en/products/software/basler-pylon-camera-software-suite/) - software sloužící pro práci s kamerami od firmy Basler. 
    
Volba jazyka Python může být pro některé z vás nepochopitelná, zvláště když v bakalářském programu není povinný. Důvod je však prostý. Jazyk Python je v tuto chvíli nejvyužívanější pro obory data science a computer vision. Vývoj v Pythonu je rychlý, jednoduchý a velmi efektivní. Existuje velké množství knihoven, návodů a připravených kódů, které v ostatních jazycích nemají obdoby. Navíc, pokud byste se chtěli zpracování obrazu dále věnovat, stejně byste pravděpodobně skončili právě s Pythonem. Ti z vás, kteří budou pokračovat v magisterském programu Znalostního inženýrství si Pythonem s Jupyter notebooky hojně užijí i později.
    
Cílem tohoto kurzu však není vyučovat jazyk Python, nýbrž zaměřit se právě na samotné metody a algoritmy zpracování obrazu. Python je jen snadná cesta, jak toho snadno ukázat co nejvíc. Naše práce se nebude skládat ani tak z programování v Pythonu, ale převážně z volání již hotových metod a využívání rozhraní (např. OpenCV). Uvidíte sami, že většina úkolů, které budeme řešit, budou velmi předpřipravené a vystačíme si tedy s doplněním pouze několika řádek základního kódu. Mnohem důležitější je porozumění problému a návrh algoritmů/metod k jeho vyřešení.

Stručné základy Pythonu lze nalézt v notebooku [introduction.ipynb](introduction.ipynb). Pro hlubší poznání pak třeba kurz v češtině od [PyLadies](https://naucse.python.cz/course/pyladies/)

## Rozchození virtuálního prostředí pro práci v Pythonu s Jupyter Notebooky
V učebně máme nainstalovaný systém Windows, všechny popsané kroky se tedy budou týkat tohoto systému. Instalace a kroky na Linuxu však probíhájí obdobně. 
K naší práci budeme potřebovat několik balíčku, které je potřeba nainstalovat do virtuálního prostředí. Abychom vám usnadnily život, je možné při vytváření virtuálního prostředí specifikovat soubor [spec-file.txt](spec-file.txt) (pozor funguje jen pro Win x64), který obsahuje seznam potřebných balíčků pro tento kurz. Ty se následně nainstalují. 

### Postup
* Zkontrolujte, zda je u vás na PC nainstalovaná Anaconda. Jinak si ji [stáhněte](https://www.anaconda.com/download)  a nainstalujte (pro Python 3.6).
* Zapněte si Anaconda Prompt, ve kterém je možné využívat Python interpreter, instalovat balíčky a přepínat/modifikovat virtuální prostředí.
* Stáhněte soubor  [spec-file.txt](spec-file.txt) a vytvořte virtuální prostředí s balíčky nutnými pro tento kurz.
	* `conda create --name SVZ --file <cesta k spec-file.txt>`
* Před každým úkolem je nutné zkontrolovat zda nepracujete ve výchozím prostředí (base). Přepnutí do prostředí SVZ:
	* `conda activate SVZ`
	* S aktivovaným prostředím spusťte Jupyter notebook ve složce se soubory ke kurzu
		* `jupyter notebook <cesta k souborum kurzu>` 
*  Otevřete úvodní notebook a zkontrolujte, zda všechny úvodní importy proběhnou bez problému.

Výpis všech virtuálních prostředí lze provést pomocí `conda env list`, výpis balíčku v aktuálním prostředí `conda list`. Deaktivace aktuálního prostředí pomocí `conda deactivate`.  V případě, že chcete nějaké prostředí odstranit, tak `conda env remove --name <nazev>`. Dobrým zvykem je neinstalovat balíčky globálně (do výchozího base prostředí), ale pro každý projekt vytvořit nové virtuální prostředí. Další detaily ke správě prostředí lze nalézt [zde](https://conda.io/docs/user-guide/tasks/manage-environments.html).

## Přípojení a správa kamer v Pylonu 
## Úvod do Surmonu

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTk4NDc0MDg2Miw0Mzk5NDMxOTJdfQ==
-->