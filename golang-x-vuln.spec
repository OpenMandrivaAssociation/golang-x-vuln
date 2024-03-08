%global debug_package %{nil}

%bcond_without bootstrap2

# Run tests in check section
# tests for cmd and internal fail
%bcond_with check

# https://github.com/golang/vuln
%global goipath		golang.org/x/vuln
%global forgeurl	https://github.com/golang/vuln
Version:		1.0.4

%gometa

Summary:	Database client and tools for the Go vulnerability database
Name:		golang-x-vuln

Release:	1
Source0:	https://github.com/golang/vuln/archive/v%{version}/vuln-%{version}.tar.gz
%if %{with bootstrap2}
# Generated from Source100
Source3:	vendor.tar.zst
Source100:	golang-package-dependencies.sh
%endif
URL:		https://github.com/golang/vuln
License:	BSD with advertising
Group:		Development/Other
BuildRequires:	compiler(go-compiler)

%description
Go's support for vulnerability management includes tooling for
analyzing your codebase and binaries to surface known
vulnerabilities in your dependencies.  This tooling is backed
by the Go vulnerability database, which is curated by the Go
security team. Go’s tooling reduces noise in your results by
only surfacing vulnerabilities in functions that your code is
actually calling.

%if ! %{with bootstrap2}
%files 
%license LICENSE PATENTS
%doc CONTRIBUTING.md README.md
%{_bindir}/govulncheck
%endif

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch

%description devel
%{description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE PATENTS
%doc CONTRIBUTING.md README.md
%doc doc

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n vuln-%{version}

rm -rf vendor

%if %{with bootstrap2}
tar xf %{S:3}
%endif

%build
%gobuildroot
%if ! %{with bootstrap2}
for cmd in $(ls -1 cmd) ; do
	%gobuild -o _bin/$cmd %{goipath}/cmd/$cmd
done
%endif

%install
%goinstall
%if ! %{with bootstrap2}
for cmd in $(ls -1 _bin) ; do
	install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done
%endif

%check
%if %{with check}
%gochecks
%endif

