%global srcname immoscraper
%global pyshortname immoscraper
%global __python /usr/bin/python3


Name: python-%{pyshortname}
Version: 0.1
Release: 1%{?dist}
Summary: A Python package for scraping an estate website

License: Proprietary
URL: https://github.com/jeanlouisHERVE/IMMO-SCRAPER
Source0: %{name}-%{version}.tar.gz

# Dependencies
Requires: python3

%description
This is a webscraper script to find the goods to be sold in a city for training purposes.

%prep
%autosetup -c -n python-immoscraper-%{version}
%setup -n python-immoscraper-%{version}

find . -type f -name "*.py" > debugsourcefiles.list

%build
# Build the package using the Python interpreter
%{__python} setup.py build

%install
# Install the package using the Python interpreter
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}
install -Dpm0644 debugsourcefiles.list %{buildroot}%{_datadir}/%{name}/debugsourcefiles.list

%files
%doc README.md
%{python3_sitelib}/modules/*
%{python3_sitelib}/python_%{srcname}-%{version}-py3.6.egg-info
%{_builddir}/%{name}-%{version}/debugsourcefiles.list

%changelog
* Sat Sep 30 2023 First Last <jeanlouis.herve@hotmail.fr> - 0.1-1
- Initial package release
