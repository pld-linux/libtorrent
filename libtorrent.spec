Summary:	LibTorrent - a BitTorrent library written in C++ for Unix
Summary(pl):	LibTorrent - biblioteka BitTorrenta napisana w C++ dla Uniksa
Name:		libtorrent
Version:	0.6.5
Release:	0.1
License:	GPL v2
Group:		Libraries
Source0:	http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	19546b552dc02a4b78328e5630317a3f
URL:		http://libtorrent.rakshasa.no/
BuildRequires:	libsigc++-devel >= 2.0
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibTorrent is a BitTorrent library written in C++ for Unix. It is
designed to avoid the redundant buffers and data copying that most
(all?) other BitTorrent implementations suffer from. The library is
single-threaded and the client handles the select loop.

%description -l pl
LibTorrent to biblioteka BitTorrenta napisana w C++ dla Uniksa. Jest
zaprojektowana aby unikn�� nadmiarowego kopiowania bufor�w i danych,
b�d�cego wad� wi�kszo�ci (wszystkich?) innych implementacji
BitTorrenta. Biblioteka jest jednow�tkowa, klient obs�uguje p�tl�
select.

%package devel
Summary:	Development files for libtorrent
Summary(pl):	Pliki programistyczne libtorrent
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libsigc++-devel >= 2.0

%description devel
Development files for libtorrent.

%description devel -l pl
Pliki programistyczne libtorrent.

%package static
Summary:	Static libtorrent library
Summary(pl):	Statyczna biblioteka libtorrent
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libtorrent library.

%description static -l pl
Statyczna biblioteka libtorrent.

%prep
%setup -q

%build
%configure \
	--%{?debug:en}%{!?debug:dis}able-debug \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# XXX: is it really needed??? libtool should do this
cd $RPM_BUILD_ROOT%{_libdir}
ln -sf libtorrent.so.*.*.* libtorrent.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/libtorrent.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtorrent.so
%{_libdir}/libtorrent.la
%{_includedir}/torrent
%{_pkgconfigdir}/libtorrent.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtorrent.a
