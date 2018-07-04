#
#TODO
# - check which simd instructions can be enabled (like in qt spec)
#   patched qt does not compile with mmx, sse and sse2 enabled
#
# Conditional build:
%bcond_without	patchedQt	# build against Qt4 modified by wkhtmltopdf project
%bcond_with	qt5		# build against Qt5
#

%define		qt_ver	4.8.7

Summary:	Programs capable of converting HTML documents into images or PDF documents
Summary(pl.UTF-8):	Programy do konwersji dokumentów HTML do obrazów lub dokumentów PDF
Name:		wkhtmltopdf
Version:	0.12.5
Release:	1
License:	LGPL v3+ (library), GPL v3+ (utilities)
Group:		Applications/Graphics
Source0:	https://github.com/wkhtmltopdf/wkhtmltopdf/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	653b68fd0eccfa05d4016fe87f6abcc9
Source1:	http://download.qt-project.org/official_releases/qt/4.8/%{qt_ver}/qt-everywhere-opensource-src-%{qt_ver}.tar.gz
# Source1-md5:	d990ee66bf7ab0c785589776f35ba6ad
#git clone https://github.com/wkhtmltopdf/qt.git; git diff origin/4.8..wk_4.8.7 > qt.patch
Patch0:		qt.patch
URL:		http://wkhtmltopdf.org/
%if %{with patchedQt}
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.1.3
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libstdc++-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	zlib-devel
%else
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
BuildRequires:	Qt5PrintSupport-devel >= 5.2
BuildRequires:	Qt5Svg-devel >= 5
BuildRequires:	Qt5WebKit-devel >= 5
BuildRequires:	Qt5XmlPatterns-devel >= 5
BuildRequires:	qt5-qmake
%else
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
BuildRequires:	QtNetwork-devel >= 4
BuildRequires:	QtSvg-devel >= 4
BuildRequires:	QtWebKit-devel >= 4
BuildRequires:	QtXmlPatterns-devel >= 4
BuildRequires:	qt4-qmake
%endif
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Programs capable of converting HTML documents into images or PDF
documents.

%description -l pl.UTF-8
Programy do konwersji dokumentów HTML do obrazów lub dokumentów PDF.

%package devel
Summary:	Header files for wkhtmltox library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki wkhtmltox
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%if %{with qt5}
Requires:	Qt5Core-devel >= 5
Requires:	Qt5Network-devel >= 5
Requires:	Qt5WebKit-devel >= 5
%else
Requires:	QtCore-devel >= 4
Requires:	QtNetwork-devel >= 4
Requires:	QtWebKit-devel >= 4
%endif

%description devel
Header files for wkhtmltox library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki wkhtmltox.

%prep
%setup -q %{?with_patchedQt: -a1}

%if %{with patchedQt}
cd qt-everywhere-opensource-src-%{qt_ver}
%patch0 -p1
# change QMAKE FLAGS to build
%{__sed} -i -e '
	s|QMAKE_CC.*=.*gcc|QMAKE_CC\t\t= %{__cc}|;
	s|QMAKE_CXX.*=.*g++|QMAKE_CXX\t\t= %{__cxx}|;
	s|QMAKE_LINK.*=.*g++|QMAKE_LINK\t\t= %{__cxx}|;
	s|QMAKE_LINK_SHLIB.*=.*g++|QMAKE_LINK_SHLIB\t= %{__cxx}|;
	s|QMAKE_CFLAGS_RELEASE.*|QMAKE_CFLAGS_RELEASE\t+= %{rpmcppflags} %{rpmcflags}|;
	s|QMAKE_CXXFLAGS_RELEASE.*|QMAKE_CXXFLAGS_RELEASE\t+= %{rpmcppflags} %{rpmcxxflags}|;
	s|QMAKE_CFLAGS_DEBUG.*|QMAKE_CFLAGS_DEBUG\t+= %{debugcflags}|;
	s|QMAKE_CXXFLAGS_DEBUG.*|QMAKE_CXXFLAGS_DEBUG\t+= %{debugcflags}|;
	' mkspecs/common/g++-base.conf
%endif

%build

%if %{with patchedQt}
export OPTFLAGS="%{rpmcflags}"
mkdir -p build_qt
cd build_qt
qt_prefix=`pwd`

../qt-everywhere-opensource-src-%{qt_ver}/configure \
	-opensource \
	-confirm-license \
	-fast \
	-release \
	-static \
	-graphicssystem raster \
	-webkit \
	-exceptions \
	-xmlpatterns \
	-system-zlib \
	-system-libpng \
	-system-libjpeg \
	-no-libmng \
	-no-libtiff \
	-no-accessibility \
	-no-stl \
	-no-qt3support \
	-no-phonon \
	-no-phonon-backend \
	-no-opengl \
	-no-declarative \
	-no-script \
	-no-scripttools \
	-no-sql-ibase \
	-no-sql-mysql \
	-no-sql-odbc \
	-no-sql-psql \
	-no-sql-sqlite \
	-no-sql-sqlite2 \
	-no-mmx \
	-no-3dnow \
	-no-sse \
	-no-sse2 \
	-no-sse3 \
	-no-ssse3 \
	-no-sse4.1 \
	-no-sse4.2 \
	-no-avx \
	-no-multimedia \
	-nomake demos \
	-nomake docs \
	-nomake examples \
	-nomake tools \
	-nomake tests \
	-nomake translations \
	-silent \
	-xrender \
	-largefile \
	-iconv \
	-openssl-linked \
	-no-javascript-jit \
	-no-rpath \
	-no-dbus \
	-no-nis \
	-no-cups \
	-no-pch \
	-no-gtkstyle \
	-no-nas-sound \
	-no-sm \
	-no-xshape \
	-no-xinerama \
	-no-xcursor \
	-no-xfixes \
	-no-xrandr \
	-no-mitshm \
	-no-xinput \
	-no-xkb \
	-no-glib \
	-no-gstreamer \
	-no-icu \
	-no-openvg \
	-no-xsync \
	-no-audio-backend \
	-no-neon \
	-prefix "$qt_prefix"

%{__make}

cd ..

$qt_prefix/bin/qmake \
%else
qmake-%{?with_qt5:qt5}%{!?with_qt5:qt4} \
%endif
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir}}

%{__make} install \
        INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix}

if [ ! -d "$RPM_BUILD_ROOT%{_libdir}" ]; then
  mv $RPM_BUILD_ROOT{%{_prefix}/lib,%{_libdir}}
fi

rm -f $RPM_BUILD_ROOT%{_libdir}/libwkhtmltox.so.0.12

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/wkhtmltoimage
%attr(755,root,root) %{_bindir}/wkhtmltopdf
%attr(755,root,root) %{_libdir}/libwkhtmltox.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwkhtmltox.so.0
%{_mandir}/man1/wkhtmlto*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwkhtmltox.so
%{_includedir}/wkhtmltox
