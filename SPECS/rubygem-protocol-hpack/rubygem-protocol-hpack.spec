%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-hpack

Name: rubygem-protocol-hpack
Version:        1.4.2
Release:        2%{?dist}
Summary:        A compresssor and decompressor for HTTP 2.0 HPACK.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  protocol-hpack=bbe3c70503214aea46d48113e225c5995128944201ee6cc567dab348aa2bed5da5b4faccf7b3114f8142ae1a9b73a31bdc2bde2947761c7366bf0357dac1282e
BuildRequires:  ruby

BuildArch: noarch

%description
Provides a compressor and decompressor for HTTP 2.0 headers, HPACK, as defined by RFC7541.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.2-2
-   Bump Version to build with new ruby
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.2-1
-   Automatic Version Bump
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.4.1-1
-   Initial build
