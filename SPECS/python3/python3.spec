Summary:        A high-level scripting language
Name:           python3
Version:        3.7.5
Release:        11%{?dist}
License:        PSF
URL:            http://www.python.org/
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
%define sha1    Python=860f88886809ae8bfc86afa462536811c347a2a1
Patch0:         cgi3.patch
Patch1:         python3-support-photon-platform.patch
Patch2:         CVE-2019-17514.patch
Patch3:         CVE-2019-18348.patch
Patch4:         CVE-2020-8492.patch
Patch5:         CVE-2020-14422.patch
Patch6:         CVE-2019-20907.patch
Patch7:         CVE-2020-26116.patch
Patch8:         CVE-2020-27619.patch
Patch9:         CVE-2021-3177.patch
Patch10:        CVE-2021-23336.patch

BuildRequires:  pkg-config >= 0.28
BuildRequires:  bzip2-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  readline-devel
BuildRequires:  xz-devel
BuildRequires:  expat-devel >= 2.1.0
BuildRequires:  libffi-devel >= 3.0.13
BuildRequires:  sqlite-devel
Requires:       ncurses
Requires:       openssl
Requires:       python3-libs = %{version}-%{release}
Requires:       readline
Requires:       xz
Provides:       python-sqlite
Provides:       python(abi)
Provides:       /usr/bin/python
Provides:       /bin/python
Provides:       /bin/python3

%if %{with_check}
BuildRequires:  iana-etc
BuildRequires:  tzdata
BuildRequires:  curl-devel
%endif

%description
The Python 3 package contains a new version of Python development environment.
Python 3 brings more efficient ways of handling dictionaries, better unicode
strings support, easier and more intuitive syntax, and removes the deprecated
code. It is incompatible with Python 2.x releases.

%package libs
Summary: The libraries for python runtime
Group: Applications/System
Requires:       (coreutils or toybox)
Requires:       expat >= 2.1.0
Requires:       libffi >= 3.0.13
Requires:       ncurses
Requires:       sqlite-libs
Requires:       bzip2-libs


%description    libs
The python interpreter can be embedded into applications wanting to
use python as an embedded scripting language.  The python-libs package
provides the libraries needed for python 3 applications.

%package        xml
Summary:        XML libraries for python3 runtime
Group:          Applications/System
Requires:       python3-libs = %{version}-%{release}
Requires:       python3 = %{version}-%{release}

%description    xml
The python3-xml package provides the libraries needed for XML manipulation.

%package        curses
Summary:        Python module interface for NCurses Library
Group:          Applications/System
Requires:       python3-libs = %{version}-%{release}
Requires:       ncurses

%description    curses
The python3-curses package provides interface for ncurses library.

%package        devel
Summary: The libraries and header files needed for Python development.
Group:          Development/Libraries
Requires:       python3 = %{version}-%{release}
Requires:       expat-devel >= 2.1.0
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts: python3 < %{version}-%{release}

%description    devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package        tools
Summary:        A collection of development tools included with Python.
Group:          Development/Tools
Requires:       python3 = %{version}-%{release}

%description    tools
The Python package includes several development tools that are used
to build python programs.

%package        setuptools
Summary:        Download, build, install, upgrade, and uninstall Python packages.
Group:          Development/Tools
BuildArch:      noarch
Requires:       python3 = %{version}-%{release}

%description    setuptools
setuptools is a collection of enhancements to the Python distutils that allow you to more easily build and distribute Python packages, especially ones that have dependencies on other packages.

%package test
Summary: Regression tests package for Python.
Group: Development/Tools
Requires: python3 = %{version}-%{release}

%description test
The test package contains all regression tests for Python as well as the modules test.support and test.regrtest. test.support is used to enhance your tests while test.regrtest drives the testing suite.

%prep
%setup -q -n Python-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
export OPT="${CFLAGS}"
%configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --enable-shared \
    --with-system-expat \
    --with-system-ffi \
    --with-dbmliborder=gdbm:ndbm
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
chmod -v 755 %{buildroot}%{_libdir}/libpython3.7m.so.1.0
%{_fixperms} %{buildroot}/*
ln -sf libpython3.7m.so %{buildroot}%{_libdir}/libpython3.7.so

# Remove unused stuff
find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete
find %{buildroot}%{_libdir} -name '*.o' -delete
rm %{buildroot}%{_bindir}/2to3

%check
make  %{?_smp_mflags} test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-, root, root)
%doc LICENSE README.rst
%{_bindir}/pydoc*
%{_bindir}/pyvenv*
%{_bindir}/python3
%{_bindir}/python3.7
%{_bindir}/python3.7m
%{_mandir}/*/*

