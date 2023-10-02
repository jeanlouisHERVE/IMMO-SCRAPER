%global srcname immoscraper
%global pyshortname immoscraper
%global __python /usr/bin/python3


Name: python-%{pyshortname}
Version: 0.1
Release: 1%{?dist}
Summary: A Python package for scraping an estate website

License: Proprietary
Source0: %{name}-%{version}.tar.gz

# Dependencies
Requires: python3

%description
This is a webscraper script to find the goods to be sold in a city for training purposes.

%prep
%autosetup -c -n python-immoscraper-%{version}
%setup -n python-immoscraper-%{version}

# Debugging statement to list the contents of the source directory
ls -l
pwd

%build
# Build the package using the Python interpreter
%{__python} setup.py build

%install
# Install the package using the Python interpreter
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

# Debugging statement to list the contents of the source directory
ls -l
pwd
cd /root/rpmbuild/BUILDROOT/python-immoscraper-0.1-1.el8.x86_64/usr/lib/python3.6/site-packages/
ls -l

%files
%doc README.md
%{python3_sitelib}/%{pyshortname}
%{python3_sitelib}/python_%{srcname}-%{version}-py3.6.egg-info

%changelog
* Sat Sep 30 2023 First Last <jeanlouis.herve@hotmail.fr> - 0.1-1
- Initial package release
