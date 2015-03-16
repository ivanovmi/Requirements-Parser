%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:             openstack-cinder
Version:          2014.2.2
Release:          2%{?dist}
Summary:          OpenStack Volume service

Group:            Applications/System
License:          ASL 2.0
URL:              http://www.openstack.org/software/openstack-storage/
Source0:          https://launchpad.net/cinder/icehouse/2014.1/+download/cinder-%{version}.tar.gz
Source1:          cinder-dist.conf
Source2:          cinder.logrotate
Source3:          cinder-tgt.conf

Source10:         openstack-cinder-api.init
Source11:         openstack-cinder-scheduler.init
Source12:         openstack-cinder-volume.init
Source13:         openstack-cinder-backup.init
Source14:         openstack-cinder-volume-vmware.init
Source20:         cinder-sudoers

#
# patches_base=2014.1.1
#
Patch0001: 0001-Remove-runtime-dep-on-python-pbr-python-d2to1.patch

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-d2to1
BuildRequires:    python-oslo-sphinx
BuildRequires:    python-pbr
BuildRequires:    python-sphinx
BuildRequires:    python-setuptools
BuildRequires:    python-netaddr >= 0.7.12

Requires:         openstack-utils
Requires:         python-cinder = %{version}-%{release}

# as convenience
Requires:         python-cinderclient

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils

Requires:         lvm2
Requires:         scsi-target-utils

%description
OpenStack Volume (codename Cinder) provides services to manage and
access block storage volumes for use by Virtual Machine instances.


%package -n       python-cinder
Summary:          OpenStack Volume Python libraries
Group:            Applications/System

Requires:         sudo

Requires:         MySQL-python

Requires:         qemu-img
Requires:         sysfsutils

Requires:         python-paramiko >= 1.13.0

Requires:         python-paste

Requires:         python-qpid
Requires:         python-kombu >= 3.0.7
Requires:         python-amqplib

Requires:         python-pbr >= 0.6, python-pbr < 0.7, python-pbr > 0.7, python-pbr < 1.0
Requires:         python-eventlet >= 0.15.1
Requires:         python-greenlet >= 0.3.2
Requires:         python-iso8601 >= 0.1.9
Requires:         python-lxml >= 2.3
Requires:         python-netaddr >= 0.7.12
Requires:         python-oslo-config >= 1:1.4.0
Requires:         python-oslo-db >= 1.0.0, python-oslo-db < 1.1
Requires:         python-oslo-messaging >= 1.4.0, python-oslo-messaging < 1.5.0
Requires:         python-oslo-rootwrap >= 1.3.0
Requires:         python-osprofiler >= 0.3.0
Requires:         python-anyjson >= 0.3.3
Requires:         python-argparse
#Requires:         python-cheetah
Requires:         python-stevedore >= 1.0.0
Requires:         python-suds >= 0.4, python-suds <= 0.4.1

Requires:         python-sqlalchemy >= 0.9.7, python-sqlalchemy <= 0.9.99
Requires:         python-migrate == 0.9.1

Requires:         python-paste-deploy >= 1.5.0
Requires:         python-crypto >= 2.6
Requires:         python-barbicanclient >= 2.1.0, python-barbicanclient < 3.0.0, python-barbicanclient > 3.0.0, python-barbicanclient < 3.0.2
Requires:         python-glanceclient >= 1:0.14.0
Requires:         python-routes >= 1.12.3, python-routes < 2.0, python-routes > 2.0
Requires:         python-webob >= 1.2.3
Requires:         python-wsgiref >= 0.1.2
Requires:         python-oslo-i18n >= 1.0.0

Requires:         python-swiftclient >= 2.2.0
Requires:         python-requests >= 2.1.0, python-requests <= 2.2.1
Requires:         python-keystonemiddleware >= 1.0.0, python-keystonemiddleware < 1.4.0
Requires:         python-novaclient >= 1:2.18.0

Requires:         python-six >= 1.7.0

Requires:         python-babel >= 1.3
Requires:         python-lockfile

Requires:         python-rtslib-fb >= 2.1.fb39
Requires:         python-taskflow >= 0.4, python-taskflow < 0.7.0

Requires:         python-ceph
#Requires:         iscsi-initiator-utils
Requires:         cryptsetup

%description -n   python-cinder
OpenStack Volume (codename Cinder) provides services to manage and
access block storage volumes for use by Virtual Machine instances.

This package contains the cinder Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Volume
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python-eventlet
BuildRequires:    python-routes
BuildRequires:    python-sqlalchemy
BuildRequires:    python-webob
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-migrate, python-iso8601

%description      doc
OpenStack Volume (codename Cinder) provides services to manage and
access block storage volumes for use by Virtual Machine instances.

This package contains documentation files for cinder.
%endif

%prep
%setup -q -n cinder-%{version}

%patch0001 -p1

find . \( -name .gitignore -o -name .placeholder \) -delete

find cinder -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# TODO: Have the following handle multi line entries
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

