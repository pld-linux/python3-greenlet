
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	python2_tests # CPython 2.x module tests

%if %{without tests}
%undefine	with_python2_tests
%endif

%define 	module	greenlet
Summary:	Lightweight in-process concurrent programming
Name:		python-%{module}
Version:	0.4.2
Release:	2
License:	MIT & PSF
Group:		Libraries/Python
URL:		http://pypi.python.org/pypi/greenlet
Source0:	http://pypi.python.org/packages/source/g/greenlet/%{module}-%{version}.zip
# Source0-md5:	580a8a5e833351f7abdaedb1a877f7ac
Patch0:		%{name}-gc_assertion_error.patch
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-2to3
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The greenlet package is a spin-off of Stackless, a version of CPython
that supports micro-threads called "tasklets". Tasklets run
pseudo-concurrently (typically in a single or a few OS-level threads)
and are synchronized with data exchanges on "channels".

%package devel
Summary:	C development headers for python-greenlet
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains header files required for C modules development.

%package -n python3-%{module}
Summary:	Lightweight in-process concurrent programming
Group:		Libraries/Python

%description -n python3-%{module}
The greenlet package is a spin-off of Stackless, a version of CPython
that supports micro-threads called "tasklets". Tasklets run
pseudo-concurrently (typically in a single or a few OS-level threads)
and are synchronized with data exchanges on "channels".

%package -n python3-%{module}-devel
Summary:	C development headers for python3-greenlet
Group:		Development/Libraries
Requires:	python3-%{module} = %{version}-%{release}

%description -n python3-%{module}-devel
This package contains header files required for C modules development.

%prep
%setup -q -n greenlet-%{version}
%patch0 -p1

%build
%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

%if %{with python2_tests}
%{__python} setup.py test

# Run the upstream benchmarking suite to further exercise the code:
PYTHONPATH=$(echo $(pwd)/build/lib.*-2.?) %{__python} benchmarks/chain.py
%endif
%endif

%if %{with python3}
# CC/CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python3} setup.py build %{?with_tests:test}

%if %{with tests}
# Run the upstream benchmarking suite to further exercise the code:
mkdir -p benchmarks-3
2to3-3.3 -o benchmarks-3 -n -w --no-diffs benchmarks
PYTHONPATH=$(echo $(pwd)/build/lib.*-3.?) %{__python3} benchmarks-3/chain.py
%endif
%endif

%install
%if %{with python2}
%{__python} setup.py \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/greenlet.txt README.rst benchmarks AUTHORS NEWS LICENSE
%attr(755,root,root) %{py_sitedir}/%{module}.so
%{py_sitedir}/%{module}*.egg-info

%files devel
%defattr(644,root,root,755)
%{_includedir}/python%{py_ver}/greenlet

%files -n python3-%{module}
%defattr(644,root,root,755)
%doc doc/greenlet.txt README.rst benchmarks AUTHORS NEWS LICENSE
%attr(755,root,root) %{py3_sitedir}/%{module}.*.so
%{py3_sitedir}/%{module}*.egg-info

%files -n python3-%{module}-devel
%defattr(644,root,root,755)
%{_includedir}/python%{py3_ver}*/greenlet
