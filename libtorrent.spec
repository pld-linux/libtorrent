#
# Conditional build:
%bcond_without	static_libs	# don't build static library
%bcond_without	ipv6		# disable IPv6 support
#
Summary:	LibTorrent - a BitTorrent library written in C++ for Unix
Summary(pl.UTF-8):	LibTorrent - biblioteka BitTorrenta napisana w C++ dla Uniksa
Name:		libtorrent
# keep stable line, see URL below
Version:	0.13.6
Release:	3
Epoch:		1
License:	GPL v2+
Group:		Libraries
Source0:	http://rtorrent.net/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	66f18044432a62c006c75f6d0bb4d7dc
Patch0:		%{name}-client_list.patch
Patch1:		%{name}-build.patch
Patch2:		libtorrent-bencoded-error.patch
URL:		https://github.com/rakshasa/rtorrent/wiki
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	cppunit-devel >= 1.9.6
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibTorrent is a BitTorrent library written in C++ for *nix, with a
focus on high performance and good code. The library differentiates
itself from other implementations by transfering directly from file
pages to the network stack. On high-bandwidth connections it is able
to seed at 3 times the speed of the official client.

%description -l pl.UTF-8
LibTorrent to biblioteka BitTorrenta napisana w C++ dla Uniksa. Jest
zaprojektowana aby uniknąć nadmiarowego kopiowania buforów i danych,
będącego wadą większości (wszystkich?) innych implementacji
BitTorrenta. Biblioteka jest jednowątkowa, klient obsługuje pętlę
select.

%package devel
Summary:	Development files for libtorrent
Summary(pl.UTF-8):	Pliki programistyczne libtorrent
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel
Requires:	openssl-devel >= 0.9.7d
Requires:	zlib-devel

%description devel
Development files for libtorrent.

%description devel -l pl.UTF-8
Pliki programistyczne libtorrent.

%package static
Summary:	Static libtorrent library
Summary(pl.UTF-8):	Statyczna biblioteka libtorrent
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static libtorrent library.

%description static -l pl.UTF-8
Statyczna biblioteka libtorrent.

%prep
v=%{version}; IFS=.; set -- $v
if [ $(($2 % 2)) = 0 ]; then
	echo "WARNING Version %{version} is probably unstable, check it first!"
	exit 1
fi
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# force refresh
%{__rm} scripts/{libtool,lt*}.m4

%build
%{__libtoolize}
%{__aclocal} -I scripts
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--%{?with_ipv6:en}%{!?with_ipv6:dis}able-ipv6 \
	--%{?debug:en}%{!?debug:dis}able-debug \
	%{?with_static_libs:--enable-static} \
%ifarch i386 i486
	--disable-instrumentation
%endif

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
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libtorrent.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtorrent.so.19

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
