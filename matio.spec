%define major 2
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	MAT File I/O Library
Name:		matio
Version:	1.5.2
Release:	2
License:	LGPLv2+
Group:		System/Libraries
Url:		http://sourceforge.net/projects/matio/
Source0:	http://downloads.sourceforge.net/matio/%{name}-%{version}.tar.gz
Patch0:		matio-1.5.0-fix-linking.patch
BuildRequires:	doxygen
BuildRequires:	ghostscript
BuildRequires:	texlive
BuildRequires:	hdf5-devel
BuildRequires:	pkgconfig(zlib)

%description
matio is an ISO C library (with a limited Fortran 90 interface)
for reading and writing Matlab MAT files.

%files
%{_bindir}/matdump

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	MAT File I/O Library
Group:		System/Libraries

%description -n %{libname}
matio is an ISO C library (with a limited Fortran 90 interface)
for reading and writing Matlab MAT files.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Development files and headers for %{name}.

%files -n %{devname}
%doc NEWS README
%{_includedir}/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1

%build
autoreconf -fi
%configure2_5x \
	--enable-shared \
	--disable-static \
	--enable-extended-sparse=yes \
	%if %{_lib} != lib
	--with-libdir-suffix=lib64
	%endif

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%makeinstall_std

rm -rf %{buildroot}%{_docdir}/matio

