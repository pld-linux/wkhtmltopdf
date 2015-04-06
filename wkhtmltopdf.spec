#
# Conditional build:
%bcond_with	qt5	# build against Qt5
#
Summary:	Programs capable of converting HTML documents into images or PDF documents
Summary(pl.UTF-8):	Programy do konwersji dokumentów HTML do obrazów lub dokumentów PDF
Name:		wkhtmltopdf
Version:	0.12.2.1
Release:	2
License:	LGPL v3+ (library), GPL v3+ (utilities)
Group:		Applications/Graphics
Source0:	https://github.com/wkhtmltopdf/wkhtmltopdf/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f3a665a462f4939fa31dfd3ef1d3231d
URL:		http://wkhtmltopdf.org/
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
%setup -q

%build
qmake-%{?with_qt5:qt5}%{!?with_qt5:qt4} \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

install -p bin/wkhtmlto* $RPM_BUILD_ROOT%{_bindir}
cp -dp bin/libwkhtmltox.so{,.?,.*.*.*} $RPM_BUILD_ROOT%{_libdir}
cp -pr include/wkhtmltox $RPM_BUILD_ROOT%{_includedir}

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

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwkhtmltox.so
%{_includedir}/wkhtmltox
