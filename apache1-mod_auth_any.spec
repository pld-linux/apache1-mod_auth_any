%define		mod_name	auth_any
Summary:	This is the any authentication module for Apache
Summary(pl):	To jest modu³ dowolnej autentykacji dla Apache
Name:		apache-mod_%{mod_name}
Version:	1.2
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.itlab.musc.edu/pub/toolbox/mod_%{mod_name}/mod_%{mod_name}-%{version}.tar.gz
URL:		http://www.itlab.musc.edu/~nafees/mod_%{mod_name}.html
Prereq:		/usr/sbin/apxs
Requires:	apache(EAPI)
BuildRequires:	/usr/sbin/apxs
BuildRequires:	apache(EAPI)-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(/usr/sbin/apxs -q LIBEXECDIR)

%description
This module allows you to use any command line program (such as
webNIS) to authenticate a user.

%description -l pl
Ten modu³ pozwala na u¿ycie dowolnego programu dzia³aj±cego z linii
poleceñ (jak np. webNIS) do autentykacji u¿ytkownika.

%prep 
%setup -q -n mod_%{mod_name}

%build
/usr/sbin/apxs -c src/mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

gzip -9nf docs/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
%doc docs/*.gz
