%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	MAT File I/O Library
Name:		matio
Version:	1.5.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://sourceforge.net/projects/matio/
Source0:	http://downloads.sourceforge.net/matio/%{name}-%{version}.tar.bz2
Patch0:		%{name}-1.3.4-fix-underlinking.patch
BuildRequires:	zlib-devel
BuildRequires:	doxygen
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex

%description
matio is an ISO C library (with a limited Fortran 90 interface)
for reading and writing Matlab MAT files.

%package -n %{libname}
Summary:	MAT File I/O Library
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
matio is an ISO C library (with a limited Fortran 90 interface)
for reading and writing Matlab MAT files.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
Development files and headers for %{name}.

%prep
%setup -q
%patch0 -p1

%build
#./bootstrap
%configure2_5x \
	--enable-shared \
	--disable-fortran \
	--enable-extended-sparse=yes \
	--enable-test=no \
	--enable-docs=yes \
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

%files -n %{libname}
%{_libdir}/*%{name}.so.%{major}*

%files -n %{develname}
%doc NEWS README ChangeLog doxygen/latex/libmatio.pdf
%{_includedir}/*.h
%{_libdir}/*%{name}.so
%{_libdir}/*%{name}.a
%{_libdir}/pkgconfig/*.pc
