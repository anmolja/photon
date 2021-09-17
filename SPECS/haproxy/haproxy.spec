Summary:        A fast, reliable HA, load balancing, and proxy solution.
Name:           haproxy
Version:        2.0.10
Release:        3%{?dist}
License:        GPL
URL:            http://www.haproxy.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.haproxy.org/download/2.0/src/%{name}-%{version}.tar.gz
%define sha1 haproxy=7a81094c367621a981012480cebc7c152c482d75
Patch0:         haproxy-CVE-2020-11100.patch
Patch1:         haproxy-CVE-2021-40346.patch
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  lua-devel
BuildRequires:  pkg-config
BuildRequires:  zlib-devel
BuildRequires:  systemd
BuildRequires:  systemd-devel
Requires:       systemd

%description
HAProxy is a fast and reliable solution offering high availability, load
balancing, and proxying for TCP and HTTP-based applications. It is suitable
for very high traffic web-sites.

%package        doc
Summary:        Documentation for haproxy
%description    doc
It contains the documentation and manpages for haproxy package.
Requires:       %{name} = %{version}-%{release}

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
make %{?_smp_mflags} TARGET=linux-glibc USE_PCRE=1 USE_OPENSSL=1 \
        USE_GETADDRINFO=1 USE_ZLIB=1 USE_SYSTEMD=1
make %{?_smp_mflags} -C contrib/systemd
sed -i s/"local\/"/""/g contrib/systemd/haproxy.service
sed -i "s/\/run/\/var\/run/g" contrib/systemd/haproxy.service
sed -i "s/192.168.1.22/127.0.0.0/g" examples/transparent_proxy.cfg

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} PREFIX=%{_prefix} DOCDIR=%{_docdir}/haproxy TARGET=linux-glibc install
install -vDm755 contrib/systemd/haproxy.service \
       %{buildroot}/usr/lib/systemd/system/haproxy.service
install -vDm644 examples/transparent_proxy.cfg  %{buildroot}/%{_sysconfdir}/haproxy/haproxy.cfg

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/systemd/system/haproxy.service
%config(noreplace) %{_sysconfdir}/haproxy/haproxy.cfg

%files doc
%defattr(-,root,root,-)
%{_docdir}/haproxy/*
%{_mandir}/*

%changelog
*   Fri Sep 17 2021 Nitesh Kumar <kunitesh@vmware.com> 2.0.10-3
-   Fix CVE-2021-40346
*   Mon Apr 06 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.10-2
-   Fix CVE-2020-11100
*   Fri Dec 06 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.10-1
-   Update to version 2.0.10
*   Thu Oct 31 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.6-1
-   Update to version 2.0.6 to fix CVE-2019-18277
*   Thu Aug 01 2019 Kuladeep Rayalla <krayalla@vmware.com> 2.0.3-2
-   Retain the current configuration while updating haproxy to next version
*   Fri Jul 26 2019 Kuladeep Rayalla <krayalla@vmware.com> 2.0.3-1
-   Update to version 2.0.3
*   Tue Jun 25 2019 Ashwin H <ashwinh@vmware.com> 2.0.0-1
-   Update to 2.0.0
*   Tue Apr 2 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-1
-   Update to 1.9.6
*   Thu Feb 28 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.14-3
-   Patch for CVE_2018_20102
-   Patch for CVE_2018_20103
*   Tue Jan 29 2019 Ajay Kaher <akaher@vmware.com> 1.8.14-2
-   Build with USE_SYSTEMD=1 to fix service startup.
*   Tue Dec 04 2018 Ajay Kaher <akaher@vmware.com> 1.8.14-1
-   Update to version 1.8.14
*   Tue Apr 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.6.12-1
-   Updated to version 1.6.12
*   Sun Nov 27 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.10-1
-   Upgrade to 1.6.10 to address CVE-2016-5360
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.3-3
-   GA - Bump release of all rpms
*   Fri May 20 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.3-2
-   Add haproxy-systemd-wrapper to package, add a default configuration file.
*   Mon Feb 22 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.3-1
-   Updated to version 1.6.3
*   Thu Oct 01 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.5.14-1
-   Add haproxy v1.5 package.

