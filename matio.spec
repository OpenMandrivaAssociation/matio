%define major 4
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	MAT File I/O Library
Name:		matio
Version:	1.5.10
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://sourceforge.net/projects/matio/
Source0:	https://sourceforge.net/projects/matio/files/%{name}-%{version}.tar.gz
BuildRequires:	doxygen
BuildRequires:	ghostscript
BuildRequires:	texlive
BuildRequires:	hdf5-devel
BuildRequires:	pkgconfig(zlib)

%description
matio is an ISO C library (with a limited Fortran 90 interface)
for reading and writing Matlab MAT files.

%files
%doc COPYING
%{_bindir}/matdump

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	MAT File I/O Library
Group:		System/Libraries

%description -n %{libname}
matio is an ISO C library (with a limited Fortran 90 interface)
for reading and writing Matlab MAT files.

%files -n %{libname}
%doc COPYING
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
%doc NEWS README COPYING
%{_includedir}/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*

#----------------------------------------------------------------------------

%prep
%setup -q
%apply_patches

%build
autoreconf -fiv
%configure \
	--enable-extended-sparse=yes \
	--with-libdir-suffix=%{_lib} \
	%{nil}

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%makeinstall_std

