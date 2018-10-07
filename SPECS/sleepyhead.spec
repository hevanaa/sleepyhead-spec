%global debug_package %{nil}

Name:           sleepyhead
Version:        1.1.0
Release:        0.1.20180614git8e6968f%{?dist}
Summary:        Sleep tracking software for monitoring CPAP treatment
Group:          Applications/Engineering
License:        GPLv3
URL:            https://sleepyhead.jedimark.net/
# The source of this package was pulled from upstreams's vcs.
# Use the following command to generate the tar ball:
# git clone https://gitlab.com/sleepyhead/sleepyhead-code.git
# tar cvjf %{name}-%{version}.tar.bz2 sleepyhead-code/
Source0:        %{name}-%{version}.tar.bz2

# Upstream provides none of the following files
Source1:        sleepyhead.desktop
Source2:        sleepyhead.appdata.xml
Source3:        sleepyhead.1

BuildRequires:  qt5-qtwebkit-devel >= 5.9.0
BuildRequires:  qt5-qtserialport-devel >= 5.9.0
BuildRequires:  qt5-qttools-devel >= 5.9.0
%if 0%{?fedora}
BuildRequires:  quazip-qt5-devel
%endif
%if 0%{?rhel}
BuildRequires: 	quazip-devel
%endif
BuildRequires:  zlib-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  libX11-devel
BuildRequires:  glibc-devel
BuildRequires:  libstdc++-devel

BuildRequires:  qt5-linguist
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
BuildRequires:  icoutils

Requires:       qt5-qtwebkit >= 5.9.0
Requires:       qt5-qtserialport >= 5.9.0

%description
Review and explore data produced by CPAP and related machines. Currently
supported CPAP machines:
Philips Respironics (System One, Dreamstation), ResMed (S9, AirSense 10,
AirCurve 10), DeVilbiss (Intellipap CPAP/Auto), Fisher & Paykel (ICON, ICON+),
Weinmann (Somnobalance).
Oximetry devices:
Contec CMS50D+/E/F/I oximeters (and clones like Pulox), ResMed (S9, 10-series
Oximeter Adapter), PRS1 Oximeter attachment, ChoiceMMed MD300W1 Oximeter.


%prep
%setup -q -n sleepyhead-code

%build
qmake-qt5
make %{?_smp_mflags}

# Convert ico file to separate freedesktop style icons
icotool -x sleepyhead/icons/bob-v3.0.ico -o sleepyhead/icons/

%install
install -Dm 0755 sleepyhead/SleepyHead $RPM_BUILD_ROOT%{_bindir}/sleepyhead

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

install -Dpm 0644                                                             \
%{SOURCE2} %{buildroot}%{_datadir}/appdata/sleepyhead.appdata.xml
appstream-util                                                                \
validate-relax --nonet %{buildroot}%{_datadir}/appdata/sleepyhead.appdata.xml

install -Dpm 0644 %{SOURCE3} %{buildroot}%{_mandir}/man1/sleepyhead.1

# install icons
num=( 1 2 3 4 5 )
pxl=( 16 32 48 64 128 )
for (( i=0; i<${#num[@]}; i++ )); do
install -Dpm 0644                                                             \
sleepyhead/icons/bob-v3.0_${num[$i]}_${pxl[$i]}x${pxl[$i]}x32.png             \
%{buildroot}%{_datadir}/icons/hicolor/${pxl[$i]}x${pxl[$i]}/apps/sleepyhead.png
done

install -d %{buildroot}%{_datadir}/sleepyhead/translations
install -pm 0644 -t                                                          \
%{buildroot}%{_datadir}/sleepyhead/translations/ sleepyhead/translations/*.qm


%post
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :


%postun
if [ $1 -eq 0 ]; then
    touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%license COPYING
%doc README
%{_bindir}/*
%{_datadir}/applications/sleepyhead.desktop
%{_datadir}/appdata/sleepyhead.appdata.xml
%{_datadir}/icons/hicolor/*/apps/sleepyhead.png
%{_datadir}/sleepyhead/
%{_mandir}/man1/sleepyhead.1*



%changelog
* Sun Oct 7 2018 Johan Heikkila <johan.heikkila@gmail.com> - 1.1.0-0.1.20180614git8e6968f
- Updated to 1.1.0-unstable-2
* Wed Nov 15 2017 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.13.20160426git0e04bd9
- Fixed build on Fedora 27
* Fri Jul 07 2017 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.12.20160426git0e04bd9
- Fixed build on Fedora 26 and corrected the snapshot date
* Sun Nov 27 2016 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.11.20160703git0e04bd9
- Workaround to build on Fedora 25 and qt 5.7
* Sat Jul 23 2016 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.10.20160703git0e04bd9
- Changed build script to also build on Epel
* Sat Jul 23 2016 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.9.20160703git0e04bd9
- Updated Finnish translation
* Tue Jul 19 2016 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.8.20160703git0e04bd9
- Cleaned up spec file
* Sun Jul 17 2016 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.7.20160703git0e04bd9
- Added man page and patch from Debian package
* Fri Jul 15 2016 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.6.20160703git0e04bd9
- Cleaned up BuildRequires, Requires and Patches
* Tue Jul 12 2016 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.5.20160703git0e04bd9
- Minor corrections to build
* Mon Jul 04 2016 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.4.20160703git0e04bd9
- Minor corrections to build
* Mon Jul 04 2016 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.3.20160703git0e04bd9
- Hopefully more compliant spec file. Added appdata.xml
* Sun Jul 03 2016 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.2.20160704git6b1c125
- Updated Fedora build files
* Sat Jun 25 2016 Johan Heikkila <johan.heikkila@gmail.com> - 1.0.0-0.0.git20160625
- Updated Fedora package from Warren's spec and latest git source
* Fri Feb 01 2013 Warren Togami <wtogami@gmail.com> - 0.9.3-0.0.git20130201
- Initial Fedora package
