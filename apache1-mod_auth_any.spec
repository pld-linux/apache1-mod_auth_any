%define		mod_name	auth_any
%define 	apxs		/usr/sbin/apxs
Summary:	Basic authentication for the Apache Web server using arbitrary shell commands
Summary(cs):	Základní autentizace pro WWW server Apache pomocí shellových pøíkazù
Summary(da):	En autenticeringsmodul for webtjeneren Apache hvor man kan bruge vilkårlige skal-kommandoer
Summary(de):	Authentifizierung für den Apache Web-Server, der arbiträre Shell-Befehle verwendet
Summary(fr):	Authentification de base pour le serveur Web Apache utilisant des commandes shell arbitraires
Summary(it):	Autenticazione di base per il server Web Apache mediante comandi arbitrari della shell
Summary(no):	En autentiseringsmodul for webtjeneren Apache der en kan bruke skall-kommandoer
Summary(pl):	Podstawowy modu³ autentykacji dla Apache, u¿ywaj±cy poleceñ pow³oki
Summary(pt):	Um módulo de autenticação de LDAP para o servidor Web Apache
Summary(sl):	Osnovna avtentikacija za spletni stre¾nik Apache, z uporabo poljubnih lupinskih ukazov
Summary(sv):	Grundläggande autentisering för webbservern Apache med valfria skalkommandon
Name:		apache-mod_%{mod_name}
Version:	1.3
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.itlab.musc.edu/pub/toolbox/mod_%{mod_name}/mod_%{mod_name}-%{version}.tar.gz
URL:		http://www.itlab.musc.edu/~nafees/mod_%{mod_name}.html
Prereq:		%{_sbindir}/apxs
Requires:	apache(EAPI)
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This module allows you to use any command line program (such as
webNIS) to authenticate a user.

%description -l cs
Balíèek mod_auth_any slou¾í pro omezení pøístupu k dokumentùm, které
poskytuje WWW server Apache. Jména a hesla jsou kontrolována pomocí
jakéhokoliv pøíkazu (jeho návratovým kódem).

%description -l de
Mod_auth_any kann verwendet werden, um den Zugriff auf von einem Web-
Server bediente Dokumente zu beschränken, indem es den Rückcode eines
gegebenen arbiträren Befehls prüft.

%description -l es
Mod_auth_any puede usarse para limitar el acceso a documentos servidos
desde un servidor web verificando el código de retorno de un comando
arbitrario especificado.

%description -l fr
Mod_auth_any peut être utilisé pour limiter l'accès à des documents
servis par un serveur Web en vérifiant le code de retour d'une
commande spécifiée arbitraire.

%description -l it
Mod_auth_any può essere utilizzato per limitare l'accesso ai documenti
serviti da un server Web controllando il codice di ritorno di un dato
comando arbitrario.

%description -l ja
Mod_auth_any ¤ÏÇ¤°Õ¤Ë»ØÄê¤µ¤ì¤¿¥³¥Þ¥ó¥É¤ÎÌá¤ê¥³¡¼¥É¤ò¥Á¥§¥Ã¥¯¤¹¤ë¤³¤È
¤Ë¤è¤Ã¤Æ¡¢Web ¥µ¡¼¥Ð¡¼¤¬Äó¶¡¤¹¤ë¥É¥­¥å¥á¥ó¥È¤Ø¤Î¥¢¥¯¥»¥¹¤òÀ©¸Â¤¹¤ë¤³¤È
¤¬¤Ç¤­¤Þ¤¹¡£

%description -l pl
Ten modu³ pozwala na u¿ycie dowolnego programu dzia³aj±cego z linii
poleceñ (jak np. webNIS) do autentykacji u¿ytkownika.

%description -l sv
Mod_auth_any kan användas för att begränsa åtkomsten till dokument
servade av en webbserver genom att kontrollera returkoden från ett
godtyckligt angivet kommando.

%prep
%setup -q -n mod_%{mod_name}

%build
%{apxs} -c src/mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%attr(755,root,root) %{_pkglibdir}/*
