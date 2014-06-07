%{!?__pecl:	%{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir:	%{expand: %%global php_extdir %(php-config --extension-dir)}}

%global pecl_name oauth

Name:		php-pecl-oauth	
Version:	1.2.3
Release:	5%{?dist}
Summary:	PHP OAuth consumer extension
Group:		Development/Languages
License:	BSD
URL:		http://pecl.php.net/package/oauth
Source0:	http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	php-devel
Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}

BuildRequires:	php-pear
Requires(post):	%{__pecl}
Requires(postun):	%{__pecl}

Provides:	php-pecl(%{pecl_name}) = %{version}

BuildRequires:	libcurl-devel
BuildRequires:	pcre-devel

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


%description
OAuth is an authorization protocol built on top of HTTP which allows 
applications to securely access data without having to store
usernames and passwords.

%prep
%setup -q -c

%build
cd %{pecl_name}-%{version}
phpize
%configure
make %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/php.d
cat > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

mkdir -p %{buildroot}%{pecl_xmldir}
install -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%clean
rm -rf %{buildroot}

%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi

%check
cd %{pecl_name}-%{version}
php -n \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so \
    --modules | grep OAuth

%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/LICENSE %{pecl_name}-%{version}/examples
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 1.2.3-3
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 02 2012 F. Kooman <fkooman@tuxed.net> - 1.2.3-1
- update to 1.2.3, bugfix, see 
  http://pecl.php.net/package-changelog.php?package=oauth&release=1.2.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-3
- build against php 5.4
- fix filters

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 F. Kooman <fkooman@tuxed.net> - 1.2.2-1
- Update to 1.2.2 (really fix RHBZ #724872 this time)

* Fri Jul 22 2011 F. Kooman <fkooman@tuxed.net> - 1.2.1-1
- update to 1.2.1 (RHBZ #724872). See
  http://pecl.php.net/package-changelog.php?package=oauth&release=1.2.1

* Sun Jul 03 2011 F. Kooman <fkooman@tuxed.net> - 1.2-1
- upgrade to 1.2

* Sun Jun 19 2011 F. Kooman <fkooman@tuxed.net> - 1.1.0-6
- add fix for http://pecl.php.net/bugs/bug.php?id=22337

* Mon Jun 13 2011 F. Kooman <fkooman@tuxed.net> - 1.1.0-5
- remove php_apiver marco, was not used

* Mon Jun 13 2011 F. Kooman <fkooman@tuxed.net> - 1.1.0-4
- add minimal check to see if module loads
- fix private-shared-object-provides rpmlint warning

* Sat Jun 11 2011 F. Kooman - 1.1.0-3
- BR pcre-devel

* Sat May 28 2011 F. Kooman - 1.1.0-2
- require libcurl for cURL request engine support 

* Sat May 28 2011 F. Kooman - 1.1.0-1
- initial package 
