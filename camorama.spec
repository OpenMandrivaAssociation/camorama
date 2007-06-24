%define name camorama
%define version 0.17
%define release %mkrel 3

Name: %{name}
Summary: A GNOME webcam application
Version: %{version}
Release: %{release}
License: GPL
Group: Video
URL: http://camorama.fixedgear.org
Source: %{name}-%{version}.tar.bz2
Source1: %{name}-16.png.bz2
Source2: %{name}-32.png.bz2
Source3: %{name}-48.png.bz2
Patch0: camorama-gcc4.patch.bz2
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: libgnomeui2-devel libglade2.0-devel 
BuildRequires: png-devel

%description
camorama is a program for controlling webcams. It is able to capture to various
image formats, as well as saving to a local dir or a FTP server on the web.
Right now you can change the video settings using the gui and apply some
filters. 

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q

%patch0 -p1

%build
%configure2_5x
%make

%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

# Menu
mkdir -p %buildroot/%_menudir
cat > %buildroot/%_menudir/%name  <<EOF
?package(%name): command="%_bindir/%name" needs="X11" \
icon="%name.png" section="Multimedia/Video" \
title="Camorama" longtitle="A GNOME webcam application" \
startup_notify="true"
EOF

# icon
install -d $RPM_BUILD_ROOT/%{_miconsdir}
install -d $RPM_BUILD_ROOT/%{_iconsdir}
install -d $RPM_BUILD_ROOT/%{_liconsdir}
bzcat %{SOURCE1} > $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
bzcat %{SOURCE2} > $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
bzcat %{SOURCE3} > $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

%{find_lang} %{name}

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
%{_menudir}/*
%_miconsdir/*.png
%_iconsdir/*.png
%_liconsdir/*.png


%clean
rm -rf $RPM_BUILD_ROOT
