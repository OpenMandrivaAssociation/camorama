%define name camorama
%define version 0.19
%define release %mkrel 1

Name: %{name}
Summary: A GNOME webcam application
Version: %{version}
Release: %{release}
License: GPL
Group: Video
URL: http://camorama.fixedgear.org
Source0: %{name}-%{version}.tar.bz2
Source1: %{name}.desktop
BuildRequires: libgnomeui2-devel libglade2.0-devel
BuildRequires: png-devel ImageMagick
BuildRequires: intltool desktop-file-utils

%description
camorama is a program for controlling webcams. It is able to capture to various
image formats, as well as saving to a local dir or a FTP server on the web.
Right now you can change the video settings using the gui and apply some
filters.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q

%build
%configure2_5x
%make

%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

# icon
install -d $RPM_BUILD_ROOT/%{_miconsdir}
install -d $RPM_BUILD_ROOT/%{_iconsdir}
install -d $RPM_BUILD_ROOT/%{_liconsdir}
install -m644 pixmaps/camorama-webcam-16.png $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
convert -sample 32x32 pixmaps/camorama.png $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
install -m644 pixmaps/camorama.png $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png
cp -rf %{SOURCE1} $RPM_BUILD_ROOT/%{_datadir}/applications/

%{find_lang} %{name}

desktop-file-install --vendor="" \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	--remove-category="Applications" \
	--remove-key="X-GNOME-Bugzilla-Component" \
	--remove-category="Graphics" \
	--add-category="Video" \
	--add-category="AudioVideo" \
	--add-category="GNOME" \
	$RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

%post
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/camorama.schemas > /dev/null
%{update_menus}

%preun
if [ "$1" = "0" ]; then
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/camorama.schemas > /dev/null
fi

%postun
%{clean_menus}

%files -f %name.lang
%defattr(-, root, root)
%doc README COPYING ChangeLog NEWS AUTHORS
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/camorama
%_miconsdir/*.png
%_iconsdir/*.png
%_liconsdir/*.png


%clean
rm -rf $RPM_BUILD_ROOT
