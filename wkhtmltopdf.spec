Summary:	Programs capable of converting HTML documents into images or PDF documents
Summary(pl.UTF-8):	Programy do konwersji dokumentów HTML do obrazów lub dokumentów PDF
Name:		wkhtmltopdf
Version:	0.11.0
%define	subver	rc1
Release:	0.%{subver}.1
License:	LGPL v3+ (library), GPL v3+ (utilities)
Group:		Applications/Graphics
#Source0Download: http://code.google.com/p/wkhtmltopdf/downloads/list
Source0:	http://wkhtmltopdf.googlecode.com/files/%{name}-%{version}_%{subver}.tar.bz2
# Source0-md5:	65378cf59698c676fcd6d8f5efd54be6
URL:		http://code.google.com/p/wkhtmltopdf/
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
BuildRequires:	QtNetwork-devel >= 4
BuildRequires:	QtSvg-devel >= 4
BuildRequires:	QtWebKit-devel >= 4
BuildRequires:	qt4-qmake
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
Requires:	QtCore-devel >= 4
Requires:	QtNetwork-devel >= 4
Requires:	QtWebKit-devel >= 4

%description devel
Header files for wkhtmltox library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki wkhtmltox.

%prep
%setup -q -n %{name}-%{version}_%{subver}

%build
qmake-qt4 \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

install bin/wkhtmlto* $RPM_BUILD_ROOT%{_bindir}
cp -dp bin/libwkhtmltox.so{,.?,.*.*.*} $RPM_BUILD_ROOT%{_libdir}
cp -pr include/wkhtmltox $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README_WKHTMLTOIMAGE README_WKHTMLTOPDF
%attr(755,root,root) %{_bindir}/wkhtmltoimage
%attr(755,root,root) %{_bindir}/wkhtmltopdf
%attr(755,root,root) %{_libdir}/libwkhtmltox.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwkhtmltox.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwkhtmltox.so
%{_includedir}/wkhtmltox