# We add REDHATCINDERVERSION/RELEASE with the pbr removal patch
sed -i s/REDHATCINDERVERSION/%{version}/ cinder/version.py
sed -i s/REDHATCINDERRELEASE/%{release}/ cinder/version.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

pushd doc

%if 0%{?with_doc}
SPHINX_DEBUG=1 sphinx-build -b html source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.doctrees build/html/.buildinfo
%endif

# Create dir link to avoid a sphinx-build exception
mkdir -p build/man/.doctrees/
ln -s .  build/man/.doctrees/man
SPHINX_DEBUG=1 sphinx-build -b man -c source source/man build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/

popd

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/cinder
install -d -m 755 %{buildroot}%{_sharedstatedir}/cinder/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/cinder

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/cinder
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/cinder/cinder-dist.conf
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_datadir}/cinder/openstack-cinder-volume-vmware
install -p -D -m 640 etc/cinder/cinder.conf.sample %{buildroot}%{_sysconfdir}/cinder/cinder.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/cinder/volumes
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/tgt/conf.d/cinder.conf
install -p -D -m 640 etc/cinder/rootwrap.conf %{buildroot}%{_sysconfdir}/cinder/rootwrap.conf
install -p -D -m 640 etc/cinder/api-paste.ini %{buildroot}%{_sysconfdir}/cinder/api-paste.ini
install -p -D -m 640 etc/cinder/policy.json %{buildroot}%{_sysconfdir}/cinder/policy.json

# Install initscripts for services
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/openstack-cinder-api
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/openstack-cinder-scheduler
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/openstack-cinder-volume
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/openstack-cinder-backup

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/cinder

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-cinder

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/cinder

