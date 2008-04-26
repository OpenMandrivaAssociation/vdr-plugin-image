
%define plugin	image
%define name	vdr-plugin-%plugin
%define version	0.2.7
%define rel	7

Summary:	VDR plugin: Image Viewer
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	GPL
URL:		http://vdr-image.berlios.de/
Source:		http://download.berlios.de/vdr-image/vdr-%plugin-%version.tar.bz2
Patch0:		image-0.2.7-i18n-1.6.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.6.0
Requires:	vdr-abi = %vdr_abi
BuildRequires:	ffmpeg-devel
BuildRequires:	libexif-devel
Requires:	ImageMagick netpbm jpeg-progs

%description
This VDR plugin allows the display of digital images, like jpeg,
tiff, png, bmp and some more, on the TV screen, using the DVB out
device from vdr.

%prep
%setup -q -n %plugin-%version
%patch0 -p1
%vdr_plugin_prep

%vdr_plugin_params_begin %plugin
# command to mount/unmount/eject image sources
var=MOUNT_CMD
param="-m MOUNT_CMD"
default=imagemount.sh
# command for converting images
var=CONVERT_CMD
param="-c CONVERT_CMD"
default=magickplugin.sh
# configuration data directory
# relative to VDR plugin configuration directory
var=CONFIG_PATH
param=--config=CONFIG_PATH
%vdr_plugin_params_end

%build

for dir in libimage liboutput; do
%make -C $dir $dir.a CFLAGS="%optflags -fPIC" CXXFLAGS="%optflags -fPIC"
done

%vdr_plugin_build

%install
rm -rf %{buildroot}
%vdr_plugin_install

install -d -m755 %{buildroot}%{_bindir}
install -m755 scripts/mount.sh %{buildroot}%{_bindir}/imagemount.sh
install -m755 scripts/imageplugin.sh %{buildroot}%{_bindir}
install -m755 scripts/magickplugin.sh %{buildroot}%{_bindir}

install -d -m755 %{buildroot}%{_vdr_plugin_cfgdir}
install -m644 examples/*.conf %{buildroot}%{_vdr_plugin_cfgdir}

%clean
rm -rf %{buildroot}

%post
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc README HISTORY examples TODO LIESMICH
%{_bindir}/imagemount.sh
%{_bindir}/imageplugin.sh
%{_bindir}/magickplugin.sh
%config(noreplace) %{_vdr_plugin_cfgdir}/*.conf


