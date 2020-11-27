Summary:        Distributed reliable key-value store
Name:           etcd
Version:        3.4.10
Release:        3%{?dist}
License:        Apache License
URL:            https://github.com/etcd-io/etcd/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1 etcd=582e5b6410fca84aacd2f3c0307373cffc2461c3
Source1:        etcd.service
%ifarch aarch64
Source2:        etcd.sysconfig
%endif
BuildRequires:  go >= 1.12
BuildRequires:  git

%description
A highly-available key value store for shared configuration and service discovery.

%prep
%setup -q

%build
./build

%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}/%{_docdir}/%{name}-%{version}
install -vdm755 %{buildroot}/lib/systemd/system
%ifarch aarch64
install -vdm 0755 %{buildroot}%{_sysconfdir}/sysconfig
%endif
install -vdm 0755 %{buildroot}%{_sysconfdir}/etcd
install -vpm 0755 -T etcd.conf.yml.sample %{buildroot}%{_sysconfdir}/etcd/etcd-default-conf.yml

chown -R root:root %{buildroot}%{_bindir}
chown -R root:root %{buildroot}/%{_docdir}/%{name}-%{version}

mv %{_builddir}/%{name}-%{version}/bin/etcd %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-%{version}/bin/etcdctl %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-%{version}/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/
mv %{_builddir}/%{name}-%{version}/etcdctl/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/README-etcdctl.md
mv %{_builddir}/%{name}-%{version}/etcdctl/READMEv2.md %{buildroot}/%{_docdir}/%{name}-%{version}/READMEv2-etcdctl.md

install -vdm755 %{buildroot}/lib/systemd/system-preset
echo "disable etcd.service" > %{buildroot}/lib/systemd/system-preset/50-etcd.preset

cp %{SOURCE1} %{buildroot}/lib/systemd/system
%ifarch aarch64
cp %{SOURCE2} %{buildroot}/etc/sysconfig/etcd
%endif
install -vdm755 %{buildroot}/var/lib/etcd

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%{_bindir}/etcd*
/%{_docdir}/%{name}-%{version}/*
/lib/systemd/system/etcd.service
/lib/systemd/system-preset/50-etcd.preset
%dir /var/lib/etcd
%config(noreplace) %{_sysconfdir}/etcd/etcd-default-conf.yml
%ifarch aarch64
%config(noreplace) %{_sysconfdir}/sysconfig/etcd
%endif

%changelog
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 3.4.10-3
-   Bump up version to compile with new go
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 3.4.10-2
-   Bump up version to compile with new go
*   Tue Aug 11 2020 Ashwin H <ashwinh@vmware.com> 3.4.10-1
-   Update to 3.4.10
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 3.4.3-2
-   Bump up version to compile with go 1.13.3-2
*   Tue Jan 14 2020 Ashwin H <ashwinh@vmware.com> 3.4.3-1
-   Update to 3.4.3
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 3.3.13-2
-   Bump up version to compile with go 1.13.3
*   Thu Oct 17 2019 Anish Swaminathan <anishs@vmware.com> 3.3.13-1
-   Upgraded to version 3.3.13, fix CVE-2018-16886
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 3.3.9-3
-   Bump up version to compile with new go
*   Mon Feb 25 2019 Keerthana K <keerthanak@vmware.com> 3.3.9-2
-   Add env variable ETCD_UNSUPPORTED_ARCH=arm64 for arm to start etcd service.
*   Fri Sep 21 2018 Sujay G <gsujay@vmware.com> 3.3.9-1
-   Bump etcd version to 3.3.9
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.1.5-4
-   Remove shadow requires
*   Sun Aug 27 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.1.5-3
-   File based configuration for etcd service.
*   Wed May 31 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.1.5-2
-   Provide preset file to disable service by default
*   Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 3.1.5-1
-   Upgraded to version 3.1.5, build from sources
*   Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 3.0.9-1
-   Upgraded to version 3.0.9
*   Fri Jun 24 2016 Xiaolin Li <xiaolinl@vmware.com> 2.3.7-1
-   Upgraded to version 2.3.7
*   Wed May 25 2016 Nick Shi <nshi@vmware.com> 2.2.5-3
-   Changing etcd service type from simple to notify
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.5-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.2.5-1
-   Upgraded to version 2.2.5
*   Tue Jul 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.1-2
-   Adding etcd service file
*   Tue Jul 21 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.1.1-1
-   Update to version etcd v2.1.1
*   Tue Mar 10 2015 Divya Thaluru <dthaluru@vmware.com> 2.0.4-1
-   Initial build.  First version
