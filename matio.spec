%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	MAT File I/O Library
Name:		matio
Version:	1.3.3
Release:	%mkrel 1
License:	GPL
Group:		System/Libraries
Url:		http://sourceforge.net/projects/matio/
Source0:	http://downloads.sourceforge.net/matio/%{name}-%{version}.tar.bz2
Patch0:		%{name}-1.3.3-fix-underlinking.patch
BuildRequires:	zlib-devel
BuildRequires:	doxygen
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
matio is an ISO C library (with a limited Fortran 90 interface)
for reading and writing Matlab MAT files.

%package -n %{libname}
Summary:	MAT File I/O Library
Group:		System/Libraries

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
./bootstrap
%configure2_5x \
	--enable-shared \
	--disable-fortran \
	--enable-extended-sparse=yes \
	--enable-test=no \
	--enable-docs=yes \
	%if %{_lib} != lib
	--with-libdir-suffix=lib64
	%endif


%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

rm -rf %{buildroot}%{_docdir}/matio

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*%{name}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc NEWS README ChangeLog doxygen/latex/libmatio.pdf
%{_includedir}/*.h
%{_libdir}/*%{name}.so
%{_libdir}/*%{name}.*a
%{_libdir}/pkgconfig/*.pc
