# Modified spec file from the librelamp project.
# Build a hobbled LibreSSL (like OpenSSL) but provide only static libraries to
# allow those who are baking LibreSSL into their application to do so, but not
# to conflict with the hosts OpenSSL.  If anything, this should only appear as
# a BuildRequires.

# Mainly ignoring man pages and the openssl/oscpcheck binaries
%define _unpackaged_files_terminate_build 0
%define ssldir %{_sysconfdir}/pki/tls

Name:		libressl
Version:	2.7.4
Release:	2%{?dist}
Summary:	OpenBSD fork of the OpenSSL Cryptography Suite

Group:		System Environment/Libraries
License:	OpenSSL
URL:		http://www.libressl.org/

Source0: 	libressl-%{version}-hobbled.tar.gz
Patch0: 	libressl-2.7.4-ecparam-no-ec2m.patch


#From the README.md
%description
LibreSSL is a fork of OpenSSL 1.0.1g developed by the OpenBSD project.
Our goal is to modernize the codebase, improve security, and apply best
practice development processes from OpenBSD.

%package static
Summary:	Static Libraries for LibreSSL
Group:		Development/Libraries
Requires:	ca-certificates >= 2008-5
Conflicts:	openssl-devel

#After first line is from the README.md
%description static
This package provides the static libraries and development header files for LibreSSL.

LibreSSL is API compatible with OpenSSL 1.0.1, but does not yet include all
new APIs from OpenSSL 1.0.2 and later. LibreSSL also includes APIs not yet
present in OpenSSL. The current common API subset is OpenSSL 1.0.1.

LibreSSL it is not ABI compatible with any release of OpenSSL, or necessarily
earlier releases of LibreSSL. You will need to relink your programs to
LibreSSL in order to use it, just as in moving between major versions of
OpenSSL.

LibreSSL's installed library version numbers are incremented to account for
ABI and API changes.

%global debug_package %{nil}

%prep
%setup
%patch0 -p1


%build
export CFLAGS="-DOPENSSL_NO_EC2M -fPIC"
%configure \
  --with-openssldir=%{ssldir} \
  --disable-shared 

##%% from RHEL/CentOS OpenSSL spec file ##%%
# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY $RPM_LD_FLAGS"

make %{?_smp_mflags}


%check
make check


%install
make install DESTDIR=%{buildroot}
install -d %{buildroot}%{ssldir}/csr
install -d %{buildroot}%{ssldir}/cert_bundle


%clean
rm -rf %{buildroot}

%files static
%defattr(-,root,root,-)
%dir %{ssldir}/certs
%dir %{ssldir}/csr
%dir %{ssldir}/cert_bundle
%attr(0644,root,root) %config(noreplace) %{ssldir}/cert.pem
%attr(0644,root,root) %config(noreplace) %{ssldir}/openssl.cnf
%attr(0644,root,root) %config(noreplace) %{ssldir}/x509v3.cnf

%{_includedir}/tls.h
%{_includedir}/openssl/*.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_prefix}/%{_lib}/pkgconfig/*.pc

%doc COPYING README.md ChangeLog VERSION
%license COPYING


%changelog
* Sat Jul 14 2018 Richard Clarke <rsclrk@pm.me> 2.7.4-2
- Forked to build and provide static libraries only.

* Sun Jun 17 2018 Alice Wonder <buildmaster@librelamp.com> 2.7.4-1
- Update to 2.7.4

* Wed Feb 07 2018 Alice Wonder <buildmaster@librelamp.com> 2.6.4-1.0
- Nuke the 1024 dh parameters

* Sat Feb 03 2018 Alice Wonder <buildmaster@librelamp.com> 2.6.4-1
- Update to 2.6.4

* Thu Sep 28 2017 Alice Wonder <buildmaster@librelamp.com> 2.5.5-2.1
- Change default ECC curves

* Mon Sep 25 2017 Alice Wonder <buildmaster@librelamp.com> 2.5.5-1
- Update to 2.5.5

* Wed Feb 01 2017 Alice Wonder <buildmaster@librelamp.com> 2.4.5-1
- Update to 2.4.5

* Sat Dec 10 2016 Alice Wonder <buildmaster@librelamp.com> 2.4.4-3
- Mass rebuild for CentOS 7.3 rebase
- Move cron.weekly script into cron.monthly

* Fri Nov 11 2016 Alice Wonder <buildmaster@librelamp.com> 2.4.4-2
- install the MODP IKE DH groups

* Mon Nov 07 2016 Alice Wonder <buildmaster@librelamp.com> 2.4.4-1
- Update to 2.4.4

* Tue Sep 27 2016 Alice Wonder <buildmaster@librelamp.com> 2.4.3-1
- Update to 2.4.3

* Sat Aug 06 2016 Alice Wonder <buildmaster@librelamp.com> 2.4.2-2
- Added compat-openssl package

* Tue Aug 02 2016 Alice Wonder <buildmaster@librelamp.com> 2.4.2-1
- Update to 2.4.2

* Thu Jul 07 2016 Alice Wonder <buildmaster@librelamp.com> 2.3.6-1
- Update to 2.3.6

* Tue May 03 2016 Alice Wonder <buildmaster@librelamp.com> 2.3.4-1
- Update to 2.3.4

* Wed Mar 23 2016 Alice Wonder <buildmaster@librelamp.com> 2.3.3-1
- Update to 2.3.3

* Sun Feb 21 2016 Alice Wonder <buildmaster@librelamp.com> 2.3.2-1
- Update to 2.3.2

* Wed Jan 06 2016 Alice Wonder <buildmaster@librelamp.com> 2.3.1-2
- Don't apply disable ssl2 handshake patch

* Thu Nov 19 2015 Alice Wonder <buildmaster@librelamp.com> 2.3.1-1
- Update to 2.3.1

* Sat Oct 03 2015 Alice Wonder <buildmaster@librelamp.com> 2.3.0-1
- Update to 2.3.0

* Wed Sep 09 2015 Alice Wonder <buildmaster@librelamp.com> 2.2.3-3
- cron script to daily generate fresh DH Parameters

* Fri Sep 04 2015 Alice Wonder <buildmaster@librelamp.com> 2.2.3-2
- Patch to disable SSL2 handshake

* Sun Aug 30 2015 Alice Wonder <buildmaster@librelamp.com> 2.2.3-1
- Update to 2.2.3

* Wed Aug 12 2015 Alice Wonder <buildmaster@librelamp.com> 2.2.2-2
- add /etc/pki/tls/{csr,cert_bundle}

* Fri Aug 07 2015 Alice Wonder <buildmaster@librelamp.com> 2.2.2-1
- Build against official release tarball
- libressl.1 man page fixes

* Thu Aug 06 2015 Alice Wonder <buildmaster@librelamp.com> 2.2.2-0.1.test
- fix libressl.cnf so it works with mod_ssl post scriptlet

* Wed Aug 05 2015 Alice Wonder <buildmaster@librelamp.com> 2.2.2-0.0.test
- fix libressl.1 man page to refer to libressl as the binary
- patch to use libressl.conf as default configuration file.

* Tue Aug 04 2015 Alice Wonder <buildmaster@librelamp.com> 2.2.1-1.1
- don't use own sub-directiory of _libdir

* Mon Aug 03 2015 Alice Wonder <buildmaster@librelamp.com> 2.2.1-1
- Initial spec file

