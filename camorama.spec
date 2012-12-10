Name:		camorama
Summary:	A GNOME webcam application
Version:	0.19
Release:	8
License:	GPLv2
Group:		Video
URL:		http://camorama.fixedgear.org
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Patch0:		camorama-0.19-fixes.patch
Patch1:		camorama-0.19-fix-vl4-header.patch
Patch2:		camorama-0.19-new-glib.patch
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	imagemagick
BuildRequires:	libv4l-devel
BuildRequires:	intltool
BuildRequires:	desktop-file-utils

%description
camorama is a program for controlling webcams. It is able to capture to various
image formats, as well as saving to a local dir or a FTP server on the web.
Right now you can change the video settings using the gui and apply some
filters.

%prep
%setup -q
%patch0 -p1 -b .fixes
%patch1 -p0 -b .v4l
%patch2 -p1 -b .glib

%build
%configure2_5x --disable-schemas-install
%make

%install
%makeinstall_std

# icon
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_liconsdir}
install -m644 pixmaps/camorama-webcam-16.png %{buildroot}%{_miconsdir}/%{name}.png
convert -sample 32x32 pixmaps/camorama.png %{buildroot}%{_iconsdir}/%{name}.png
install -m644 pixmaps/camorama.png %{buildroot}%{_liconsdir}/%{name}.png
cp -rf %{SOURCE1} %{buildroot}%{_datadir}/applications/

%{find_lang} %{name}

desktop-file-install --vendor="" \
	--dir %{buildroot}%{_datadir}/applications \
	--remove-category="Applications" \
	--remove-key="X-GNOME-Bugzilla-Component" \
	--remove-category="Graphics" \
	--add-category="Video" \
	--add-category="AudioVideo" \
	--add-category="GNOME" \
	%{buildroot}%{_datadir}/applications/*.desktop

%preun
%preun_uninstall_gconf_schemas camorama

%files -f %{name}.lang
%doc README COPYING ChangeLog NEWS AUTHORS
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/camorama
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png