# Install rootwrap files in /usr/share/cinder/rootwrap
mkdir -p %{buildroot}%{_datarootdir}/cinder/rootwrap/
install -p -D -m 644 etc/cinder/rootwrap.d/* %{buildroot}%{_datarootdir}/cinder/rootwrap/

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/cinder-debug
rm -fr %{buildroot}%{python_sitelib}/cinder/tests/
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}/usr/share/doc/cinder/README*

%pre
getent group cinder >/dev/null || groupadd -r cinder --gid 165
if ! getent passwd cinder >/dev/null; then
  useradd -u 165 -r -g cinder -G cinder,nobody -d %{_sharedstatedir}/cinder -s /sbin/nologin -c "OpenStack Cinder Daemons" cinder
fi
exit 0

%post
for svc in volume api scheduler backup; do
    /sbin/chkconfig --add openstack-cinder-$svc
done

%preun
if [ $1 -eq 0 ] ; then
    for svc in volume api scheduler backup; do
        /sbin/service openstack-cinder-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del openstack-cinder-${svc}
    done
fi

%postun
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in volume api scheduler backup; do
        /sbin/service openstack-cinder-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

%files
%doc LICENSE

%dir %{_sysconfdir}/cinder
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/cinder.conf
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/api-paste.ini
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/rootwrap.conf
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-cinder
%config(noreplace) %{_sysconfdir}/sudoers.d/cinder
%config(noreplace) %{_sysconfdir}/tgt/conf.d/cinder.conf
%attr(-, root, cinder) %{_datadir}/cinder/cinder-dist.conf

%dir %attr(0750, cinder, root) %{_localstatedir}/log/cinder
%dir %attr(0755, cinder, root) %{_localstatedir}/run/cinder
%dir %attr(0755, cinder, root) %{_sysconfdir}/cinder/volumes

%{_bindir}/cinder-*
%{_initrddir}/openstack-cinder-*
%{_datarootdir}/cinder
%{_mandir}/man1/cinder*.1.gz

%defattr(-, cinder, cinder, -)
%dir %{_sharedstatedir}/cinder
%dir %{_sharedstatedir}/cinder/tmp

%files -n python-cinder
%doc LICENSE
%{python_sitelib}/cinder
%{python_sitelib}/cinder-%{version}*.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
* Fri Mar 06 2015 Daniil Trishkin <dtrishkin@mirantis.com> - 2014.2.2
- Update to upstream 2014.2.2

* Wed Jun 11 2014 Eric Harney <eharney@redhat.com> - 2014.1.1-2
- Add dependency on iscsi-initiator-utils

* Mon Jun 09 2014 Eric Harney <eharney@redhat.com> - 2014.1.1-1
- Update to Icehouse stable release 1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Alan Pevec <apevec@redhat.com> - 2014.1-3
- drop crudini build dependency

* Mon Apr 21 2014 Eric Harney <eharney@redhat.com> - 2014.1-2
- Remove qpid settings from cinder-dist.conf

* Thu Apr 17 2014 Eric Harney <eharney@redhat.com> - 2014.1-1
- Update to 2014.1 (Icehouse)

* Tue Apr 15 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.10.rc3
- Add python-oslo-messaging requirement
- Add GlusterFS delete patch
- Add systemd patches (not used yet)

* Tue Apr 15 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.9.rc3
- Update to Icehouse RC3

* Mon Apr 07 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.8.rc2
- Update to Icehouse RC2
- Icehouse requires newer version of python-six

* Thu Mar 27 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.7.rc1
- Update to Icehouse RC1

* Tue Mar 25 2014 PÃ¡draig Brady <pbrady@redhat.com> - 2014.1-0.6.b3
- Depend on python-rtslib and targetcli rather than scsi-target-utils

* Fri Mar 21 2014 PÃ¡draig Brady <pbrady@redhat.com> - 2014.1-0.5.b3
- Use lioadm iSCSI helper rather than tgtadm

* Sun Mar 16 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.4.b3
- Update to Icehouse milestone 3
- Add deps on python-oslo-rootwrap, python-taskflow

* Mon Jan 27 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.3.b2
- Update to Icehouse milestone 2

* Mon Jan 06 2014 PÃ¡draig Brady <pbrady@redhat.com> - 2014.1-0.2.b1
- Set python-six min version to ensure updated

* Thu Dec 19 2013 Eric Harney <eharney@redhat.com> - 2014.1-0.1.b1
- Update to Icehouse milestone 1

* Mon Oct 28 2013 Eric Harney <eharney@redhat.com> - 2013.2-2
- Fix GlusterFS volume driver clone operations

* Thu Oct 17 2013 Eric Harney <eharney@redhat.com> - 2013.2-1
- Update to 2013.2 (Havana)
- Restart/remove cinder-backup service during upgrade/uninstallation

* Wed Oct 16 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.13.rc3
- Update to Havana RC3

* Fri Oct 11 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.12.rc2
- Update to Havana RC2

* Tue Oct 08 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.11.rc1
- Update to Havana RC1
- Fix python-novaclient req epoch

* Mon Sep 23 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.10.b3
- Depend on python-novaclient 2.15

* Wed Sep 18 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.9.b3
- Add cinder-dist.conf
- Tighten permissions on /var/log/cinder

* Mon Sep 9 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.8.b3
- Update to Havana milestone 3
- Add dependency on python-novaclient

* Thu Aug 29 2013 PÃ¡draig Brady <pbrady@redhat.com> - 2013.2-0.7.b2
- Add dependency on sysfsutils to support the fiber channel driver

* Mon Aug 26 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.6.b2
- Add cinder-backup service init script

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.2-0.5.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 PÃ¡draig Brady <pbrady@redhat.com> - 2013.2-0.4.b2
- Add dependency on python-suds to support the netapp driver
- Add dependency on python-keystoneclient for auth token middleware
- Add dependency on qemu-img for volume creation from Glance images

* Sun Jul 21 2013 PÃ¡draig Brady <pbrady@redhat.com> - 2013.2-0.3.b2
- Update to Havana milestone 2

* Thu Jun 13 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.2.b1
- Update to Havana milestone 1

* Mon May 13 2013 Eric Harney <eharney@redhat.com> - 2013.1.1-1
- Update to Grizzly stable release 1, 2013.1.1

* Mon Apr 08 2013 Eric Harney <eharney@redhat.com> - 2013.1-2
- Backport fix for GlusterFS driver get_volume_stats

* Thu Apr 04 2013 Eric Harney <eharney@redhat.com> - 2013.1-1
- Update to Grizzly final release

* Tue Apr  2 2013 PÃ¡draig Brady <pbrady@redhat.com> - 2013.1-0.6.rc3
- Adjust to support sqlalchemy-0.8.0

* Wed Mar 27 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.5.rc3
- Update to Grizzly RC3 release

* Mon Mar 25 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.5.rc2
- Update to Grizzly RC2 release

* Mon Mar 18 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.5.rc1
- Update to Grizzly RC1 release

* Tue Mar 05 2013 PÃ¡draig Brady <P@draigBrady.com> - 2013.1-0.4.g3
- Add dependency on python-stevedore

* Mon Feb 25 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.3.g3
- Fix build issues with G-3 update

* Mon Feb 25 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.2.g3
- Update to Grizzly milestone 3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.1-0.2.g2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.1.g2
- Update to Grizzly milestone 2

* Thu Nov 29 2012 Eric Harney <eharney@redhat.com> - 2013.1-0.1.g1
- Update to Grizzly milestone 1

* Wed Nov 14 2012 Eric Harney <eharney@redhat.com> - 2012.2-2
- Remove unused dependency on python-daemon

* Thu Sep 27 2012 PÃ¡draig Brady <P@draigBrady.com> - 2012.2-1
- Update to Folsom final

* Fri Sep 21 2012 PÃ¡draig Brady <P@draigBrady.com> - 2012.2-0.5.rc1
- Update to Folsom RC1

* Fri Sep 21 2012 PÃ¡draig Brady <P@draigBrady.com> - 2012.2-0.4.f3
- Fix to ensure that tgt configuration is honored

* Mon Sep 17 2012 PÃ¡draig Brady <P@draigBrady.com> - 2012.2-0.3.f3
- Move user config out of /etc/cinder/api-paste.ini
- Require python-cinderclient

* Mon Sep  3 2012 PÃ¡draig Brady <P@draigBrady.com> - 2012.2-0.2.f3
- Initial release
