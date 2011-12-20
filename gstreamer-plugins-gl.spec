#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
#
%define		gstname gst-plugins-gl
%define		gst_major_ver   0.10
%define		gst_req_ver	0.10.28
%define		gstpb_req_ver	0.10.28
#
%include	/usr/lib/rpm/macros.gstreamer
#
Summary:	GStreamer Streaming-media framework plug-in for OpenGL
Summary(pl.UTF-8):	Wtyczka OpenGL do środowiska strumieni multimedialnych GStreamer
Name:		gstreamer-plugins-gl
Version:	0.10.2
Release:	4
License:	LGPL v2+
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gst-plugins-gl/%{gstname}-%{version}.tar.bz2
# Source0-md5:	878fe4199be1c94f8aa2f7f23891cc95
URL:		http://gstreamer.net/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.10
%{?with_apidocs:BuildRequires:	docbook-dtd412-xml}
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glew-devel >= 1.4.0
BuildRequires:	glib2-devel >= 1:2.6
BuildRequires:	gstreamer-devel >= %{gst_req_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_req_ver}
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.6}
BuildRequires:	libpng-devel >= 1.0
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
BuildRequires:	python >= 2.1
BuildRequires:	rpmbuild(macros) >= 1.470
Requires:	gstreamer >= %{gst_req_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_req_ver}
Obsoletes:	gstreamer-imagesink-gl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module contains integration library and plug-in for using OpenGL
within GStreamer pipelines.

%description -l pl.UTF-8
Ten moduł zawiera bibliotekę i wtyczkę pozwalające na używanie
OpenGL-a w potokach GStreamera.

%package devel
Summary:	Include files for GStreamer streaming-media framework OpenGL API
Summary(pl.UTF-8):	Pliki nagłówkowe API OpenGL dla środowiska strumieni multimedialnych GStreamer
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenGL-GLU-devel
Requires:	glew-devel >= 1.4.0
Requires:	gstreamer-devel >= %{gst_req_ver}
Requires:	gstreamer-plugins-base-devel >= %{gstpb_req_ver}

%description devel
Include files for GStreamer streaming-media framework OpenGL API.

%description devel -l pl.UTF-8
Pliki nagłówkowe API OpenGL dla środowiska strumieni multimedialnych
GStreamer.

%package apidocs
Summary:	GStreamer streaming-media framework OpenGL API documentation
Summary(pl.UTF-8):	Dokumentacja API OpenGL dla środowiska strumieni multimedialnych GStreamer
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GStreamer streaming-media framework OpenGL API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API OpenGL dla środowiska strumieni multimedialnych
GStreamer.

%prep
%setup -q -n %{gstname}-%{version}

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-examples \
	--disable-silent-rules \
	--disable-static \
	--%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_major_ver}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README RELEASE TODO
%attr(755,root,root) %{_libdir}/libgstgl-%{gst_major_ver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstgl-%{gst_major_ver}.so.1
%attr(755,root,root) %{_libdir}/gstreamer-%{gst_major_ver}/libgstopengl.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgstgl-%{gst_major_ver}.so
%{_includedir}/gstreamer-%{gst_major_ver}/gst/gl
%{_pkgconfigdir}/gstreamer-gl-%{gst_major_ver}.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gst-plugins-gl-libs-%{gst_major_ver}
%{_gtkdocdir}/gst-plugins-gl-plugins-%{gst_major_ver}
%endif
