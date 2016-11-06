Name:           sleepyhead
Version:        1.0.0
Release:        0.10.20160703git0e04bd9%{?dist}
Summary:        Sleep tracking software for monitoring CPAP treatment
Group:          Applications/Engineering
License:        GPLv3
URL:            https://sleepyhead.jedimark.net/
# The source of this package was pulled from upstreams's vcs.
# Use the following command to generate the tar ball:
# git clone https://gitlab.com/sleepyhead/sleepyhead-code.git
# tar cvjf %{name}-%{version}.tar.bz2 sleepyhead-code/
Source0:        %{name}-%{version}.tar.bz2

# Upstream ships third party libraries
Patch0:         0001-Fedora-ships-with-quazip.patch
# There	is no qt5 of quazip in	Epel
Patch1:         0001-Epel-ships-with-quazip.patch
# Upstream notified by Debian and patch adapted
Patch2:         0002-Adapt-source-code-to-generate-reproducible-builds.patch
# This has been proposed informally to upstream
Patch3:         0003-Added-translations-path-for-linux.patch
# Translations ongoing
Patch4:         0004-Greek-and-Arabic-translations-not-yet-available.patch
# Informally proposed to upstream
Patch5:         0005-Added-additional-icons-to-ico-file.patch
# Proposed to upstream, waiting for approval
Patch6:         0006-Updated-Swedish-translation.patch
# Proposed to upstream, waiting for approval
Patch7:         0007-Updated-Finnish-translation.patch

# Upstream provides none of the following files
Source1:        sleepyhead.desktop
Source2:        sleepyhead.appdata.xml
Source3:        sleepyhead.1

BuildRequires:  qt5-qtwebkit-devel >= 5.5.0
BuildRequires:  qt5-qtserialport-devel >= 5.5.0
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
BuildRequires:  git
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
BuildRequires:  icoutils

Requires:       qt5-qtwebkit >= 5.5.0
Requires:       qt5-qtserialport >= 5.5.0

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
# Create a git repo within the expanded tarball.
git init
git config user.email "..."
git config user.name "..."
# apply patches
%if 0%{?fedora}
git am %{PATCH0}
%endif
%if 0%{?rhel}
git am %{PATCH1}
%endif
git am %{PATCH2} %{PATCH3} %{PATCH4} %{PATCH5} %{PATCH6} %{PATCH7}


%build
qmake-qt5
make %{?_smp_mflags}
lrelease-qt5 SleepyHeadQT.pro

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
num=( 1 2 3 4 5 6 7 8 )
pxl=( 256 128 64 48 32 24 22 16 )
for (( i=0; i<${#num[@]}; i++ )); do
install -Dpm 0644                                                             \
sleepyhead/icons/bob-v3.0_${num[$i]}_${pxl[$i]}x${pxl[$i]}x32.png             \
%{buildroot}%{_datadir}/icons/hicolor/${pxl[$i]}x${pxl[$i]}/apps/sleepyhead.png
done

install -d %{buildroot}%{_datadir}/sleepyhead/translations
install -pm 0644 -t                                                          \
%{buildroot}%{_datadir}/sleepyhead/translations/ Translations/*.qm


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
