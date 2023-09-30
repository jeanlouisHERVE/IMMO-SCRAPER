%global srcname immo-scraper
%global pyshortname immoscraper

Name: python-%{pyshortname}
Version: 1.0
Release: 1%{?dist}
Summary: A Python package for scraping an estate website

License: Proprietary

# Dependencies
BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3

%description
This is a webscraper script to find the goods to be sold in a city for training purpose.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pyshortname}
%{python3_sitelib}/%{pyshortname}-%{version}-py%{python3_version}.egg-info

%changelog
* Date First Last <jeanlouis.herve@hotmail.fr> - 1.0-1
- Initial package release