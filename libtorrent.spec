#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	LibTorrent - a BitTorrent library written in C++ for Unix
Summary(pl):	LibTorrent - biblioteka BitTorrenta napisana w C++ dla Uniksa
Name:		libtorrent
Version:	0.9.1
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	622c448cd73d1c15963c0ae709d5335d
Patch0:		%{name}-inttypes.patch
URL:		http://libtorrent.rakshasa.no/
BuildRequires:	automake
BuildRequires:	libsigc++-devel >= 2.0
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibTorrent is a BitTorrent library written in C++ for Unix. It is
designed to avoid the redundant buffers and data copying that most
(all?) other BitTorrent implementations suffer from. The library is
single-threaded and the client handles the select loop.

%description -l pl
LibTorrent to biblioteka BitTorrenta napisana w C++ dla Uniksa. Jest
zaprojektowana aby unikn±æ nadmiarowego kopiowania buforów i danych,
bêd±cego wad± wiêkszo¶ci (wszystkich?) innych implementacji
BitTorrenta. Biblioteka jest jednow±tkowa, klient obs³uguje pêtlê
select.

%package devel
Summary:	Development files for libtorrent
Summary(pl):	Pliki programistyczne libtorrent
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libsigc++-devel >= 2.0
Requires:	openssl-devel >= 0.9.7d

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
%patch0 -p1

%build
cp /usr/share/automake/config.sub .
%configure \
	--%{?debug:en}%{!?debug:dis}able-debug \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtorrent.a
%endif
