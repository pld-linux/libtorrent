#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	LibTorrent - a BitTorrent library written in C++ for Unix
Summary(pl.UTF-8):	LibTorrent - biblioteka BitTorrenta napisana w C++ dla Uniksa
Name:		libtorrent
Version:	0.11.8
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	1e50de4a4f0ee6d9c643993aea9bdbf0
Patch0:		%{name}-client_list.patch
URL:		http://libtorrent.rakshasa.no/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libsigc++-devel >= 2.0
BuildRequires:	libtool >= 2:1.5
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pkgconfig
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
Requires:	%{name} = %{version}-%{release}
Requires:	libsigc++-devel >= 2.0
Requires:	openssl-devel >= 0.9.7d

%description devel
Development files for libtorrent.

%description devel -l pl.UTF-8
Pliki programistyczne libtorrent.

%package static
Summary:	Static libtorrent library
Summary(pl.UTF-8):	Statyczna biblioteka libtorrent
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libtorrent library.

%description static -l pl.UTF-8
Statyczna biblioteka libtorrent.

%prep
%setup -q
%patch0 -p1

# from libtool 1.9f, autoconf 2.60 can't stand it (endless recursion)
rm -f scripts/{libtool,lt*}.m4

%build
%{__libtoolize}
%{__aclocal} -I scripts
%{__autoconf}
%{__autoheader}
%{__automake}

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
%doc AUTHORS README TODO
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
