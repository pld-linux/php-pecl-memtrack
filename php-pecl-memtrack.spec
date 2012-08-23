%define		modname	memtrack
%define		status		beta
Summary:	%{modname} - watch memory consumption in PHP scripts
Summary(pl.UTF-8):	%{modname} - monitorowanie zużycia pamięci w skryptach PHP
Name:		php-pecl-%{modname}
Version:	0.2.1
Release:	3
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	6cdf83e24fab5982a3c264ce12503d12
Source1:	%{name}.ini
URL:		http://pecl.php.net/package/memtrack/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
memtrack is a PHP extension that tracks memory consumption in PHP
scripts and produces reports (warnings) when memory usage reaches
certain levels set by the user.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
memtrack to rozszerzenie PHP śledzące zużycie pamięci w skryptach PHP
i generujące raport (ostrzeżenia) w przypadku przekroczenia
określonych przez użytkownika wartości.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