%dir %{_libdir}/python3.7
%dir %{_libdir}/python3.7/site-packages

%{_libdir}/libpython3.so
%{_libdir}/libpython3.7.so
%{_libdir}/libpython3.7m.so.1.0


%exclude %{_libdir}/python3.7/ctypes/test
%exclude %{_libdir}/python3.7/distutils/tests
%exclude %{_libdir}/python3.7/sqlite3/test
%exclude %{_libdir}/python3.7/idlelib/idle_test
%exclude %{_libdir}/python3.7/test
%exclude %{_libdir}/python3.7/lib-dynload/_ctypes_test.*.so
%exclude %{_bindir}/pip3
%exclude %{_bindir}/pip3.7
%exclude %{_libdir}/python3.7/site-packages/pip/*
%exclude %{_libdir}/python3.7/site-packages/pip-19.2.3.dist-info/*

%files libs
%defattr(-,root,root)
%doc LICENSE README.rst
%{_libdir}/python3.7
%{_libdir}/python3.7/site-packages/easy_install.py
%{_libdir}/python3.7/site-packages/README.txt
%exclude %{_libdir}/python3.7/site-packages/
%exclude %{_libdir}/python3.7/ctypes/test
%exclude %{_libdir}/python3.7/distutils/tests
%exclude %{_libdir}/python3.7/sqlite3/test
%exclude %{_libdir}/python3.7/idlelib/idle_test
%exclude %{_libdir}/python3.7/test
%exclude %{_libdir}/python3.7/lib-dynload/_ctypes_test.*.so
%exclude %{_libdir}/python3.7/xml
%exclude %{_libdir}/python3.7/lib-dynload/pyexpat*.so
%exclude %{_libdir}/python3.7/curses
%exclude %{_libdir}/python3.7/lib-dynload/_curses*.so
%exclude %{_libdir}/python3.7/distutils/command/wininst-*.exe

%files  xml
%{_libdir}/python3.7/xml/*
%{_libdir}/python3.7/lib-dynload/pyexpat*.so

%files  curses
%{_libdir}/python3.7/curses/*
%{_libdir}/python3.7/lib-dynload/_curses*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/python-3.7.pc
%{_libdir}/pkgconfig/python-3.7m.pc
%{_libdir}/pkgconfig/python3.pc
%{_libdir}/libpython3.7m.so
%{_bindir}/python3-config
%{_bindir}/python3.7-config
%{_bindir}/python3.7m-config

%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files tools
%defattr(-,root,root,755)
%doc Tools/README
%{_bindir}/2to3-3.7
%exclude %{_bindir}/idle*

%files setuptools
%defattr(-,root,root,755)
%{_libdir}/python3.7/site-packages/pkg_resources/*
%{_libdir}/python3.7/site-packages/setuptools/*
%{_libdir}/python3.7/site-packages/setuptools-41.2.0.dist-info/*
%{_bindir}/easy_install-3.7

%files test
%{_libdir}/python3.7/test/*

%changelog
*   Tue Mar 02 2021 Piyush Gupta <gpiyush@vmware.com> 3.7.5-11
-   Fix CVE-2021-23336
*   Tue Feb 16 2021 Tapas Kundu <tkundu@vmware.com> 3.7.5-10
-   Packages python3-pip as separate spec
*   Fri Jan 01 2021 Shreyas B. <shreyasb@vmware.com> 3.7.5-9
-   Fix CVE-2021-3177
*   Thu Nov 05 2020 Tapas Kundu <tkundu@vmware.com> 3.7.5-8
-   Fix CVE-2020-27619
*   Mon Oct 12 2020 Tapas Kundu <tkundu@vmware.com> 3.7.5-7
-   Fix CVE-2020-26116
*   Thu Aug 06 2020 Tapas Kundu <tkundu@vmware.com> 3.7.5-6
-   Do not package /usr/lib/python3.7/lib2to3 in tools
*   Mon Jul 20 2020 Tapas Kundu <tkundu@vmware.com> 3.7.5-5
-   Fix for CVE-2019-20907
*   Wed Jul 01 2020 Tapas Kundu <tkundu@vmware.com> 3.7.5-4
-   Address CVE-2020-14422
*   Thu Apr 02 2020 Tapas Kundu <tkundu@vmware.com> 3.7.5-3
-   Fix for CVE-2020-8492
*   Thu Mar 26 2020 Tapas Kundu <tkundu@vmware.com> 3.7.5-2
-   Fix CVE-2019-18348
*   Sun Nov 10 2019 Tapas Kundu <tkundu@vmware.com> 3.7.5-1
-   Updated to 3.7.5 patch release
*   Tue Nov 05 2019 Tapas Kundu <tkundu@vmware.com> 3.7.4-4
-   Fix CVE-2019-17514
*   Wed Oct 23 2019 Tapas Kundu <tkundu@vmware.com> 3.7.4-3
-   Fix conflict of libpython3.so
*   Mon Oct 21 2019 Shreyas B. <shreyasb@vmware.com> 3.7.4-2
-   Fixed makecheck errors.
*   Thu Oct 17 2019 Tapas Kundu <tkundu@vmware.com> 3.7.4-1
-   Updated to patch release 3.7.4
-   Fix CVE-2019-16935
*   Wed Sep 11 2019 Tapas Kundu <tkundu@vmware.com> 3.7.3-3
-   Fix CVE-2019-16056
*   Mon Jun 17 2019 Tapas Kundu <tkundu@vmware.com> 3.7.3-2
-   Fix for CVE-2019-10160
*   Mon Jun 10 2019 Tapas Kundu <tkundu@vmware.com> 3.7.3-1
-   Update to Python 3.7.3 release
*   Thu May 23 2019 Tapas Kundu <tkundu@vmware.com> 3.7.0-6
-   Fix for CVE-2019-5010
*   Tue Mar 12 2019 Tapas Kundu <tkundu@vmware.com> 3.7.0-5
-   Fix for CVE-2019-9636
*   Mon Feb 11 2019 Taps Kundu <tkundu@vmware.com> 3.7.0-4
-   Fix for CVE-2018-20406
*   Fri Dec 21 2018 Tapas Kundu <tkundu@vmware.com> 3.7.0-3
-   Fix for CVE-2018-14647
*   Tue Dec 04 2018 Tapas Kundu <tkundu@vmware.com> 3.7.0-2
-   Excluded windows installer from python3 libs packaging.
*   Wed Sep 26 2018 Tapas Kundu <tkundu@vmware.com> 3.7.0-1
-   Updated to version 3.7.0
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.6.1-9
-   Requires coreutils or toybox
-   Requires bzip2-libs
*   Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 3.6.1-8
-   Remove devpts mount in check
*   Mon Aug 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-7
-   Add pty for tests to pass
*   Wed Jul 12 2017 Xiaolin Li <xiaolinl@vmware.com> 3.6.1-6
-   Add python3-test package.
*   Fri Jun 30 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-5
-   Remove the imaplib tests.
*   Mon Jun 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.6.1-4
-   Added pip, setuptools, xml, and curses sub packages.
*   Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 3.6.1-3
-   Fix symlink and script
*   Wed May 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.6.1-2
-   Exclude idle3.
*   Wed Apr 26 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.6.1-1
-   Updating to latest
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.5.3-3
-   Python3-devel requires expat-devel.
*   Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-2
-   Provides /bin/python3.
*   Tue Feb 28 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-1
-   Updated to version 3.5.3.
*   Fri Jan 20 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.5.1-10
-   Added patch to support Photon OS
*   Tue Dec 20 2016 Xiaolin Li <xiaolinl@vmware.com> 3.5.1-9
-   Move easy_install-3.5 to devel subpackage.
*   Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 3.5.1-8
-   Use sqlite-{devel,libs}
*   Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> 3.5.1-7
-   Patch for CVE-2016-5636
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 3.5.1-6
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.1-5
-   GA - Bump release of all rpms
*   Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 3.5.1-4
-   Edit scriptlets.
*   Wed Apr 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.1-3
-   update python to require python-libs
*   Thu Apr 07 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.5.1-2
-   Providing python3 binaries instead of the minor versions.
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.5.1-1
-   Updated to version 3.5.1
*   Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 3.4.3-3
-   Edit post script.
*   Mon Aug 17 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3-2
-   Remove python.o file, and minor cleanups.
*   Wed Jul 1 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3
-   Add Python3 package to Photon.