Summary:    nghttp2 is an implementation of HTTP/2 and its header compression algorithm, HPACK.
Name:       nghttp2
Version:    1.41.0
Release:    2%{?dist}
License:    MIT
URL:        https://nghttp2.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution: Photon
Source0:	https://github.com/nghttp2/nghttp2/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha1 nghttp2=809b2f948d02e271adc498d8ef225d30509dc0d0

BuildRequires: c-ares-devel
BuildRequires: openssl-devel
BuildRequires: systemd
BuildRequires: zlib-devel
BuildRequires: libxml2-devel
BuildRequires: libevent-devel
BuildRequires: jansson-devel

%description
Implementation of the Hypertext Transfer Protocol version 2 in C.

%package devel
Summary: Header files for nghttp2
#Requires: %{name}
Requires: %{name} = %{version}-%{release}

%description devel
These are the header files of nghttp2.

%prep
%setup -q

%build
autoreconf -i
%configure  \
    --disable-static \
    --enable-lib-only \
    --disable-python-bindings

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm %{buildroot}/%{_libdir}/*.la

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_datadir}/nghttp2
%{_docdir}/%{name}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Wed Jun 24 2020 Tapas Kundu <tkundu@vmware.com> 1.41.0-2
-   Used configure macro and removed whitespaces
*   Thu Jun 11 2020 Ashwin H <ashwinh@vmware.com> 1.41.0-1
-   Upgrade to version 1.41.0
*   Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.33.0-1
-   Upgrade to version 1.33.0
*   Tue Jun 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.23.1-1
-   First version