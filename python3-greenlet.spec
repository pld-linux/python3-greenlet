#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_without	tests		# unit tests and benchmarks (any)

%define 	module	greenlet
Summary:	Lightweight in-process concurrent programming
Summary(pl.UTF-8):	Lekkie programowanie równoległe wewnątrz procesu
Name:		python3-%{module}
Version:	3.1.1
Release:	1
License:	MIT, PSF (Stackless Python parts)
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/greenlet/
Source0:	https://files.pythonhosted.org/packages/source/g/greenlet/%{module}-%{version}.tar.gz
# Source0-md5:	13a71396abdf249280fa25d258acf435
URL:		https://pypi.org/project/greenlet/
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
BuildRequires:	python3-modules >= 1:3.5
%if %{with doc}
# already installed
BuildRequires:	python3-greenlet
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# -fno-tree-dominator-opts because https://bugzilla.opensuse.org/show_bug.cgi?id=902146
%define		specflags_x32	-fno-tree-dominator-opts

%description
The greenlet package is a spin-off of Stackless, a version of CPython
that supports micro-threads called "tasklets". Tasklets run
pseudo-concurrently (typically in a single or a few OS-level threads)
and are synchronized with data exchanges on "channels".

%description -l pl.UTF-8
Pakiet greenlet to odprysk projektu Stackless - wersji CPythona
obsługującej mikrowątki zwane "taskletami". Tasklety działają
pseudorównolegle (zwykle w jednym lub kilku wątkach na poziomie
systemu operacyjnego) i są synchronizowane przy wymianie danych
poprzez "kanały".

%package devel
Summary:	C development headers for Python 2 greenlet module
Summary(pl.UTF-8):	Pliki nagłówkowe C dla modułu Pythona 2 greenlet
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python3-devel >= 1:3.7

%description devel
This package contains header files required for C modules development.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia modułów w
C.

%package apidocs
Summary:	API documentation for Python greenlet module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona greenlet
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python greenlet module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona greenlet.

%prep
%setup -q -n greenlet-%{version}

%build
%py3_build

%if %{with tests}
BUILDDIR=$(echo $(pwd)/build-3/lib.linux-*)
PYTHONPATH="$BUILDDIR" \
%{__python3} -m unittest discover greenlet.tests

# Run the upstream benchmarking suite to further exercise the code:
PYTHONPATH="$BUILDDIR" \
%{__python3} benchmarks-3/chain.py
%endif

%if %{with doc}
PYTHONPATH=$(echo $(pwd)/build-3/lib.linux-*) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/greenlet/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/greenlet/{platform,tests}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES.rst LICENSE README.rst %{?with_tests:benchmarks-3}
%dir %{py3_sitedir}/greenlet
%attr(755,root,root) %{py3_sitedir}/greenlet/_greenlet.cpython-*.so
%{py3_sitedir}/greenlet/*.py
%{py3_sitedir}/greenlet/__pycache__
%{py3_sitedir}/greenlet-%{version}-py*.egg-info

%files devel
%defattr(644,root,root,755)
%{_includedir}/python%{py3_ver}*/greenlet

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
