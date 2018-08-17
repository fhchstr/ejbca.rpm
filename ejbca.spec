# Prevent binary stripping -- keep this or resulting binaries will be modified
%global __os_install_post %{nil}

%define ejbca_version       6.9.0.2
%define ejbca_ver_underline 6_9_0_2
%define package_release     1
# 'stage' must be either migrX, rcX or release. Where X is a positive integer
%define stage               release

%define java_version        1.8.0

# DO NOT CHANGE ANYTHING BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING
# (except the CHANGELOG which is at the end of the file)
# ------------------------------------------------------------------------

%define ejbca_dir_orig ejbca_ee_%{ejbca_ver_underline}

# Create a preproduction package if the file .build_prep exists
%if %(test -e .build_prep && echo 1 || echo 0)
  %define platform prep
%else
  %define platform prod
%endif

Name:      ejbca-%{platform}
Summary:   EJBCA PKI Certificate Authority software
Provides:  %{name}
Version:   %{ejbca_version}
Release:   %{package_release}.%{stage}
License:   LGPL
Group:     Applications/System
URL:       https://www.ejbca.org
BuildArch: noarch
Packager:  Your Name <your.name@company.com>
Source0:   %{ejbca_dir_orig}.zip
Source1:   ejbca-custom
Patch0:    my_patch.diff

# Java openjdk is recommended by PrimeKey
Requires: java-%{java_version}-openjdk
# Tools to create new users
Requires(pre): shadow-utils
# Prevents rpmbuild from generating auto-require/auto-provide for each jar file it finds
AutoReq: no
AutoProv: no
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
EJBCA is a PKI Certificate Authority software, built using Java (JEE) technology.
Robust, flexible, high performance, scalable, platform independent, and component based.
EJBCA can be used stand-alone or integrated with other applications.

Being extremely scalable and flexible, EJBCA is suitable to build a complete PKI infrastructure
for any large enterprise or organization.

%prep
%{__rm} -rf *

unzip -q %{SOURCE0}
%{__cp} -a %{SOURCE1} .

#  Delete the Windows scripts
find . -name "*.bat" -delete
find . -name "*.cmd" -delete

# Apply the patches
pushd %{ejbca_dir_orig}
patch -p0 --ignore-whitespace < %{PATCH0}
#patch -p0 --ignore-whitespace < %{PATCH1}


%build
pushd %{ejbca_dir_orig}
ant clean build clientToolBox ejbca-db-cli


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/opt/
%{__cp} -a %{ejbca_dir_orig} %{buildroot}/opt/ejbca


%pre
# Create a 'ejbca' user & group if not already there
getent group ejbca > /dev/null || groupadd -r ejbca
getent passwd ejbca > /dev/null || \
    useradd -r -g ejbca -M -d /opt/ejbca -s /bin/bash -c 'EJBCA' ejbca


%files
%defattr(0640,ejbca,ejbca,0750)
/opt/ejbca
# Set the X bit on the scripts
%defattr(0750,ejbca,ejbca)
/opt/ejbca/bin/ejbca.sh
/opt/ejbca/bin/extra/cronverify.sh
/opt/ejbca/bin/extra/csv_to_endentity.sh
/opt/ejbca/bin/extra/sign-verify.sh
/opt/ejbca/bin/pkcs11HSM.sh
/opt/ejbca/dist/clientToolBox/ejbcaClientToolBox.sh
/opt/ejbca/dist/ejbca-db-cli/run.sh
/opt/ejbca/dist/ejbca-ws-cli/ejbcawsracli.sh

%changelog
* Fri Aug 17 2018 Your Name <your.name@company.com> - 6.9.0.2-1.release
- Initial release
